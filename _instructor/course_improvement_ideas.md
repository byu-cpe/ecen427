# Course Improvement Ideas

Suggestions for new content in ECEn 427, based on a review of all lab writeups, the LDD/AXI study-question pages, the documentation pages, and the lecture slide decks (Sep 2026).

## The big picture

The course has an unusually strong hands-on spine (userspace UIO → char driver → sysfs platform driver → custom AXI hardware → DMA), but the reading list has conspicuous holes:

- LDD3 chapters 5, 7, and 8 are skipped entirely; Ch. 6 is ioctl-only; Ch. 10 stops right before top/bottom halves.
- Only 2 of ~50 OSTEP chapters are assigned (Ch. 2 and 4).
- As a result, **kernel concurrency, blocking I/O, deferred work, and kernel memory allocation are absent**, even though the labs walk right past all four.
- The HLS accelerator lab is fully written but hidden (`under_construction: true`).
- Students are quizzed on I2C/SPI but never touch either.

---

## Larger topics (with lab integration)

### 1. Concurrency and synchronization — the biggest gap

Students never see a lock, in kernel or userspace, all semester. Yet Lab 5's audio driver has a *real* race: the ISR and `write()` both touch the audio buffer, and the driver only works because a single-opener assumption is silently made.

**Integration:** Add LDD3 Ch. 5 as `ldd5.md` and OSTEP Ch. 26–29 readings. Then in Lab 5 M3/M4, require `spinlock_irqsave` around the shared buffer and an atomic open-count (grade by a test that hammers the device from two processes). On the userspace side, add a Space Invaders milestone (or Lab 3 variant) that moves sound or input polling onto a `pthread` with a mutex-protected queue — right now the whole game is single-threaded ISR-tick polling, which reinforces a pattern students will outgrow immediately in industry.

### 2. Blocking I/O and wait queues — close the loop students are already halfway through

In Lab 2 students *consume* blocking `read()` and `poll()` via UIO; they never *implement* the provider side. Lab 5 M3 currently has `read()` return a "still playing" flag, forcing the test app to busy-poll — the exact anti-pattern Lab 3 forbids.

**Integration:** Assign the rest of LDD3 Ch. 6 (wait queues, `poll`, `O_NONBLOCK`). Change Lab 5 M3 so `write()` of a new clip blocks on `wait_event_interruptible()` until playback finishes (ISR calls `wake_up()`), with `O_NONBLOCK` returning `-EAGAIN`, and implement `.poll`. This is a small code delta but teaches the single most important kernel pattern the course currently omits, and it makes the UIO behavior from Lab 2 stop being magic.

### 3. Boot process and building the system image

The PYNQ image is pre-built magic, `pynq.dts` is explicitly off-limits, and there's no coverage of FSBL, U-Boot, kernel config, or rootfs — arguably the most common real-world embedded Linux task. The pipeline that produces the class image is invisible to students.

**Integration:** Lightest: one lecture + a "trace the boot" homework over the serial console (read U-Boot output, inspect `BOOT.BIN`, kernel cmdline, `/proc/device-tree`, systemd targets). Fuller: a 1-week lab (could replace the shelved self-directed lab slot) where students build the image with PetaLinux or Buildroot and boot their own kernel — this would also finally let them modify the base device tree rather than only overlays.

### 4. Kernel-side DMA and `mmap()` — upgrade Lab 8's own critique

Lab 8's writeup already tells students userspace DMA is "a massive security vulnerability" — a perfect setup with no payoff. Similarly, students do `open`/`lseek`/`write` on the HDMI framebuffer at 921 KB/frame but never see how a driver could hand them a zero-copy mapping.

**Integration:** Add a Lab 8 M2 (or extra credit) that moves the CDMA into a kernel driver using `dma_alloc_coherent()` and the DMA API, exposed via ioctl — teaching physical/virtual/bus addresses and cache coherency (the Zynq HP-vs-ACP port story) properly. Alternatively or additionally, have students implement `.mmap` in a driver so the game blits directly into the framebuffer, and measure the syscall-count improvement with the `strace` harness Lab 4 already built.

### 5. Restore the HLS accelerator lab (or an AXI-master trajectory)

The only hardware students design is an AXI-Lite *slave*; the polished HLS lab (AXI master, Vitis, latency/resource tradeoffs) is hidden. Hardware acceleration is where the industry — and every ML-on-edge job posting — is going. If the 8-lab schedule is full, offer it as extra credit or the capstone alternative to Lab 8; the writeup mostly needs its stale links fixed (`copy_bitmap_region` vs `fill_bitmap_region`, wrong header path).

### 6. Debugging and observability beyond `printk`

The course's stated philosophy is self-reliance, but the only debugging tools taught are `printk`/`dmesg` and `valgrind`. One lecture plus threaded requirements would pay off in every lab: cross-`gdb` with `gdbserver` for the game, `ftrace`/`trace_events` for watching their own ISR fire in Lab 5, `perf` for the Lab 4 benchmarking milestone (replacing "guess why drawSprite is slow" with actual profiles).

