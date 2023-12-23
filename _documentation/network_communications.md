---
layout: page
toc: false
title: Setting Up Network Communications
short_title: PYNQ Network
indent: 1
number: 5
---


## SSH Communication 
Once you have the PYNQ set up you can connect to it using SSH. 

If you are working in the lab, you can access the PYNQ board in the lab using:

    ssh byu@pynq03.ee.byu.edu
        
where the "03" is replaced with the number of the PYNQ board you are using.  **The default password is `byu`.**  

If working remotely, you will need to replace *pynq03.ee.byu.edu* with your PYNQ's IP address.





## SSH Keys
Instead of having to authenticate with a password each time connecting to the PYNQ, you should set up an SSH key.  

### Generate a Public/Private Key Pair
If you don't already have public/private keys created (they are usually located at `~/.ssh/id_rsa.pub` and `~/.ssh/id_rsa`), you can generate one by running `ssh-keygen` on your computer.  

Then run `ssh-copy-id <PYNQ IP/hostname>` to enable passwordless connections to the PYNQ.

**Before proceeding, make sure you can ssh into your PYNQ board without being prompted for a password.**

