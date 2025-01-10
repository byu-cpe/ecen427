---
layout: page
toc: false
title: Compiling and Running Programs on the PYNQ Board
short_title: Compiling Programs
indent: 1
number: 9
---


Look through the files provided to you in the Git repo.  There are some helpful explanations in the README.md <https://github.com/byu-cpe/ecen427_student>.  

## Build System

For most programs you create in this class, you will compile them on your workstation, and then copy them over to the PYNQ board to run them.  This is called **cross-compiling**.  This is done because the ARM CPU on the PYNQ board is very slow, and it is much faster to compile on your workstation.  Running VS Code on your workstation will also allow you to use such benefits as intellisense and github co-pilot to help you write your code.  

### Install Compiler
Before proceeding you should install the G++ ARM compiler on your workstation.  You can do this by running the following command:

    cd <your_repo>
    make g++-arm-11.2

This will take a few minutes and you will need about 1GB of free space in your home drive. If you don't want to install these, you can compile on the PYNQ board, but it will be much slower.

### CMake 

To build your user space programs, you are required to use CMake.  CMake is a tool that will automatically create Makefiles for you, based on a configuration file called `CMakelists.txt`.  CMake is already set up in the provided repo. 

You can look at the top-level [CMakeLists.txt](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/CMakeLists.txt) file provided to you.  *Note:* This file is located in your `userspace` folder.  For the first few labs of the class you will be writing code that runs in Linux user space, so all of your code will be placed within this folder.  Later, beginning in Lab 5, you will write kernel code that will be located in the `kernel` folder, but this will not be built using the CMake system.

For Lab1, you are provided a *Hello, World* application, [main.cpp](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/apps/helloworld/main.cpp).


Note that the top-level [CMakeLists.txt](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/CMakeLists.txt) file has a `add_subdirectory(apps)` statement, which will instruct CMake to process the apps [CMakeLists.txt](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/apps/CMakeLists.txt) file.  This in turn has a `add_subdirectory(helloworld)` statement that will process the lab1 [CMakeLists.txt](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/apps/helloworld/CMakeLists.txt) file.  

### Deploying Executables to the PYNQ Board

