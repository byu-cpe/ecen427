#!/usr/bin/env python3
"""Convert a quiz written in YAML into Moodle XML that Learning Suite can import.

Usage:
  quiz_to_moodle.py ../solns/quizzes/quiz1.yml [out.xml]      # default: print to stdout

YAML layout (see ../solns/quizzes/README.md for the full reference):

  title: "Quiz 1: OS, Lab 1"        # exact Learning Suite exam name
  sections:                          # optional; each becomes a question block
    - name: Operating Systems
      questions:
        - type: multiple_choice      # one correct answer
          text: Question text (plain text or HTML)
          choices: [A, B, C]
          correct: 0                 # 0-based index, or the choice text
          points: 1                  # optional, default 1
          feedback: shown after grading   # optional
        - type: multiple_response    # several correct answers
          choices: [...]
          correct: [0, 2]
        - type: true_false
          correct: true
        - type: short_text
          accepted: [strace]         # any of these, case-insensitive
        - type: open_response        # free text, graded by hand
  questions: [...]                   # alternative: flat list, no blocks

The generated file matches the dialect Learning Suite itself produces from its
"Export questions" dialog (Moodle XML, html-format CDATA text, fraction
percentages). Section names are emitted as <question type="category"> markers,
which Learning Suite ignores on import; push_quiz.py recreates them as blocks.
"""
import html
import sys

import yaml

TYPES = {"multiple_choice", "multiple_response", "true_false", "short_text",
         "open_response"}
# Not offered: Moodle "numerical" questions are silently dropped by Learning Suite's importer.


def as_html(text):
    """Plain text becomes a <p>; anything already containing a tag is passed through."""
    text = str(text).strip()
    if "<" in text and ">" in text:
        return text
    return "<p>%s</p>" % html.escape(text, quote=False).replace("\n", "<br>\n")


def cdata(s):
    return "<![CDATA[%s]]>" % s.replace("]]>", "]]]]><![CDATA[>")


def htext(s):
    return '<text>%s</text>' % cdata(as_html(s))


def feedback_el(s):
    return '<feedback format="html">%s</feedback>' % htext(s or "")


def resolve_correct(q, choices):
    """Return the set of 0-based correct indices for a choice question."""
    raw = q["correct"]
    items = raw if isinstance(raw, list) else [raw]
    out = set()
    for c in items:
        if isinstance(c, bool):
            raise ValueError("choice question %r: 'correct' must be an index or choice text" % q["text"][:40])
        if isinstance(c, int):
            if not 0 <= c < len(choices):
                raise ValueError("question %r: correct index %d out of range" % (q["text"][:40], c))
            out.add(c)
        else:
            matches = [i for i, ch in enumerate(choices) if str(ch).strip() == str(c).strip()]
            if len(matches) != 1:
                raise ValueError("question %r: correct text %r does not match exactly one choice" % (q["text"][:40], c))
            out.add(matches[0])
    return out


def choice_question(q, name, single):
    choices = q["choices"]
    correct = resolve_correct(q, choices)
    if single and len(correct) != 1:
        raise ValueError("multiple_choice %r needs exactly one correct answer" % q["text"][:40])
    if not correct:
        raise ValueError("multiple_response %r needs at least one correct answer" % q["text"][:40])
    # Learning Suite rounds each share to two decimals of the grade, so hand out
    # whole-percent shares that sum to exactly 100 (34/33/33 rather than 3 x 33.33).
    base, extra = divmod(100, len(correct))
    shares = {}
    for k, idx in enumerate(sorted(correct)):
        shares[idx] = base + (1 if k < extra else 0)
    parts = ['<question type="multichoice">',
             '<name><text>%s</text></name>' % html.escape(name),
             '<questiontext format="html">%s</questiontext>' % htext(q["text"]),
             '<generalfeedback format="html">%s</generalfeedback>' % htext(q.get("feedback", "")),
             '<penalty>0.3333333</penalty><hidden>0</hidden>',
             '<defaultgrade>%s</defaultgrade>' % q.get("points", 1),
             '<single>%d</single>' % (1 if single else 0),
             '<shuffleanswers>%s</shuffleanswers>' % ("true" if q.get("shuffle") else "false"),
             '<answernumbering>abc</answernumbering>',
             '<correctfeedback format="html">%s</correctfeedback>' % htext(""),
             '<partiallycorrectfeedback format="html">%s</partiallycorrectfeedback>' % htext(""),
             '<incorrectfeedback format="html">%s</incorrectfeedback>' % htext(""),
             '<shownumcorrect/>']
    for i, ch in enumerate(choices):
        frac = str(shares[i]) if i in correct else "0"
        parts.append('<answer fraction="%s" format="html">%s%s</answer>'
                     % (frac, htext(ch), feedback_el("")))
    parts.append('</question>')
    return "".join(parts)


