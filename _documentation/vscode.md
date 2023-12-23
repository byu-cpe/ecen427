---
layout: page
toc: false
title: Setup VSCode
indent: 1
number: 8
---

There are two ways for us to work on our PYNQ filesystem remotely:

1. Mounting the remote PYNQ filesystem on our local computer.  This will make it appear as if the PYNQ filesystem is a folder on your computer. This allows us to use our computer's processor to analyze and compile code, so it is much faster than working directly on the PYNQ board.  This is what I would advise to use most of the time.

1. Connecting to the PYNQ board via VS Code Remote Extension, and editing and compiling on the PYNQ board.  This will run much slower, but is mandatory for the labs where you are doing kernel development.

## Method 1: Mounting the PYNQ Filesystem

> 📝 Run this on your computer.

1. Create a directory where you will mount the PYNQ remote filesystem.  For example:

        mkdir ~/pynq_remote

1. Run the sshfs command to mount the remote filesystem:

        sshfs -o idmap=user byu@PYNQ_IP:~/repo ~/pynq_remote
        
    Replacing `PYNQ_IP` with the IP address or network name of your PYNQ board, `~/repo` with the path of your repository on the PYNQ board.

1. Verify that you can view and edit the files on the PYNQ board.

        cd ~/pynq_remote
        ls
        touch test.txt

1. You can unmount the filesystem by running:

        fusermount -u ~/pynq_remote

    You will need to close any windows or terminals using this directory before the command will work.

## Install VS Code 

VSCode is already installed on the lab computers.  If you are using your personal computer, install it from <https://code.visualstudio.com/download>

Next, Install the *Remote - SSH* extension from *Microsoft*. 

<img src="{% link media/setup/vscoderemoteextensionssh.jpg %}" width="400">

## SSH Config and SSH Keys
Before proceeding, make sure you set up your SSH config file (`~/.ssh/config`) and SSH keys (`~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub`) as described on an earlier [page]({% link _documentation/setup_pynq_board.md %}#ssh-keys).  

*Note:* If you are using Windows on your personal computer, VSCode will look for your SSH config file and SSH keys in your Windows home directory (not the WSL home directory).

<!-- 
  - Create a .ssh folder if you don't have one: ''mkdir /mnt/c/Users/<your windows username>/.ssh''
  - Copy over the config file: ''cp ~/.ssh/config /mnt/c/Users/<your windows username>/.ssh/''
  - Copy over the SSH keys: ''cp ~/.ssh/id_rsa* /mnt/c/Users/<your windows username>/.ssh/''  -->

### SSH Config 

Before proceeding to setup VSCode, you will need to create an SSH config file on your home computer.
  * Click the green button in the bottom left of VSCode, and select *Remote-SSH: Open Configuration File...*.  Note: if there is no green button in the bottom left, you haven't installed the *Remote - SSH* extension (see above).

  <img src="{% link media/setup/vscodegreenbutton.jpg %}" width="200">

  * You will then be asked to select an SSH configuration file to open.  You should pick the one that is in your home directory (*~/.ssh/config*).
  * This SSH configuration file is used to tell the SSH program about computers you can connect to, and to save settings for each computer.  This file may be empty right now, but you should add a new entry like this:

```
Host pynq<number>
    Hostname pynq03.ee.byu.edu
    User byu
```
   
The SSH config serves as a shortcut for using SSH, and is required by VSCode for remote connections.  Keep in mind that as you switch seats and boards in the lab, you will need to add new entries to this file.

<!-- If you are running Windows with WSL, VSCode will be using the ''.ssh/config'' file in your **Windows** home directory, but you may also choose to place an identical file in your **WSL** home directory (''~/.ssh/config'').  That way you can simply type:<code>
ssh pynq
</code>
from the WSL terminal.  If you are using Mac or Linux, you don't need to create an extra config file, as the one created by VSCode should be sufficient.
 -->

### Connecting via SSH 
  - Click the green button in the bottom left of VSCode, and select *Remote-SSH: Connect to Host..*
  - If your SSH config file is set up correctly, you should now be given a list of the machines available in your SSH config file.  Select your *pynq\<number>* board.
  - A new VSCode window should pop up, and the VSCode server will be installed on your PYNQ board.  This can take a few minutes.  If an error pops up, try clicking *Retry* a few times.
  - Once connected, the green status bar in the lower left corner should read *SSH: pynq\<number>*
  - You can now click *File->Open Folder* and then select your *ecen427* repository folder that you cloned earlier.

### Re-Connecting

If the future, you can just press *Ctrl+R* to list all of the recent folders you have opened.  This can be used to quickly reconnect to the PYNQ board and open your repository.

## Install VSCode Extensions 
When you open the folder using VSCode, you should see a message indicating that there are recommended extensions for your code.  Click *Install All*.

<img src="{% link media/setup/vscode_recommendations.png %}" width="400">




## Accessing the Terminal 

Instead of using a separate terminal to SSH to your PYNQ, you may prefer to use the terminal integrated in VSCode.  Click *Terminal->New Terminal* (Ctrl+~) to open a remote terminal.

## Committing Code via Git 
From VSCode you can now directly edit your files and commit them to your Github repository.  Try it out:
  - Create a new file called *README*.  You can do this by opening the *Explorer* view in VSCode (top button in left-hand pane), then in the file browser, right-click and select *New File*.
  - Add the line *This is the ECEN427 repo for \<your name\>* to your file and save it.
  - Open the *Source Control* view of VSCode (third button down in the left-hand pane).  Your new file should be listed in the *Changes* section.
  - Click the **+** button next to your file to Stage it for commit.
  - Add a commit message and click the check mark to commit (or Ctrl+Enter)
  - Push this commit up to Github by clicking the three dots and selecting *Push*, or by clicking the Sync button in the bottom blue strip of VSCode (two buttons to the right of the green SSH button you used earlier).