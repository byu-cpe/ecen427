---
layout: page
toc: true
title: Git Setup
indent: 1
number: 7
---


In the labs for this class, you will be completing some tasks on your computer, and some tasks on the PYNQ board.  In this setup step, you will set up your Git repository and SSH keys on both your computer and the PYNQ board.  


## Computer Setup
> 📝 Run this on your computer.


### Register your SSH Key with Github


  - Run `ls ~/.ssh/id_*.pub` to find your public key file.  Depending on the Ubuntu version, it will be named either `id_ed25519.pub` or `id_rsa.pub`.
  - Run `cat ~/.ssh/<your key file>` to display your public key.  Copy the entire outputted text, including the `ssh-ed25519` (or `ssh-rsa`) at the beginning and computer address at the end.
  - Go to <https://github.com/settings/keys>, click *New SSH key* button, and paste your key in the *Key* box.  Give your key a name (like *caedm*) and click *Add SSH key* to save the key.
  - Check that you can now authenticate with Github by running
  
        ssh -T git@github.com  
        
    You should see a message like this:
  
        Hi <your_github_username>! You've successfully authenticated, but GitHub does not provide shell access.


### Github Repository Access

A private repository is created for you, already containing the starter code.  You will use this repository throughout the entire semester.

1. Make sure you have completed the Microsoft Form asking for your GitHub username.  Your repository is created from these form responses, so it cannot be created until you have done this.

1. Once your repository has been created, GitHub will email you an invitation to collaborate on *byu-ecen427-classroom/427-labs-\<your_github_username\>* (sent to the email address on your GitHub account).  Accept it.  If you can't find the email, log in to Github and visit `https://github.com/byu-ecen427-classroom/427-labs-<your_github_username>`, replacing `<your_github_username>` with your GitHub username; a banner with the invitation will appear at the top of the page.

1. Repositories are created in batches as students complete the form, which may take up to 24 hours.  If you haven't received an invitation within a day of completing the form, post on Teams.

### Clone your Repo

  - Go to your repository page: *https://github.com/byu-ecen427-classroom/427-labs-\<your_github_username\>*
  - Click the **Code** button, and then the **SSH** tab.
  - Copy the URL that is shown.  It should be something like: *git@github.com:byu-ecen427-classroom/427-labs-\<your_id\>.git*
  - Clone the repository into a directory you want to use, for example:  

        git clone <github_ssh_address> ~/ecen427

  - Open this in VS Code by running `code ~/ecen427`



### Add Starter Code Remote 

  - When you clone your repo, Git will create a *remote* called *origin* that is connected to your repo. 
  - You can view your remotes by typing `git remote`, and even check the linked URL by typing `git remote get-url origin`.
  - Next, you should add a new remote.  You can call it whatever you like, but a good name is *startercode*.  This remote will link to the starter code repository.  This will allow you to retrieve any updates I make to the code provided to you (I will probably need to make some updates to the code during the semester).  You do this like so:

        git remote add startercode https://github.com/byu-cpe/ecen427_student


Then, if you ever need to pull down changes I make, you can do the following to fetch the latest changes from the starter code and merge them into your code:
  
    git fetch startercode
    git merge startercode/main

## PYNQ Setup

> 📝 Run this on the PYNQ board

### Create SSH Key
Create an SSH key on the PYNQ by running `ssh-keygen` (you can just hit *Enter* a bunch of times to skip the prompts).
This will create two files in your `~/.ssh` directory: `id_rsa` and `id_rsa.pub`.  The `id_rsa` file is your private key, and the `id_rsa.pub` file is your public key (The filenames are different than when you ran ssh-keygen on the lab computers, because the different Ubuntu versions in the lab versus the board have different default key formats).  **Do not share your private key with anyone.**

### Register with Github

Follow the same steps as above to register your PYNQ public key with Github.  Note that on the PYNQ board your public key is `~/.ssh/id_rsa.pub` and begins with `ssh-rsa`, which differs from your computer as described above.  Check that you can now authenticate with Github by running 

    ssh -T git@github.com
  
### Clone your Repo on the PYNQ

Follow the same steps as above to clone your repo on the PYNQ.  

### Configure Git 

Since this is the first time using Git on the PYNQ system, you need to configure it.  Run these commands (**making sure to enter your name and email**):
```
git config --global user.name "Your Name"
git config --global user.email your_email@example.com
```
