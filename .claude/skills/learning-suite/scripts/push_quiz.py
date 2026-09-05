#!/usr/bin/env python3
"""Push a YAML quiz into an existing Learning Suite exam.

Usage:
  push_quiz.py ../solns/quizzes/quiz1.yml --dry-run     # convert + parse, show current and planned questions, change nothing
  push_quiz.py ../solns/quizzes/quiz1.yml               # append the YAML's questions to the exam
  push_quiz.py ../solns/quizzes/quiz1.yml --replace     # delete every existing question/block first, then import

How it works: the YAML becomes Moodle XML (quiz_to_moodle.py), Learning Suite's
own importer parses it into question JSON (a read-only server call, the same one
the Import dialog uses), this script patches what the Moodle dialect cannot
express (multiple response, case-insensitive short text, section blocks), and
the questions page's importQuestions() creates them exactly as the dialog would.

The exam must already exist with a name equal to the YAML `title`; its dates
and points are not touched. After a successful import the exam's description is
set from the YAML `description`. --replace refuses to run on a published
exam. Deleting is irreversible. Requires an authenticated session (see SKILL.md).
"""
import json
import sys
import time

import ls_quiz
import quiz_to_moodle

VM = ls_quiz.VM_JS.strip()

PARSE_JS = """
new Promise(function(r){
  require(["app/views/exam/QuestionImportUtil"], function(u){
    var f = new File([%s], "quiz.xml", {type: "text/xml"});
    u.processQuestionImportFile("Moodle", f).then(
      function(res){ r({questions: res.questions, bad: res.badQuestions || null}); },
      function(e){ r({error: String(e && e.message || e)}); });
  });
})
"""

DELETE_ALL_JS = """
new Promise(async function(r){
  var vm = %s;
  var deleted = [];
  try {
    while (vm.loadedQuestions.length) {
      var q = vm.loadedQuestions[0];
      var isBlock = ["ItemGroup", "DynamicItemGroup"].includes(q.type);
      vm.confirmDeleteQuestion(0);
      await new Promise(function(d){ setTimeout(d, 300); });
      if (isBlock) { vm.deleteBlockValue = "all"; await vm.deleteQuestionBlockButtonClick("save"); }
      else { await vm.deleteQuestionButtonClick("save"); }
      deleted.push((isBlock ? "block: " : "") + (q.title || (q.question || "").replace(/<[^>]+>/g, "").slice(0, 60)));
      await new Promise(function(d){ setTimeout(d, 400); });
    }
    r({deleted: deleted, remaining: vm.loadedQuestions.length});
  } catch (e) { r({error: String(e), deleted: deleted}); }
})
""" % VM

# Kicks off the import and returns at once; the outcome is parked on window so
# the script can poll for it (an import can outlast the CDP socket timeout).
IMPORT_JS = """
(function(){
  var vm = %s;
  var payload = %s;
  vm.importAt = vm.loadedQuestions.length; vm.importIntoBlock = false; vm.importAtInBlock = -1;
  window.__pushQuizOutcome = null; window.__pushQuizStatus = [];
  vm.importQuestions({questions: payload.questions, blocks: payload.blocks, closePopup: true,
                      resolve: function(o){ window.__pushQuizOutcome = o; },
                      updateStatus: function(s){ window.__pushQuizStatus.push(s); }});
  return true;
})()
"""

POLL_JS = """
(function(){
  var o = window.__pushQuizOutcome, st = window.__pushQuizStatus || [];
  if (!o) return {done: false, lastStatus: st[st.length-1] || null};
  return {done: true, lastStatus: st[st.length-1] || null,
          errors: (o.questionErrors || []).map(function(e){ return String(e.error || e); }),
          error: o.error ? String(o.error) : null};
})()
"""


def flatten(doc):
    """[(section_index or None, section_name, question_dict)] in YAML order, plus block names."""
    sections = doc.get("sections")
    if sections is None:
        return [(None, None, q) for q in doc.get("questions", [])], []
    rows, names = [], []
    for i, sec in enumerate(sections):
        names.append(sec.get("name") or "Block %d" % (i + 1))
        for q in sec.get("questions", []):
            rows.append((i, names[-1], q))
    return rows, names


def block_payload(name):
    return {"description": "", "headerText": name, "learningOutcomes": [], "LOCount": None,
            "scoreXofY": False, "XofYQuestionCount": None, "XofYPoints": None,
            "answerAllQuestions": None, "groupType": "Group",
            "ls_data": {"randomQuestionOrder": False, "dynamicQuestionCount": None},
            "weight": None, "deleteContents": False, "poolID": None, "numQuestions": None,
            "isDynamic": False}