The provided CMakeLists.txt file contains a function, [deploy_to_board()](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/CMakeLists.txt#L39), that will copy a specified executable to the PYNQ board after it is built.  To enable this for a particular executable, you would add a line like this to the CMakeLists.txt file for your executable:

    deploy_to_board(exe_name)

You don't need to do this for the first lab, as it is already done for you [here](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/helloworld/CMakeLists.txt#L2).

<span style="color:red">**IMPORTANT:**</span> Before this function will work, you need to update [this line](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/CMakeLists.txt#L46) and replace `pynq` with the hostname or IP address of your PYNQ board (A table is provided on Learningsuite). Also update the `myrepo` directory to match the path of your code repository on your PYNQ board. It might look something like this:

    COMMAND scp $<TARGET_FILE:${target_name}> byu@pynq01.ee.byu.edu:~/ecen427/cross-compiled/

### Compiling Your Code 

To compile the Lab1 executable, on your lab computer, you need to navigate to the build directory, and then run CMake and point it to the top-level CMakeLists.txt file, like so:

    cd userspace/build
    cmake ..

This will produce a Makefile in your build directory.  Run it to compile the *Hello, World* application.

    make


**Tip:** After running `cmake` once, you won't need to run it ever again (unless you completely delete your build directory).  Once CMake has set up the Makefile system, you can just re-run `make` for any future changes.  Even if you change the CMake files, the system is set up so that the generated Makefile will detect these updates, and automatically call CMake to update itself.

<span style="color:red">**IMPORTANT:**</span> Never run ''cmake'' from anywhere but your *build* directory.  It creates *many* temporary files that will clutter up your source files.

## Running Your Code 
Your executables will be copied to the *cross-compiled* directory you set in the earlier step.  Connect to your PYNQ board via SSH, and navigate to the directory where your executables are located.  You can then run them like so:

    ssh <mypynq>
    cd <myrepo>/cross-compiled
    sudo ./helloworld

While you don't need sudo to run the helloworld program, you will need it for all later programs that access hardware devices. 


## Understanding the CMakeLists.txt files 

The top-level [CMakeLists.txt](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/CMakeLists.txt) file contains the following line

    cmake_minimum_required(VERSION 3.5)

which is found at the beginning of most CMake files and indicates the minimum version of CMake that your makefile supports. The next line:

    set(CMAKE_BUILD_TYPE Release)

instructs CMake to compile your code with compiler optimizations (so it runs faster).  If you want to enable debug information, which can be helpful when using tools like *valgrind*, change this to *Debug*. 

The next set of lines allow you to compile your code on your computer, even though it has very different architecture from the ARM CPU on the PYNQ board.  This is called *cross-compiling*.  

    if (NOT ${CMAKE_HOST_SYSTEM_PROCESSOR} STREQUAL "armv7l")
        message(WARNING "Building on non-PYNQ board.  Cross-compiling will be performed.")

        SET(CMAKE_SYSTEM_PROCESSOR armv7)
        SET(CMAKE_CROSSCOMPILING 1)
        set(CMAKE_C_COMPILER "$ENV{HOME}/g++-arm-8.2-ecen427/bin/arm-linux-gnueabihf-gcc")
        set(CMAKE_CXX_COMPILER "$ENV{HOME}/g++-arm-8.2-ecen427/bin/arm-linux-gnueabihf-g++")
        add_compile_options("-march=armv7-a")
        add_compile_options("-mfpu=vfpv3")
        add_compile_options("-mfloat-abi=hard")
        add_link_options("-march=armv7-a")
        add_link_options("-mfpu=vfpv3")
        add_link_options("-mfloat-abi=hard")
        add_link_options("-mhard-float")
    endif()


The following line:
    
    include_directories(drivers)

line instructs CMake where to look for header (*.h*) files.  In Lab 2 you will create some drivers with associated header files that you will want to include in your application code.  This line ensures the compiler will find your driver header files.

    add_subdirectory(drivers)
    add_subdirectory(apps)

These lines instruct CMake to look in these directories for additional CMakeLists.txt files and process them.


The Lab 1 [CMakeLists.txt](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/apps/helloworld/CMakeLists.txt) file contains the following: 

    add_executable(helloworld main.c)

This directs CMake to create a new executable program.  The first argument is the name of the executable, which in this case is `helloworld`.  The remaining arguments to the command provide a list of source code files, which in this case is only main.c.


## Backing up Your Code

You should commit your files and push them up to Github <ins>**OFTEN!!**</ins>.  **We will not make any special accommodations for students that lose their code because they were not pushing their code up to Github frequently.**. 




## Remote Development with VS Code

Instead of cross-compiling, you can connect directly to your PYNQ board and build the code there.  This is slower, but is required for labs where you are writing kernel code.  The easiest way to do this is to use the *Remote - SSH* extension in VS Code, which allows you to run a VS code window on your workstation, but have it connect to your PYNQ board.

### Install

Install the *Remote - SSH* extension from *Microsoft*. 

<img src="{% link media/setup/vscoderemoteextensionssh.jpg %}" width="400">

### SSH Keys
Before proceeding, make sure you set up your SSH keys (`~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub`) as described on an earlier [page]({% link _documentation/setup_pynq_board.md %}#ssh-keys).  

*Note:* If you are using Windows on your personal computer, VSCode will look for your SSH keys in your Windows home directory (not the WSL home directory).  You may want to copy your SSH keys there:

    cp ~/.ssh/id_rsa* /mnt/c/Users/<your windows username>/.ssh/


### Connecting 
  - Click the blue button in the bottom left of VSCode, and select *Connect to Host..*
  - Type in `byu@<PYNQ IP or hostname>` and press enter.
  - A new VS Code window should pop up, and the VS Code server will be installed on your PYNQ board.  This can take a few minutes.  If an error pops up, try clicking *Retry* a few times.
  - Once connected, the blue box in the lower left corner should display the IP/network name.

### Opening a Folder
  - You can now click *File->Open Folder* and then select your repository folder that you cloned on the PYNQ board.
  - If you open a Terminal, it will be a remote terminal on the PYNQ board.
