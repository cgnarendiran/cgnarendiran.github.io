---
layout: post
title:  "How fast can you cook with your CPUs?"
date:   2025-04-15
image:  images/blog17/cover.jpg
tags:  asyncio multithreading multiprocessing
---
*On the cover: Boiling pasta fasta*

Concurrency in Python is like running a restaurant kitchen during a dinner rush — and if you're making pasta, you're bound to get a side of judgment from an Italian grandma every time you mess up.

Let’s walk through **asyncio**, **multithreading**, and **multiprocessing** — with veggies, pasta, and real code along the way.

---

## 1. Asyncio: One Chef, Smart Scheduling

You’ve got **one chef** in the kitchen.
He’s focused, fast, and organized. He doesn’t multitask in the traditional sense. When water's boiling or the oven’s preheating, he jumps over to another dish.

It’s the classic **asyncio model**: non-blocking, efficient, and perfect when most of your time is spent **waiting on something**.

🔑 **Key Traits**:

* Single thread, single core
* Non-blocking, cooperative multitasking
* Great for I/O-bound tasks

### ✅ Example (Asyncio)

```python
import asyncio

async def boil_pasta(order_id):
    print(f"Order {order_id}: Boiling pasta (30s)...")
    await asyncio.sleep(30)
    print(f"Order {order_id}: Pasta ready!")

# Not suitable for asyncio – CPU-bound work
def chop_veggies(order_id):
    print(f"Order {order_id}: Chopping veggies...")
    total = sum(i * i for i in range(10**7))
    print(f"Order {order_id}: Veggies chopped.")

def cook_pasta(order_id):
    print(f"Order {order_id}: Cooking pasta sauce...")
    total = sum(i * i for i in range(10**7))
    print(f"Order {order_id}: Sauce ready.")

async def main():
    await asyncio.gather(
        boil_pasta(1),
        boil_pasta(2),
        boil_pasta(3),
    )

asyncio.run(main())
```

🧀 **Chef’s note**:
Yes, we’re boiling three pastas at once — and no, we’re not adding olive oil to the water. Somewhere in Italy, a grandma just fainted.

**Note**: The CPU-heavy `chop_veggies` and `cook_pasta` should not be run inside asyncio — they block the event loop and defeat the purpose of async.


## 2. Multithreading: Multiple Chefs, One Kitchen

You hire **multiple chefs**, but they all work in the same cramped kitchen.

They can each work on something — one’s boiling pasta, another’s chopping veggies — but they bump into each other. Sometimes they fight over who gets to use the stove, and sometimes, someone just stands there holding a ladle, waiting.

That’s **multithreading** in Python. It works well when tasks are **I/O-bound**, but for CPU work, they still politely wait in line — thanks to the GIL.

🔑 **Key Traits**:

* Shared memory space
* Limited by the Global Interpreter Lock (GIL)
* Still useful for concurrent I/O

### ✅ Example (Multithreading)

```python
import threading
import time

def boil_pasta(order_id):
    print(f"Order {order_id}: Boiling pasta (30s)...")
    time.sleep(30)
    print(f"Order {order_id}: Pasta ready!")

def chop_veggies(order_id):
    print(f"Order {order_id}: Chopping veggies...")
    total = sum(i * i for i in range(10**7))
    print(f"Order {order_id}: Veggies chopped.")

def cook_pasta(order_id):
    print(f"Order {order_id}: Cooking pasta sauce...")
    total = sum(i * i for i in range(10**7))
    print(f"Order {order_id}: Sauce ready.")

tasks = [
    threading.Thread(target=boil_pasta, args=(1,)),
    threading.Thread(target=boil_pasta, args=(2,)),
    threading.Thread(target=chop_veggies, args=(1,)),
    threading.Thread(target=cook_pasta, args=(1,))
]

for t in tasks:
    t.start()
for t in tasks:
    t.join()
```

🍝 **Cultural footnote**:
This is also the point where someone suggests breaking spaghetti to make it fit in the pot faster. At this point, the Italian government places you on a watchlist.

---

## 3. Multiprocessing: Many Kitchens, True Parallelism

You finally go full Gordon Ramsay and open **multiple kitchens**, each with its own chef, tools, and stove.

They don’t talk to each other much, but each gets their job done in full parallel glory. No fighting over ladles or fridge space.

That’s **multiprocessing** — great for **CPU-bound** tasks, because every process runs on its own core.

🔑 **Key Traits**:

* True parallelism (one process per CPU core)
* High memory usage (each process is isolated)
* Slower inter-process communication

### ✅ Example (Multiprocessing)

```python
import multiprocessing
import time

def boil_pasta(order_id):
    print(f"Order {order_id}: Boiling pasta (30s)...")
    time.sleep(30)
    print(f"Order {order_id}: Pasta ready!")

def chop_veggies(order_id):
    print(f"Order {order_id}: Chopping veggies...")
    total = sum(i * i for i in range(10**7))
    print(f"Order {order_id}: Veggies chopped.")

def cook_pasta(order_id):
    print(f"Order {order_id}: Cooking pasta sauce...")
    total = sum(i * i for i in range(10**7))
    print(f"Order {order_id}: Sauce ready.")

if __name__ == "__main__":
    tasks = [
        multiprocessing.Process(target=boil_pasta, args=(1,)),
        multiprocessing.Process(target=boil_pasta, args=(2,)),
        multiprocessing.Process(target=chop_veggies, args=(1,)),
        multiprocessing.Process(target=cook_pasta, args=(1,))
    ]

    for p in tasks:
        p.start()
    for p in tasks:
        p.join()
```

🍷 **Warning**:
Each chef works completely independently here. So if one of them starts putting ketchup in carbonara, no one’s there to stop them. Italy loses another star in the Michelin sky.

---

## TL;DR – Which Kitchen Setup Should You Use?

| Model               | Kitchen Metaphor                | Best For  | Avoid When                     |
| ------------------- | ------------------------------- | --------- | ------------------------------ |
| **Asyncio**         | 1 chef, smart task juggler      | I/O-bound | CPU-heavy work                 |
| **Multithreading**  | Many chefs, one crowded kitchen | I/O-bound | Heavy CPU + shared memory bugs |
| **Multiprocessing** | Many chefs, many kitchens       | CPU-bound | Data sharing, high memory use  |


Concurrency in Python is about making the most of what you’ve got — chefs, stoves, and time.

* If you're mostly **waiting on things** (I/O), let one chef juggle tasks smartly with `asyncio`.
* If you've got **lots of waiting**, and can tolerate a bit of stepping on toes, go `multithreading`.
* If your tasks are **CPU-heavy**, unleash a team of chefs in separate kitchens with `multiprocessing`.

And remember:
**Never break the spaghetti. Ever.**

Fin.