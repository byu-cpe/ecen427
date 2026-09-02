---
layout: page
toc: true
title: Checking Your Code with Valgrind
short_title: Valgrind
indent: 1
number: 8
---

[Valgrind](https://valgrind.org/) is a tool that runs your program and watches every memory access, reporting memory errors (such as use of uninitialized memory, out-of-bounds accesses, and use after free) and memory leaks.  As described on the [Lab Submission]({% link _pages/submission.md %}) page, your userspace applications must run cleanly under valgrind.

## Running valgrind

Check your code with valgrind before you submit; it is run the same way the TAs will run it:

1. Build your code in *Debug* mode so that valgrind can report source file names and line numbers (see [Compiling and Running Code]({% link _documentation/compiling_running_code.md %})).

1. From your build directory, run your application under valgrind.  For example, for Space Invaders:

   ```bash
   valgrind --leak-check=full ./apps/space_invaders/space_invaders
   ```

   Expect your program to run much slower than normal; this is a side effect of how valgrind works.

1. For interactive applications like Space Invaders, exercise the program (play a game, trigger the different behaviors of your application), then stop it with `Ctrl+C`.  The TAs will do the same when grading.  Valgrind prints its report after the program exits.

1. Look at the end of the report.  Your submission is considered clean when:
   * The `LEAK SUMMARY` shows `0 bytes in 0 blocks` for *definitely lost*, *indirectly lost*, and *possibly lost*.  (*still reachable* memory is acceptable; system libraries often leave reachable allocations behind.)
   * The `ERROR SUMMARY` line reports `0 errors from 0 contexts`.

   A clean run ends something like this:

   ```
   ==1919== LEAK SUMMARY:
   ==1919==    definitely lost: 0 bytes in 0 blocks
   ==1919==    indirectly lost: 0 bytes in 0 blocks
   ==1919==      possibly lost: 0 bytes in 0 blocks
   ==1919==    still reachable: 27,824 bytes in 247 blocks
   ==1919==         suppressed: 0 bytes in 0 blocks
   ==1919==
   ==1919== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
   ```

## Interpreting the results

If valgrind reports errors or leaks, it will point you to the source line where the bad memory was allocated or accessed.  The `examples/valgrind` directory in your class repository contains small example programs demonstrating common memory bugs (leaks, use after free, double free, out-of-bounds access, and more), along with the valgrind output each one produces.  These are a good reference for interpreting your own valgrind reports.