def patch(parsed, rows):
    """Apply what Moodle XML cannot carry: types, case sensitivity, block membership."""
    if len(parsed) != len(rows):
        sys.exit("Learning Suite parsed %d questions but the YAML has %d; a question type was probably dropped"
                 % (len(parsed), len(rows)))
    for pq, (sec_idx, _, yq) in zip(parsed, rows):
        t = yq["type"]
        if t == "multiple_response":
            correct = [k for k, c in pq["choices"].items() if c.get("points", 0) > 0]
            # Re-split the points so they sum exactly to the question's total.
            total = float(yq.get("points", 1))
            share = round(total / len(correct), 2)
            for k, c in pq["choices"].items():
                c["correct"] = k in correct
                c["points"] = share if k in correct else 0
            pq["choices"][correct[-1]]["points"] = round(total - share * (len(correct) - 1), 2)
            pq["totalPoints"] = total
            pq["itemType"] = "MultipleResponse"
            pq["selectMaximum"] = len(correct)
            pq["selectMinimum"] = 0
            pq["partialCredit"] = bool(yq.get("partial_credit", True))
            pq.setdefault("ls_data", {})["numberOfAnswers"] = False
        elif t == "short_text":
            pq.setdefault("ls_data", {})["caseSensitive"] = bool(yq.get("case_sensitive", False))
        if sec_idx is not None:
            pq["blockNumber"] = sec_idx
    return parsed


def describe(parsed, rows):
    print("== planned import: %d questions" % len(parsed))
    last = object()
    for pq, (sec_idx, sec_name, _) in zip(parsed, rows):
        if sec_idx != last:
            last = sec_idx
            if sec_name:
                print("  [block] %s" % sec_name)
        text = pq.get("question", "").replace("<input data-index=\"0\">", "")
        text = __import__("re").sub(r"<[^>]+>", "", text).strip()
        extra = ""
        if pq["itemType"] in ("MultipleChoice", "MultipleResponse", "TrueFalse"):
            extra = " correct=" + ",".join(k for k, c in pq["choices"].items() if c.get("correct"))
        elif pq["itemType"] == "FillInTheBlank":
            extra = " accepted=" + "|".join(a["ResponseText"] for a in pq["choices"][0]["answers"])
            extra += " case=%s" % pq["ls_data"].get("caseSensitive")
        print("      %-16s %s pt  %s%s" % (pq["itemType"], pq.get("totalPoints"), text[:70], extra))


def print_summary(label, s):
    print("== %s: %d top-level items" % (label, len(s)))
    for item in s:
        if "block" in item:
            print("  [block] %s (%d questions)" % (item["block"], item["n"]))
            for c in item["children"]:
                print("      %-16s %s pt  %s" % (c["type"], c["points"], c["text"]))
        else:
            print("  %-16s %s pt  %s" % (item["type"], item["points"], item["text"]))


def count(s):
    return sum(i["n"] if "block" in i else 1 for i in s)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if len(args) != 1 or flags - {"--dry-run", "--replace"}:
        sys.exit(__doc__)
    doc = quiz_to_moodle.load(args[0])
    xml, n = quiz_to_moodle.convert(doc)
    rows, block_names = flatten(doc)
    print("converted %d questions from %s" % (n, args[0]))

    tab = ls_quiz.open_questions_page(doc["title"])
    exam = tab.exam
    print("exam %r (id %s, url %s, published=%s)"
          % (exam["name"], exam["id"], exam["url"], exam.get("isPublished")))
    before = tab.evaluate(ls_quiz.SUMMARY_JS)
    print_summary("before", before)

    res = tab.evaluate(PARSE_JS % json.dumps(xml))
    if res.get("error"):
        sys.exit("Learning Suite could not parse the Moodle XML: %s" % res["error"])
    if res.get("bad"):
        sys.exit("Learning Suite rejected questions: %s" % json.dumps(res["bad"], indent=1))
    parsed = patch(res["questions"], rows)
    describe(parsed, rows)

    if "--dry-run" in flags:
        print("dry run: nothing changed")
        tab.close()
        return

    if "--replace" in flags and before:
        if exam.get("isPublished"):
            sys.exit("refusing to --replace questions on a published exam")
        d = tab.evaluate(DELETE_ALL_JS)
        print("deleted %d items" % len(d.get("deleted", [])))
        if d.get("error") or d.get("remaining"):
            sys.exit("delete did not finish cleanly: %s" % json.dumps(d, indent=1))

    payload = {"questions": parsed, "blocks": [block_payload(b) for b in block_names]}
    tab.evaluate(IMPORT_JS % (VM, json.dumps(payload)))
    deadline = time.time() + 600
    out = {"done": False}
    while time.time() < deadline and not out.get("done"):
        time.sleep(2)
        out = tab.evaluate(POLL_JS)
    if not out.get("done"):
        print("import did not finish within 10 minutes; last status:", out.get("lastStatus"))
    elif out.get("error") or out.get("errors"):
        print("import reported problems:", json.dumps(out, indent=1))

    time.sleep(1.5)
    tab.goto(f"{ls_quiz.BASE}/questions/id-{exam['url']}", settle=2.5)
    after = tab.evaluate(ls_quiz.SUMMARY_JS)
    print_summary("after", after)
    expected = n + (0 if "--replace" in flags else count(before))
    print("questions: before=%d after=%d expected=%d %s"
          % (count(before), count(after), expected, "OK" if count(after) == expected else "MISMATCH"))
    ok = count(after) == expected and not out.get("error") and not out.get("errors")

    # Keep the exam's Learning Suite description in step with the YAML.
    desc = (doc.get("description") or "").strip()
    if desc and ok:
        res = ls_quiz.set_assignment_property(tab, doc["title"], "description", desc)
        print("description:", "unchanged" if res.get("unchanged") else "updated to %r" % desc)
    tab.close()
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
