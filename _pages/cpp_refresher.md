---
layout: page
toc: true
title: C++ Refresher for Space Invaders
short_title: C++ Refresher
---

Space Invaders ([Lab 4]({% link _labs/space_invaders.md %})) is the first lab where you write a large amount of C++.  You have seen all of this C++ before in CS 235 and CS 240, but for most students it has been a year or more, and the labs so far have been in C.  Work through this page before you start the lab; plan on about an hour.

The lab comes with a set of class headers that lay out one design for the game.  **Using those headers is completely optional**: you may build on them, modify them, or write everything from scratch.  This page uses them as examples because they show each C++ feature in context, but the features themselves are ones you will need whichever way you build the game.

**Budget:** about 50 minutes of video, plus a few short readings.  Each topic below tells you what to look for in the provided headers, gives one short video, and a written alternative if you would rather read.  The videos are from The Cherno's C++ series, which is aimed at exactly this level: you already know how to program, and want a fast, correct picture of one C++ feature at a time.  The readings are from [learncpp.com](https://www.learncpp.com/), which is the best free written reference for this material.

Skim the [provided headers](https://github.com/byu-cpe/ecen427_student/tree/main/userspace/apps/space_invaders) first, even if you do not plan to use them, then go through the topics in order.  If a topic is still fresh for you, skip its video and just read the notes.

## References vs. Pointers

**Where you will see it:** [Graphics.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Graphics.h) takes a `Sprites &sprites` in its constructor and stores it as a reference member.  `main.cpp` does `Graphics &graphics = Globals::getGraphics();`.  Everything else, such as the `Sprite *` and `Alien *` members, is a plain pointer, and `nullptr` is used for "no object".

* Video: [REFERENCES in C++](https://www.youtube.com/watch?v=IzoFn3dfsPA) (10 min)
* Reading: [Lvalue references](https://www.learncpp.com/cpp-tutorial/lvalue-references/)

A reference is an alias for an existing object; a pointer stores an address.

```c++
int x = 10;
int &r = x;    // reference: must be initialized, can never refer to anything else
int *p = &x;   // pointer: can be null, can be reassigned

r = 20;        // modifies x
*p = 30;       // modifies x
```

Use references for parameters when the object must exist and you do not need to reseat it.  Use pointers when "no object" is a valid value, or when you own something allocated with `new`.

## Constructors and Member Initializer Lists

**Where you will see it:** [Aliens.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Aliens.h), [Tank.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Tank.h) and [UFO.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/UFO.h) have `const` members such as `const uint32_t moveTickMax;`.  Graphics has a reference member.  Neither kind can be assigned in the constructor body; they must be initialized in the constructor's initializer list, or the code will not compile.  [Lives.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Lives.h) shows the syntax: `Lives() : numLives(LIVES_AT_START) {}`.

* Video: [Member Initializer Lists in C++](https://www.youtube.com/watch?v=1nfuYMXjZsA) (9 min)
* Reading: [Constructor member initializer lists](https://www.learncpp.com/cpp-tutorial/constructor-member-initializer-lists/)

```c++
class Foo {
  int &ref;
  const int max;

public:
  Foo(int &x, int m) : ref(x), max(m) {}   // the only place these can be set
};
```

Members are initialized in the order they are declared in the class, not the order in the initializer list.  The compiler warns about a mismatch, and you are graded on having no warnings.

## Inheritance

**Where you will see it:** [GameObject.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/GameObject.h) is the base class for everything drawn on screen.  Alien, Bullet, Bunker, BunkerBlock, Tank and UFO all say `class X : public GameObject`, and each constructor comment says "Make sure this calls the parent constructor."  The base class keeps `x`, `y` and `sprite` as `protected` so subclasses can use them.  [Bullet.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Bullet.h) declares its own `kill()` and tells you to call the parent's `kill()` from it.

* Video: [Inheritance in C++](https://www.youtube.com/watch?v=X8nYM8wdNRE) (8 min)
* Reading: [Constructors and initialization of derived classes](https://www.learncpp.com/cpp-tutorial/constructors-and-initialization-of-derived-classes/) and [Calling inherited functions and overriding behavior](https://www.learncpp.com/cpp-tutorial/calling-inherited-functions-and-overriding-behavior/)

```c++
class Base {
public:
  Base(int x) {}
  void f() {}
};

class Derived : public Base {
public:
  Derived() : Base(42) {}   // the base constructor is called from the initializer list
  void g() { Base::f(); }   // calling a base class function by name
};
```

Two things to notice.  The base constructor is called in the initializer list, alongside your own members.  And when a subclass declares a function with the same name as one in the base class (Bullet's `kill()`), the subclass version hides the base version; you call the base version explicitly with `GameObject::kill()`.  None of the provided headers use `virtual`; if you want to know what that would change, the optional video at the bottom of this page covers it.

## STL Containers and Iterating

**Where you will see it:** [Aliens.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Aliens.h) stores `std::vector<std::vector<Alien *>>`, a vector of rows.  [Bullets.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Bullets.h) keeps the enemy bullets in a `std::list<Bullet *>`, and its `kill()` must remove one from the middle.  [Lives.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Lives.h) and [Bunker.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Bunker.h) hold vectors of objects.  [Sprites.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Sprites.h) uses `std::map` to look sprites up by an enum.

* Video: [Dynamic Arrays in C++ (std::vector)](https://www.youtube.com/watch?v=PocJ5jXv8No) (14 min)
* Reading: [Sequence containers](https://hackingcpp.com/cpp/std/sequence_containers.html) on hackingcpp, a visual cheat sheet for `std::vector` and `std::list` and when to prefer each; and [Range-based for loops](https://www.learncpp.com/cpp-tutorial/range-based-for-loops-for-each/) on learncpp.

`std::vector` is a contiguous array: fast indexing and iteration, fast `push_back`, slow to insert or erase in the middle.  `std::list` is a doubly linked list: no indexing, but erasing anywhere is cheap and does not disturb other iterators.  `std::map` is a sorted key-to-value dictionary.

Range-based for loops are the normal way to walk a container:

```c++
std::vector<int> v = {1, 2, 3};
for (int x : v) { ... }          // by value
for (auto &x : v) { ... }        // by reference, if you need to modify

std::map<std::string, int> m;
for (const auto &[key, value] : m) { ... }
```

**Erasing while iterating** is the one thing here that catches almost everyone, and Bullets needs it.  You cannot erase inside a range-based for loop; the loop's hidden iterator is invalidated and the behavior is undefined.  Use an explicit iterator and let `erase()` hand you the next one:

```c++
std::list<Bullet *> bullets;

for (auto it = bullets.begin(); it != bullets.end(); ) {
  if ((*it)->isDead()) {
    delete *it;                  // if the list owns the objects
    it = bullets.erase(it);      // erase returns the iterator to the next element
  } else {
    ++it;
  }
}
```

The same pattern works for `std::vector`.  If you want the details of why, [std::vector::erase](https://en.cppreference.com/w/cpp/container/vector/erase) and [std::list::erase](https://en.cppreference.com/w/cpp/container/list/erase) on cppreference each have an example loop and state exactly which iterators are invalidated.

## Static Members and the Globals Singleton

**Where you will see it:** [Globals.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Globals.h) is a class you never instantiate (`Globals() = delete;`).  It has only static functions, each holding one game-wide object in a function-local static.  [Colors.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Colors.h) is a class of `static const constexpr` constants, and [Score.h](https://github.com/byu-cpe/ecen427_student/blob/main/userspace/apps/space_invaders/Score.h) has a static helper, `padScore()`.

* Video: [Static for Classes and Structs in C++](https://www.youtube.com/watch?v=V-BFlMrBtqQ) (9 min)
* Reading: [Static member functions](https://www.learncpp.com/cpp-tutorial/static-member-functions/) and [Static local variables](https://www.learncpp.com/cpp-tutorial/static-local-variables/)

Games have a lot of global state.  Rather than scatter global variables through the program, the provided code puts each one behind a static accessor:

```c++
class Globals {
public:
  static Graphics &getGraphics() {
    static Graphics g;    // constructed the first time this function runs, lives until exit
    return g;
  }
};

Globals::getGraphics().fillScreen(Colors::BLACK);   // called on the class, not an object
```

This is called Meyers' singleton.  The function-local static is initialized on first use, so there is exactly one Graphics and its construction order relative to other globals is never a problem.  Any code in the game can reach the sprites, graphics, bullets, score and lives through Globals.

## Quick Reminders

No video needed for these, but look for them in the headers.

* **Forward declarations.**  Many headers say `class Sprite;` or `class Tank;` instead of including the header.  That is enough to declare a pointer or reference to the class, and keeps headers from including each other in a cycle.  Your `.cpp` file must include the real header before it calls any method on the object.  [Forward declarations to reduce compile-time dependencies](https://arne-mertz.de/2018/03/forward-declarations/) explains it in a few paragraphs.
* **Header and .cpp split.**  The headers declare the class; you define the functions in the matching `.cpp` as `void Alien::moveLeft() { ... }`.  Small functions defined inside the class body in the header, such as `getX()`, are already done.  See [Classes and header files](https://www.learncpp.com/cpp-tutorial/classes-and-header-files/) if this is fuzzy.
* **`new` and `delete`.**  Bullets are created with `new` when fired and must be deleted when killed; Sprites has a destructor that frees what its constructor allocated.  Every `new` needs exactly one `delete`, and your code will be [checked with valgrind]({% link _documentation/valgrind.md %}) for leaks.  Optional video: [The NEW Keyword in C++](https://www.youtube.com/watch?v=NUZdUSqsCs4) (11 min).
* **Enums.**  The headers use C-style `typedef enum { ... } name_t;`, sometimes nested inside a class (Tank's `tank_state_t`).  An enum nested in a class is referred to from outside as `Tank::tank_state_t`.
* **Overloading and default arguments.**  Graphics has two `drawSprite()` functions that differ only in their parameters; Tank and Bullet each have two constructors.  Audio's `playSound(std::string name, bool loop = false)` has a default argument.
* **`std::string`.**  Graphics draws `std::string` values.  Use `.length()` for the character count and `str[i]` for a character; `std::to_string(n)` converts a number.

## If You Want More

Optional, in rough order of usefulness for this lab.  All are from the same series.

* [Virtual Functions in C++](https://www.youtube.com/watch?v=oIV2KchSyGQ) (7 min): what the provided headers chose not to use, and why `Bullet::kill()` hiding `GameObject::kill()` is not the same thing.
* [Local Static in C++](https://www.youtube.com/watch?v=f7mtWD9GdJ4) (8 min): the mechanism behind Globals.
* [Constructors in C++](https://www.youtube.com/watch?v=FXhALMsHwEY) (7 min) and [Destructors in C++](https://www.youtube.com/watch?v=D8cWquReFqw) (5 min)
* [Visibility in C++](https://www.youtube.com/watch?v=6OVQ8nh3KP0) (9 min): public, private and protected.
* [CONST in C++](https://www.youtube.com/watch?v=4fJBrditnJU) (13 min)
* [ENUMS in C++](https://www.youtube.com/watch?v=x55jfOd5PEE) (8 min)
* [C++ Header Files](https://www.youtube.com/watch?v=9RJTQmK0YPI) (15 min)
* [ITERATORS in C++](https://www.youtube.com/watch?v=SgcHcbQ0RCQ) (17 min)
* [Introduction to iterators](https://www.learncpp.com/cpp-tutorial/introduction-to-iterators/) on learncpp, if you would rather read.
