---
layout: page
toc: false
title: Fourteen Ways to Fool Your Synchronizer
---
Please read this paper: [Fourteen Ways to Fool Your Synchronizer]({% link media/fourteenwaystofoolyoursynchronizer.pdf %})
Study Questions

1. When is it OK to use a 1-FF synchronizer?
1. Why is it a bad idea to place synchronizer FFs on data signals?
1. What is the term, T, in the MTBF equation on the first page?
1. What is a reasonable amount of time for T, if latency is not an issue?
1. How does the number of synchronizers in a product affect reliability?
1. How is the use of 2 FFs, wired closely in series to create a synchronizer related to the value of T?


## Notes:

1. When the paper refers to “bundled data” in Section 2, it is referring to the idea that the data wires are treated as a “bundle”, i.e., all of the bits on the data-wires need not have the same delay as long as the values will arrive by some worst-case timing specification, usually dictated by the slowest wire in the bundle. The two-flop synchronizer described in Figures 1 and 2 is based upon this assumption.
1. You can only mitigate metastability. It cannot be completely eliminated from any digital system. However, with proper design you can lower the likelihood of metastability so that it is negligible.