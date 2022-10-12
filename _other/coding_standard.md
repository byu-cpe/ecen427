---
layout: page
toc: false
title: ECEn 427 Coding Standard
short_title: Coding Standard
indent: 0
number: 2
---


**(We use the same coding standard as ECEN 330)**

Click the link below to leave the 427 website and be taken to the ECEN 330 coding standard page.


[ECEN 330 Coding Standard](https://byu-cpe.github.io/ecen330/other/coding-standard/)


## Grading Source Code 
The TAs will apply the following method  when evaluating your source code. The goal is to get you in the habit of writing, readable, reusable, high-quality code. As such the TAs will be quite strict when grading your code.
  * In general, the coding standard counts toward 20% of your lab grade (some labs don't apply).
  * Each lab has a set number of maximum points that represents how many infractions can be made before you earn 0% on the coding standard portion.
  * You will lose a point for each infraction, not just each type of infraction; however, the maximum number of points you can lose for each type of infraction is 3.  For example, if your code has 8 magic numbers, you will lose 5 points. 
  * For example, in Lab 2, if you lose 5 points, you will receive a coding standard score of 5/10, and thus 15%/30% on the coding standard portion of the lab.
 

| Lab  |  Points | Notes on Lab |
|------|---------|--------------|
| Lab2 |  10 | 20% of lab grade |
| Lab3 |  30 | 20% of lab grade |
| Lab4 |  15 | 20% of lab grade |
| Lab6 |  10 | 20% of lab grade |

## Lab 3 Notes

For lab 3 you have the choice of using the traditional coding standard grader, or an automatic linting tool (clang-tidy).

### Traditional Coding Standard

* You are not responsible for any violation of the coding standard in the provided .h or .cpp files.

### Linter

If you alternatively use the clang-tidy linter, you can be sure to get 100\% on the coding standard grade; however, you may find it very challenging to address the linting issues, as you may need to learn new things about C++ you weren't previously aware of.

The run clang-tidy:
1. Make sure you have the latest version of the userspace *CMakeLists.txt* file.  It should have these lines in it:
    ```
    if (TIDY)
      find_program(CLANG_TIDY_EXE NAMES "clang-tidy" REQUIRED)
      set(CLANG_TIDY_COMMAND "${CLANG_TIDY_EXE}" "-checks=modernize-*,bugprone-*,clang-analyzer-*,cppcoreguidelines-*,google-*,misc-*,portability-*,-google-readability-braces-around-statements")
    ```

1. When you run cmake, specify the TIDY option:
  ```
  cd userspace/build
  cmake .. -DTIDY=1
  ```

1. Compile as usual, and note that a warning will be printed for each clang-tidy linter error.

Similar to the traditional coding standard checker, you will be deducted one point for each linting warning.  Also like the traditional coding standard, you will lose a point for each infraction, not just each type of infraction; however, the maximum number of points you can lose for each type of infraction is 3.

