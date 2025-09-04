---
layout: post
title:  "How can you cook your pasta fasta? :p"
date:   2025-04-15
image:  images/blog17/cover.jpeg
tags:  asyncio multithreading multiprocessing python parallelism pasta
---
*On the cover: A cute robot chef cooking pasta*

Concurrency in Python is like running a restaurant kitchen during a dinner rush — and if you're making pasta, you're bound to get a side of judgment from an Italian grandma every time you mess up.

Let’s walk through **asyncio**, **multithreading**, and **multiprocessing** — with veggies, pasta, and real code along the way.

## 1. Asyncio: One Chef, Smart Scheduling

You’ve got **one chef** in the kitchen.
He’s focused, fast, and organized. He can multitask if it's possible to do so. Example, when water's boiling or the oven’s preheating, he jumps over to another dish. But obviosuly he cannot chop several veggies at once.

It’s the classic **asyncio model**: non-blocking, efficient, and perfect when most of your time is spent **waiting on something**.

🔑 **Key Traits**:

* Single thread, single core
* Non-blocking, cooperative multitasking
* Great for I/O-bound tasks

### Example (Asyncio)

Consider this code:

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

# Not suitable for asyncio – CPU-bound work
def prepare_sauce(order_id):
    print(f"Order {order_id}: Preparing pasta sauce...")
    total = sum(i * i for i in range(10**7))
    print(f"Order {order_id}: Sauce ready.")

async def cook_pasta(order_id):
    await boil_pasta(order_id)
    chop_veggies(order_id)
    prepare_sauce(order_id)

async def restaurant():
    await asyncio.gather(
        cook_pasta(1),
        cook_pasta(2),
        cook_pasta(3),
    )

asyncio.run(restaurant())
```

Yes, we’re boiling three pastas at once — and no, we’re not adding olive oil to the water. Somewhere in Italy, a grandma just fainted.

But look at the blocking `chop_veggies` and `prepare_sauce` functions. They block the event loop (in this case the chef) and defeat the purpose of async. Even though three pastas are boiling simultaneously, the chef still has to chop veggies and prepare sauce one at a time. Every piece of code has to yield control back to event loop, otherwise it will block it completely.

Unless the chef can call his temporary assistants to help him with the veggies and sauce. That means the chef can assign the tasks to the assistants and they can chop veggies and prepare sauce in parallel.

```python
async def cook_pasta(order_id):
    await boil_pasta(order_id)
    await asyncio.to_thread(chop_veggies, order_id)
    await asyncio.to_thread(prepare_sauce, order_id)
```

Now, it is truly parallel. At this point, you might as well hire a bunch of chefs to help you run the restaurant. So asyncio is useful when you're boiling a thousand pastas and not worry about the veggies and sauce. One good use case is when you're crawling a large number of URLs. They are all I/O bound and can be run in parallel.


## 2. Multithreading: Multiple Chefs, One Kitchen

You hire **multiple chefs**, but they all work in the same cramped kitchen.

They can each work on something — one’s boiling pasta, another’s chopping veggies — but they bump into each other. Sometimes they fight over who gets to use the stove, and sometimes, someone just stands there holding a ladle, waiting.

That’s **multithreading** in Python. It works well when tasks are **I/O-bound**, but for CPU work, they still politely wait in line — thanks to the Global Interpreter Lock (GIL).

🔑 **Key Traits**:

* Shared memory space
* Limited by the Global Interpreter Lock (GIL)
* Useful for concurrent I/O

### Example (Multithreading)

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

def prepare_sauce(order_id):
    print(f"Order {order_id}: Preparing pasta sauce...")
    total = sum(i * i for i in range(10**7))
    print(f"Order {order_id}: Sauce ready.")

def cook_pasta(order_id):
    tasks = [
        threading.Thread(target=boil_pasta, args=(order_id,)),
        threading.Thread(target=chop_veggies, args=(order_id,)),
        threading.Thread(target=prepare_sauce, args=(order_id,)),
    ]
    return tasks

def restaurant():
    all_tasks = []
    for order_id in range(1, 4):
        all_tasks.extend(cook_pasta(order_id))
    for t in all_tasks:
        t.start()
    for t in all_tasks:
        t.join()

restaurant()
```

This is also the point where one of the chefs suggests breaking spaghetti to make it fit in the pot and boiling it faster. At this point, the Italian government places you on a watchlist.

---

## 3. Multiprocessing: Many Kitchens, True Parallelism

You finally go full Gordon Ramsay and open **multiple kitchens**, each with its own chef, tools, and stove.

They don’t talk to each other much, but each gets their job done in full parallel glory. No fighting over ladles or fridge space.

That’s **multiprocessing** — great for **CPU-bound** tasks, because every process runs on its own core.

🔑 **Key Traits**:

* True parallelism (one process per CPU core)
* High memory usage (each process is isolated)
* Slower inter-process communication

### Example (Multiprocessing)

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

def prepare_sauce(order_id):
    print(f"Order {order_id}: Preparing pasta sauce...")
    total = sum(i * i for i in range(10**7))
    print(f"Order {order_id}: Sauce ready.")

def cook_pasta(order_id):
    processes = [
        multiprocessing.Process(target=boil_pasta, args=(order_id,)),
        multiprocessing.Process(target=chop_veggies, args=(order_id,)),
        multiprocessing.Process(target=prepare_sauce, args=(order_id,)),
    ]
    return processes

def restaurant():
    all_processes = []
    for order_id in range(1, 4):
        all_processes.extend(cook_pasta(order_id))
    for p in all_processes:
        p.start()
    for p in all_processes:
        p.join()

restaurant()
```

Each chef now works completely independently here. So if one of them starts putting ketchup in carbonara, no one’s there to stop them. Italy loses another star in the Michelin sky.

Remember that multiprocessing is not a silver bullet. It has its own set of challenges, such as high memory usage and slower inter-process communication. If say the chefs want to exchange stuff like good knives and talk to each other, they have to move between kitchens losing time. In multiprocessing terms, they have to use some form of inter-process communication (IPC) like pipes, queues, or shared memory.

The worst use case for multiprocessing is when you have several IO-bound tasks and you try to run it in multiple processes. It's like hiring 1000 chefs to boil 1000 pastas. You're just making it worse for yourself as a restaurant owner.

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