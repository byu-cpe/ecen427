---
layout: lab
toc: true
title: "Lab 4: Space Invaders (No Sound)"
short_title: Space Invaders
number: 4
under_construction: false

---
In this lab you will write  the software that implements all functionality (except sound) for Space Invaders.

## Objective
* Gain experience interacting with a Linux driver (HDMI driver) from user space.
* Practice writing C++ application code.
* Practice with software [concurrency](https://stackoverflow.com/questions/1050222/what-is-the-difference-between-concurrency-and-parallelism).

## Team Git Repository 

This is the only lab where you will be permitted to work in a team.  Your team will be three students.  The teams are pre-set and are listed on Learning Suite.  If two teams mutually agree, you may swap team members.  Do this before proceeding with the next step.


You will use a shared repository for this lab, and then return to working in your private repository for the remainder of the labs.  Once you have your team arranged, follow this link to create a new shared Github repository for lab 3: <https://classroom.github.com/a/FIA1_rqk>
  * The first team member to sign up should create a new team name.
  * The other team members can join the team created by the first team member.
  * Once you have a team repository created, **each member of the team** needs to complete the Learning Suite quiz to indicate their team repository URL.

Once your empty lab 3 repository is created, you will need to import one of your team member's individual repository, into your shared repository. You can choose which member of team's code to use, but **all team members must have submitted lab3 before you share your code**.

You can do this in a similar manner to how you obtained the starter code:

        git clone --bare git@github.com:<team member's repo>.git
        cd <team member's repo>.git/
        git push --mirror git@github.com:byu-ecen427-classroom/<your team repo>.git
        cd ..
        rm -rf <team member's repo>.git


## Implementation

### Milestone 1: Graphics

<!-- <iframe width="500" height="350"
src="https://www.youtube.com/embed/V5XPFLa0Cdk?start=200">
</iframe> -->

In this milestone you will implement the functions defined in [Graphics.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Graphics.h). These should be implemented in *Graphics.cpp*.  Some resources to review:
  * Refer to the [HDMI]({% link _documentation/hdmi.md %}) page for documentation on how to interact with the HDMI driver.
  * The individual sprites defined in [resources/sprites.c](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/resources/sprites.c)
  * The [Sprites.cpp](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Sprites.cpp)/[Sprites.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Sprites.h) class which instances all of the individual sprites, provides enums and access functions to get the sprite data.

Your graphics functions need to be efficient and execute quickly.  The best way to do this is to reduce the number of system calls you make to the HDMI driver.

Several test functions are provided, and will be used to evaluate your graphics functions:
1. The [graphics_test](https://github.com/byu-cpe/ecen427_student/tree/main/userspace/apps/graphics_test) program should be used first to verify correctness of your Graphics functions.  It should produce an image that looks like this:
    <img src="{% link media/graphics_test.jpg %}" width="500">
  
    Pay attention to how your UFO (in red) and tank (in yellow) are drawn, as they test sprite drawing with no filled background color vs. filled background color, respectively.  
1. The [graphics_syscall](https://github.com/byu-cpe/ecen427_student/tree/main/userspace/apps/graphics_syscalls) program.  This program draws a single large sprite.  It should be run like so to measure the number of system calls made:
   ```
   sudo strace --summary-only ./graphics_syscalls
   ```
   When this test program is run, the number of system calls should be less than 500. If you are making more than 500 system calls, you will need to better optimize your code.
1. The [graphics_benchmarking](https://github.com/byu-cpe/ecen427_student/tree/main/userspace/apps/graphics_benchmarking) program.  This will measure the average runtime to perform the *drawSprite()* functions on a sprite of a set size.  The average reported runtime for the *drawSprite()* functions should be less than 3ms.

### Milestone 2 

<iframe width="500" height="350"
src="https://www.youtube.com/embed/kGd4K0jBjis">
</iframe>

Implement all of the game video except for bullets and collisions.  Tanks should move, aliens should march, etc.  Use the video above as a reference. Keep in mind that when an entire column of aliens is gone from the edge the remaining aliens keep marching to the edge of the screen, past where the would have stopped if the edge aliens were alive. This feature doesn't need to be functional for this milestone, but keep it in mind for the next milestone.

The approach you take to the game timing should be tick-based, controlled by the FIT interrupt, similar to the clock lab.  You may find it helpful to use state machines as you learned in ECEn 330 and ECEn 390, although this is not required.  If you decide not to use state machines, your code must still work with the tick-based approach.

You are provided with a [main.cpp](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/main.cpp) file.  This file already is set up to use the FIT timer to tick the game.  The game is designed to run at 60 ticks per second (or 60fps), although you shouldn't redraw everything every tick.  Instead, you should only redraw sprites as they move or change.  The provided code will report whether you are missing interrupts (which would cause the game to run slower than 60fps).  This occurs if the code in any given loop iteration exceeds 16.67ms.  You will see 1 missed interrupt as the code starts up, but it should not increase after that.  

You can optionally comment out [this line](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/main.cpp#L60), which will cause the game to run as fast as possible, not waiting for the FIT interrupt before ticking.  The loop will report the longest time spent in a tick, which can be useful for debugging performance issues if you are having trouble meeting the 60fps requirement. 

**Controls**: To make grading easier, you should use these controls for the game:
* BTN2: Move the tank left. Hold down to move continuously.
* BTN1: Shoot a bullet. Only one bullet can be on the screen at a time. You can choose whether you can hold down to shoot a subsequent bullet or if you have to release and press again.
* BTN0: Move the tank right. Hold down to move continuously.

### Milestone 3 
<iframe width="500" height="350"
src="https://www.youtube.com/embed/V5XPFLa0Cdk?start=200">
</iframe>
Implement all of the game video, including bullets and all game interactions.  When you have finished this milestone, you will have the entire game implemented minus sound.  Use the above video as a reference.  It is difficult to see, but the number of points added to the score for each saucer destroyed is a number between 50 and 300, in multiples of 50. Also, the points for the block aliens are 10, 20 and 40, starting from the type on the bottom row and going up to the type on the top row.

The game should end if the aliens reach the bottom (either reaching the bunkers, tank, or bottom of the screen, your choice).  This is required for this milestone, but not Milestone 2.

**Note: You do not need to implement the high score screen.  Although this is shown in the video, it is not required for this lab this semester.**

Student often ask whether they can change the game in some way.  The answer is yes, you can make changes, provided they are stylistic and do not reduce the complexity of the game.  For example, the following would be permitted:
* Changing the colors of the aliens, bunkers, or ship.
* Changing the shape of the aliens, bunkers, or ship.
* Slight modifications to the speed of the game.

The following would not be permitted:
* Reducing the number of aliens, bunkers, or ships.
* Eliminating the bunker erosion patterns.
* Reducing the number of bullets that can be on the screen at once.

### Valgrind Check

On submission, your code will be checked with valgrind to ensure there are no reported issues.  Valgrind will be run with:
```
valgrind --leak-check=full  ./space_invaders
```
10% of your grade for this lab will be based on having no reported issues from valgrind.

## Submission 
Follow the submission instructions for each milestone on the [Submission]({% link _pages/submission.md %}) page.


## Resources 

### An Example Approach for Alien Bit-Map Data 

There are several ways to implement the bit-maps for your aliens. In the past, students have used editors to create bit-maps. Another approach is to create the bit-maps using a text editor. The code below will not compile but should give you a good idea of how to do this. There is more code further down that contains all of the bitmaps you will need for this lab in text form, as will be explained.

If you squint your eyes a bit, you should be able to see the shape of one of the aliens in the text below (the 1s are the bright pixels that form the alien). Carefully study what packWord32 does. Also, note that the 1's and 0's that form the alien are part of a 'C' array initialization. After thinking about this for a bit, you should be able to figure out how use this data structure to write the bit-map to the display.

```
const uint32_t sprite_alien_bottom_in_12x8[] =
{
	packWord12(0,0,0,0,1,1,1,1,0,0,0,0),
	packWord12(0,1,1,1,1,1,1,1,1,1,1,0),
	packWord12(1,1,1,1,1,1,1,1,1,1,1,1),
	packWord12(1,1,1,0,0,1,1,0,0,1,1,1),
	packWord12(1,1,1,1,1,1,1,1,1,1,1,1),
	packWord12(0,0,1,1,1,0,0,1,1,1,0,0),
	packWord12(0,1,1,0,0,1,1,0,0,1,1,0),
	packWord12(0,0,1,1,0,0,0,0,1,1,0,0)
};
```

One of the requirements is for the sprites to be scaled to be the same size as in the video.  Using this suggested implementation, it is easy to dynamically scale the sprites when they are being displayed.

### Alien Shapes Defined in C Code 

To save some time, we will give you the definitions of the aliens in their two guises, the spaceship, etc. These definitions are useful if you use the approach that was discussed above.

  * [sprites.c](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/apps/space_invaders/resources/sprites.c)
  * [sprites.h](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/apps/space_invaders/resources/sprites.h)

### Bunker Erosion Patterns 

 Take a look at the [sprites.c](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/apps/space_invaders/resources/sprites.c) file for erosion patterns. The corners of the bunkers should erode such that no pixels get set that weren't set before they started to erode.  So, although the erosion patterns are square in shape, the corners of the bunkers should erode within their original pixel constraints.
