---
layout: page
toc: false
title: Linux Device Drivers, Chapter 4
---

## Reading

Pages Debugging by Printing (75-82), Debugging System Faults (93-98).  Also read about the *dev_\** and *pr_\** functions (<https://www.kernel.org/doc/html/latest/process/coding-style.html#printing-kernel-messages> (only Section 13) and <https://lwn.net/Articles/487437/>). 

## Study Questions

1. How do you classify messages with printk?

2. (T or F) There is a comma between the log-level and the message.

3. (T or F) Changing the log-level of the console can change what messages are displayed.

4. (T or F) You can use dmesg to read console messages.

5. (T or F) printk writes messages into a stack.

6. (T or F) dmesg prints out only the most recent message written to the console.

7. (T or F) You can modify the size of the buffer used with printk.

8. How does printk_ratelimit work?

9. How can you use Oops messages to determine where in your code the problem is located?

10. When should you use the *dev_\** and *pr_\** functions?