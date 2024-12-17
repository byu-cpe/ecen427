---
layout: lab
toc: true
title: "Lab 4: Space Invaders (No Sound)"
short_title: Space Invaders
number: 4
under_construction: true

---

## Graphics

### Verifying BOOT using HDMI
The PYNQ video signal comes from the HDMI port labeled *HDMI Out* located on the topside of the board. This should already be connected to a dedicated monitor in the lab.  If you work remotely, you will need to find an HDMI-compatible display to use.  

<!-- As we are not using a lab room this year, you must provide your own display and HDMI cable (nothing fancy). We have tested the PYNQ board and found that it works correctly with just about any computer monitor and most TVs (though not all).  -->

You can verify that your PYNQ board is imaged correctly, and connected to the display correctly by powering it on, and after it has booted (about 1 min), you should see something like this on your display:

<img src = "{% link media/setup/pynqdisplaytestimage.jpg %}" width="400">



## Objective
Write the software that implements all video functionality for Space Invaders. Your game should closely mirror the game shown in the video below.

## Team Git Repository 

This is the only lab where you will be permitted to work in a team.  Your team will be three students.  The teams are pre-set and are listed on Learning Suite.  If two teams mutually agree, you may swap team members.  Do this before proceeding with the next step.


You will use a shared repository for this lab, and then return to working in your private repository for the remainder of the labs.  Once you have your team arranged, follow this link to create a new shared Github repository for lab 3: <https://classroom.github.com/a/cRunbQEp>
  * The first team member to sign up should create a new team name.
  * The other team members can join the team created by the first team member.
  * Once you have a team repository created, each member of the team needs to complete the Learning Suite quiz to indicate their team repository URL.

Once your empty lab 3 repository is created, you will need to import one of your team member's individual repository, into your shared repository. You can choose which member of team's code to use, but **all team members must have submitted lab3 before you share your code**.

You can do this in a similar manner to how you obtained the starter code:

        git clone --bare git@github.com:<team member's repo>.git
        cd <team member's repo>.git/
        git push --mirror git@github.com:byu-ecen427-classroom/<your team repo>.git
        cd ..
        rm -rf <team member's repo>.git


## Implementation

### Milestone 1

<iframe width="500" height="350"
src="https://www.youtube.com/embed/V5XPFLa0Cdk?start=200">
</iframe>


Complete the end scenario for space invaders. See the video above for details on how it should function (fast forward the video to 3:20). Note that the video says the high score screen can be in any pattern or configuration, meaning you can have as many rows or columns of scores as you like and the button API can be however you would like to implement it, as long as it matches the video's functionality. However, it is required that the high scores are presented in sorted order from highest score to lowest and that at least two text sizes are used. Refer to the [HDMI]({% link _documentation/hdmi.md %}) page for documentation on how to interact with the hdmi driver.

*Note:* To make it easier for the TAs to grade this, you should commit an existing high scores file into your repository.  Make sure not to use absolute file paths when opening the high-scores file, as the paths will likely be different on the TA's grading system.  You should also not rely on your space invaders executable being run from any particular directory.  Instead, access your high scores file  using a path relative to the space-invaders executable. [Stack overflow](https://stackoverflow.com/a/933996/609215) has a good explanation of how to do this with the `readlink` function.



### Milestone 2 

<iframe width="500" height="350"
src="https://www.youtube.com/embed/kGd4K0jBjis">
</iframe>

Implement all of the game video except for bullets and collisions.  Tanks should move, aliens should march, etc.  Use the video above as a reference. Keep in mind that when an entire column of aliens is gone from the edge the remaining aliens keep marching to the edge of the screen, past where the would have stopped if the edge aliens were alive. This feature doesn't need to be functional for this milestone, but keep it in mind for the next milestone.

### Milestone 3 
<iframe width="500" height="350"
src="https://www.youtube.com/embed/V5XPFLa0Cdk?start=200">
</iframe>
Implement all of the game video, including bullets and all game interactions.  When you have finished this milestone, you will have the entire game implemented minus sound.  Use the above video as a reference.  
It is difficult to see, but the number of points added to the score for each saucer destroyed is a number between 50 and 300, in multiples of 50. Also, the points for the block aliens are 10, 20 and 40, starting from the type on the bottom row and going up to the type on the top row.

## Suggestions 
<!-- Unlike previous courses, in this course you are given quite a bit of freedom regarding your implementation strategy.  However, you must work within these requirements:
  - You must adhere to the coding standard.  
    * Since header files are usually provided to you, students often forget about the coding standard rules regarding header files.  Be sure to review Rule 2.1.  
    * You will find it easier to follow this rule if you only put items in your header files that *need to be used by other .c files*.  If a #define, struct, etc. is only used in one .c file, it should be placed at the top of that .c file, and NOT in a header file.  This is good C coding practice and you should make a habit of following it when designing your own software structure. -->
  - You may find it helpful to use state machines as you learned in ECEn 330 and ECEn 390. Your game loop could consist primarily of calls to tick functions for your state machines. 

## Submission 
Follow the submission instructions for each milestone on the [Submission]({% link _other/submission.md %}) page.


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

The patterns for the bunker erosions are depicted in this pdf file. By studying this file and watching some of the provided game videos, you should be able to figure out how to code the bunker erosions. If you watch the game carefully, you will see that the bunkers are composed of blocks that go through predictable patterns as they are hit with bullets.  Take a look at the [sprites.c](https://github.com/byu-cpe/ecen427_student/blob/master/userspace/apps/space_invaders/resources/sprites.c) file for erosion patterns.

The corners of the bunkers should erode such that no pixels get set that weren't set before they started to erode.  So, although the erosion patterns are square in shape, the corners of the bunkers should erode within their original pixel constraints.