---

## Smaller topics (≤ 1 lecture each)

### Kernel / OS

1. Deferred work: top/bottom halves, threaded IRQs, workqueues (the explicit cut in the ldd10 reading)
2. Kernel memory allocation: `kmalloc` vs `vmalloc`, GFP flags (LDD3 Ch. 8)
3. Kernel timers, jiffies, hrtimers — natural companion to the PIT labs ("how does the kernel do what your PIT does?")
4. `devm_*` managed resources — modernizes Lab 5's goto-unwinding and shows current kernel idiom vs LDD3's 2005 style
5. The Linux device model: kobjects, buses, udev internals (students already use udev rules blindly)
6. Comparing kernel↔user interfaces: `/dev` vs ioctl vs sysfs vs debugfs vs netlink — a unifying lecture after Labs 5 and 7 where they've built two of them
7. Virtual memory and the MMU: page tables, TLB, what `mmap`/`ioremap` actually do — de-magics UIO
8. Scheduling: CFS, nice, `SCHED_FIFO`/`chrt` — directly relevant to Lab 4's "no missed 16.67 ms frames" requirement
9. What makes Linux (not) real-time: PREEMPT_RT, interrupt latency, `cyclictest`
10. Signals and graceful shutdown — the game should clean up the screen and audio on Ctrl+C
11. IPC survey: pipes, Unix sockets, POSIX shared memory
12. The `/proc` filesystem as a diagnostic toolbox (`/proc/interrupts` appears in ldd10 but is never explored)
13. Kernel module licensing, GPL, and in-tree vs out-of-tree drivers

### Tools & software engineering

14. Cross-debugging with `gdb`/`gdbserver` (if not part of the larger observability unit)
15. Linkers and ELF: static vs dynamic linking, `ldd`, sysroots — students cross-compile all semester without knowing what the toolchain does
16. Unit testing in C/C++ (GoogleTest/Unity) + hardware-in-the-loop tests; students never write a test, only run provided ones
17. Real Git workflow: branching, PRs, code review — even the team lab uses Git purely as a submission mechanism; one review cycle in Lab 4 would be cheap and valuable
18. GitHub Actions CI beyond `.commitdate`: build + clang-format + clang-tidy on every push (infrastructure already half-exists)
19. AddressSanitizer/UBSan as fast alternatives to valgrind
20. `strace`/`ltrace` formal lecture — Lab 4 grades on syscall counts but nothing teaches the tool

### C/C++

21. RAII and smart pointers — the C++ deck teaches raw `delete`; `unique_ptr` for `GameObject`s is a one-lecture upgrade
22. `virtual`, polymorphism, and vtables — the deck shows inheritance for the game class hierarchy but never `virtual`, which students will need the moment they store `GameObject*`s heterogeneously
23. Endianness, alignment, and packed structs — students hit this in the WAVE parser, framebuffer packing, and DMA descriptor alignment with no supporting lecture
24. `errno` and POSIX error-handling conventions (vs kernel `-ERRNO` returns they see in Lab 5 — the symmetry is teachable)

### Hardware / peripherals

25. Hands-on I2C: `i2c-tools`/`/dev/i2c` to poke the ADAU1761 codec — converts the quiz-only I2C/SPI page into a 1-hour exercise and de-magics the provided `audio_config_init()`
26. UART internals — students use the serial console daily without ever learning the peripheral
27. AXI-Stream and the video pipeline (VDMA, VTC) — explains the HDMI hardware they've been writing to all semester
28. Clock-domain crossing beyond the synchronizer paper: async FIFOs, handshake CDC — bridges the metastability reading to the multi-clock reality visible in the block design
29. Watchdog timers and embedded reliability patterns (brownout, safe-state design)
30. Embedded security: secure boot, TrustZone on Zynq, why `/dev/mem` and userspace DMA are dangerous — Lab 8's writeup already opens this door
31. Investigate Versal: what comes after Zynq — AMD's Versal adaptive SoC (hard NoC, AI Engines, Arm A72/R5 processing system, programmable logic) and how the PS/PL boundary, address map, and Linux bring-up compare to the Zynq-7000 students use all semester

### Lab 1 lecture companions (pair with the cross-compilation toolchain lecture)

32. Why the ARM binary won't run on your x86 workstation but the same source compiles for both — ISAs, ELF headers, exploring binaries with `file`/`readelf`/`ldd`
33. Anatomy of the SD card image: use `lsblk`, `fdisk -l`, `df` to inspect the partitions — boot partition vs rootfs, what filesystem is used, what `dd` actually wrote

### Other additions

34. udev: how `/dev/ecen427/*` gets its stable names — uevents, rule matching, writing a udev rule; students rely on the class udev rules in Lab 2 without ever seeing them (narrower, hands-on slice of #5's device-model lecture)

### Combinations that compound

- #4 + #6 modernize Lab 5.
- #8 + #9 give Lab 4's frame-deadline requirement a theoretical backbone.
- #25 turns dead quiz material into hands-on work.
