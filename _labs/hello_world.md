---
layout: lab
toc: true
title: "Lab 1: Hello World on the PYNQ-Z2 Board"
short_title: Hello World
number: 1
---

In this lab you will set up your PYNQ board and run a simple program on it.  

## Objectives
* Set up your PYNQ board image
* Learn how to build and run programs on the PYNQ board.

## Overview 

**Before you can proceed with this lab**, you must complete [this Microsoft Form](https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=m278xvtRqEi3eZ7lZLQEE4ha3g3zImFKktW1XFmV3zhUNE45UEUzWlJPVVkwVEwzOUxXTkc3RU5QTC4u) and submit your GitHub username.  Your Git repository for the semester is created from these form responses, which may take up to 24 hours.  If you added the class late, message the instructor so your repository gets created promptly.

To fully pass off this lab, you will need to perform all of the required setup activities listed below, including tutorials on Linux and Git.  Questions from this material will be on the first quiz.

The last setup step involves compiling and running a *Hello, World!* application on the PYNQ board.  You need modify this program as described below, and submit your code.




## Requirements 

This page describes how to set up your computer and PYNQ board for the labs in this class.  This takes some time, but it is essential that you get all of these things working before moving on the later labs.  

If you run into issues, post on Teams.  <ins>**Do not skip any setup steps**</ins>.  For convenience, these setup steps are also shown in the sidebar.

  * [Image the PYNQ SD card]({% link _documentation/pynq_imaging.md %})
  * [Setup the PYNQ board]({% link _documentation/setup_pynq_board.md %})
  - [Complete the Tutorials]({% link _documentation/tutorials.md %})  
  - [Setup Git/Github]({% link _documentation/setup_git.md %})  
  - [Compiling and Running Programs]({% link _documentation/compiling_running_code.md %})  


After you have completed these steps, do the following:

  - Modify the *Hello, World* application so that it prints `Hello, World from <your name>!`
  - Submit your code.


##  Submission

Follow the instructions on the [Submission]({% link _pages/submission.md %}) page.

## Lifelong Learning: What's Next?

During setup you ran `ssh-keygen` and `ssh-copy-id`, and suddenly you could log into your board without a password.  That wasn't magic; it was public-key cryptography.

Explore this question: **What did `ssh-keygen` and `ssh-copy-id` actually do?**
  * What are the two files `ssh-keygen` created, and what is each one for?
  * What ended up in `~/.ssh/authorized_keys` on the board, and how does the server use it to decide you are you?
  * Why does the private key never need to leave your machine, even during login?  (At a hand-wavy level, how can you prove you *have* a secret without *showing* it?)

**AI use is encouraged for this section.**  This is a great topic to explore in a conversation with an AI tool.  See the [Lifelong Learning: What's Next?]({% link _pages/lifelong_learning.md %}) page.

When you're done, record what you learned in a few sentences in `lifelong_learning/lab1.txt`.
