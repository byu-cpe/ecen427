---
layout: page
toc: false
title: Lab Submission
short_title: Lab Submission
indent: 0
number: 3
icon: fa fa-cloud-arrow-up
sidebar: true
---

Lab pass-offs will not be done in person.  Instead, you will run a script that will perform the official submission of your lab to the GitHub repository.  It will do the following:
* Tag your repository with the proper lab-specific tag
* Check to make sure that the `.commitdate` file in your tagged repository is created. (this will be used to determine if you submitted on time)

**Important:** Before submitting, make sure you have completed the [Lifelong Learning and Service]({% link _pages/lifelong_learning_and_service.md %}) requirement for the lab.

To submit your lab, run one of the following commands from within your lab repository:
```bash
make submit_lab1
make submit_lab2
make submit_lab3
make submit_lab4_m1
make submit_lab4_m2
make submit_lab4_m3
make submit_lab5_m1
make submit_lab5_m2
make submit_lab5_m3
make submit_lab5_m4
make submit_lab6_m1
make submit_lab6_m2
make submit_lab7
make submit_lab8
```

You may run the `make submit_*` script as many times as you like (there is no penalty for multiple submissions).
However, every time you run `make submit_*`, the submission date of your lab will be updated.
If your submission date is past the deadline for the lab, you will receive a late penalty as described in the syllabus.

<!-- Describe other options to the submission script -->

## Submitting complete, buildable code

The TAs grade your lab by cloning your tagged submission and building it with the standard build process.
They will not repair your build for you.
Before you submit, make sure that:

* Every source file you wrote is committed **and pushed** — not just saved locally.
* Every change you made to a `CMakeLists.txt` is committed and pushed.  The lines you uncomment in
  `userspace/drivers/CMakeLists.txt` and `userspace/apps/CMakeLists.txt` to compile your drivers and
  applications are especially easy to forget, because your own build keeps working after you edit them.
* A fresh clone of your repository builds cleanly.  The surest way to check is to clone your repository
  into a new directory and build it there.

<span style="color:red">**If the TAs cannot build your submission — for example, because your CMake files are
missing or configured incorrectly — and they have to modify your build in order to grade it, an automatic
10% deduction will be applied.**</span>

<span style="color:red">**If you forget to commit your code and a TA has to reach out to you to obtain it, you
will receive a 20% penalty for the first offense (equivalent to the minimum late penalty).  For any
subsequent offense, you will be required to resubmit the lab at the then-current date, and that resubmission
will incur the associated late penalty.**</span>

## If the submission fails . . .

If your `make submit_*` continues to print messages saying that the commit file has not been created then you may not have GitHub Actions setup properly on your GitHub repository.
Follow these instructions to fix this problem (this is a one-time problem that occurs when you first setup your repository).

1. Visit the website of your repository


1. Click on the "Actions" button in the tool-bar of the web page.

   <img src="{% link media/git/git_web_toolbar.png %}">

   You may see the following image:

   <img src="{% link media/git/git_actions.png %}" >

   Click "Enable Actions on this repository"

1. Make a small change in your repository. (i.e., change the aboutme.txt or such).
   Recommit the file and push it to the repository.

1. Rerun the passoff script.