def true_false_question(q, name):
    ans = q["correct"]
    if isinstance(ans, str):
        ans = ans.strip().lower() in ("true", "t", "yes")
    if not isinstance(ans, bool):
        raise ValueError("true_false %r: 'correct' must be true or false" % q["text"][:40])
    fb = q.get("feedback", "")
    parts = ['<question type="truefalse">',
             '<name><text>%s</text></name>' % html.escape(name),
             '<questiontext format="html">%s</questiontext>' % htext(q["text"]),
             '<generalfeedback format="html">%s</generalfeedback>' % htext(fb),
             '<penalty>1</penalty><hidden>0</hidden>',
             '<defaultgrade>%s</defaultgrade>' % q.get("points", 1)]
    for val in (True, False):
        parts.append('<answer fraction="%d" format="moodle_auto_format"><text>%s</text>%s</answer>'
                     % (100 if val == ans else 0, "true" if val else "false",
                        feedback_el(fb if val != ans else "")))
    parts.append('</question>')
    return "".join(parts)


def short_text_question(q, name):
    accepted = q.get("accepted") or []
    if isinstance(accepted, str):
        accepted = [accepted]
    if not accepted:
        raise ValueError("short_text %r needs a non-empty 'accepted' list" % q["text"][:40])
    parts = ['<question type="shortanswer">',
             '<name><text>%s</text></name>' % html.escape(name),
             '<questiontext format="html">%s</questiontext>' % htext(q["text"]),
             '<generalfeedback format="html">%s</generalfeedback>' % htext(q.get("feedback", "")),
             '<penalty>0.3333333</penalty><hidden>0</hidden>',
             '<defaultgrade>%s</defaultgrade>' % q.get("points", 1),
             '<usecase>%d</usecase>' % (1 if q.get("case_sensitive") else 0)]
    for a in accepted:
        parts.append('<answer fraction="100" format="moodle_auto_format"><text>%s</text>%s</answer>'
                     % (html.escape(str(a)), feedback_el("")))
    parts.append('</question>')
    return "".join(parts)


def open_response_question(q, name):
    return "".join(['<question type="essay">',
                    '<name><text>%s</text></name>' % html.escape(name),
                    '<questiontext format="html">%s</questiontext>' % htext(q["text"]),
                    '<generalfeedback format="html">%s</generalfeedback>' % htext(q.get("feedback", "")),
                    '<penalty>0</penalty><hidden>0</hidden>',
                    '<defaultgrade>%s</defaultgrade>' % q.get("points", 1),
                    '<responseformat>editor</responseformat><responserequired>1</responserequired>',
                    '<responsefieldlines>10</responsefieldlines><attachments>0</attachments>',
                    '<graderinfo format="html">%s</graderinfo>' % htext(q.get("grader_notes", "")),
                    '</question>'])



def category_marker(name):
    return ('<question type="category"><category><text>%s</text></category></question>'
            % html.escape(str(name)))


def convert(doc):
    if "title" not in doc:
        raise ValueError("quiz YAML needs a 'title' (the Learning Suite exam name)")
    sections = doc.get("sections")
    if sections is None:
        sections = [{"name": None, "questions": doc.get("questions", [])}]
    out = ['<?xml version="1.0"?>', '<quiz>']
    n = 0
    for sec in sections:
        if sec.get("name"):
            out.append(category_marker(sec["name"]))
        for q in sec.get("questions", []):
            n += 1
            t = q.get("type")
            if t not in TYPES:
                raise ValueError("question %d: unknown type %r (expected one of %s)"
                                 % (n, t, ", ".join(sorted(TYPES))))
            if "text" not in q:
                raise ValueError("question %d has no 'text'" % n)
            name = "Question #%d" % n
            if t == "multiple_choice":
                out.append(choice_question(q, name, single=True))
            elif t == "multiple_response":
                out.append(choice_question(q, name, single=False))
            elif t == "true_false":
                out.append(true_false_question(q, name))
            elif t == "short_text":
                out.append(short_text_question(q, name))
            elif t == "open_response":
                out.append(open_response_question(q, name))
    out.append('</quiz>')
    return "\n".join(out) + "\n", n


def load(path):
    with open(path) as fh:
        return yaml.safe_load(fh)


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    doc = load(sys.argv[1])
    xml, n = convert(doc)
    if len(sys.argv) == 3:
        with open(sys.argv[2], "w") as fh:
            fh.write(xml)
        print("wrote %d questions for %r to %s" % (n, doc["title"], sys.argv[2]))
    else:
        sys.stdout.write(xml)


if __name__ == "__main__":
    main()
