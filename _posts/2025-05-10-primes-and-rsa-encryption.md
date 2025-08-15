---
layout: post
title:  "Prime Numbers to Padlocks - RSA Encryption and SSH"
date:   2025-05-10
image:  images/blog18/cover.webp
tags:  primes rsa encryption python
---
*On the cover: RSA Encryption*

If you’ve ever shopped online, sent a private message, or connected to a secure website, you’ve probably used RSA encryption without even knowing it. RSA is one of the most famous cryptographic systems, and what makes it magical is this:

> You can tell the whole world how to lock a message for you,
> but only you can unlock it.

This blog is a beginner-friendly walk-through of **how** that’s possible, why we don’t just share our secret key, and why a couple of prime numbers hold the entire system together.

---

## **The Padlock Story (Simon Singh’s analogy)**

Imagine you want to send me a secret message by mail.

1. I send you an **open padlock** — but **keep the key** with me.
2. You put your message in a box, lock it with my padlock, and send it back.
3. Because the box is locked, **only I** (who have the key) can open it.

The magic is:

* You never got my private key.
* Anyone can lock a box for me, but no one else can open it.

RSA works on the **same idea**, except the padlock is just a **big number** called **n**, and the way to lock something is using a public number **e**.

---

## **The Ingredients**

1. **Two large prime numbers**: $p$ and $q$
   (We keep these secret.)
2. **Their product**: $n = p \times q$
   (This is the “padlock” — we give this to everyone.)
3. **Totient**: $\varphi(n) = (p-1) \times (q-1)$
   (This is used for building the key.)
4. **Public exponent**: $e$

   * A small number that’s coprime to $\varphi(n)$ — often 3, 17, or 65537.
   * This is the “how to lock the box” number.
   * We give out **both $n$ and $e$** to the world.
     This is totally safe — knowing $n$ and $e$ doesn’t help anyone find $p$ and $q$ if they’re large enough.

---

## **Why We Give Out e (and n)**

If we didn’t give $e$, people wouldn’t know *how* to lock messages for us.

Think of $n$ as the shape of the padlock, and $e$ as the turning method.
Both are needed to lock something, but **only the person with $d$** (the private key) can reverse it.

Mathematically:

* Public key = $(e, n)$
* Private key = $(d, n)$
* $d$ is computed from $e$ and $\varphi(n)$ using the modular inverse:

  $$
  e \times d \equiv 1 \ (\text{mod} \ \varphi(n))
  $$

---

## **The Math Magic**

1. **Encryption** (locking the box):

   $$
   C \equiv M^e \ (\text{mod} \ n)
   $$

   Where:

   * $M$ is your message (as a number),
   * $C$ is the encrypted message.

2. **Decryption** (unlocking the box):

   $$
   M \equiv C^d \ (\text{mod} \ n)
   $$

   This works because of **Euler’s theorem**:
   If $\gcd(M, n) = 1$, then:

   $$
   M^{\varphi(n)} \equiv 1 \ (\text{mod} \ n)
   $$

   and we choose $e$ and $d$ so that $e \times d \equiv 1 \ (\text{mod} \ \varphi(n))$.

---

## **A Small Example (for humans)**

Let’s pick tiny numbers (not secure at all):

* $p = 5$, $q = 11$
* $n = 55$
* $\varphi(n) = (5-1) \times (11-1) = 4 \times 10 = 40$
* Pick $e = 3$ (coprime to 40)
* Find $d$ such that $3d \equiv 1 \ (\text{mod} \ 40)$ → $d = 27$

Public key: $(e=3, n=55)$
Private key: $(d=27, n=55)$

Say we want to encrypt $M = 12$:

* **Encrypt**: $C = 12^3 \ \text{mod} \ 55 = 1728 \ \text{mod} \ 55 = 23$
* **Decrypt**: $M = 23^{27} \ \text{mod} \ 55 = 12$ ✅

---

## **Why it’s secure**

If someone knows $n$ and $e$:

* They can encrypt messages to you.
* But they can’t easily find $d$ without knowing $\varphi(n)$.
* And to get $\varphi(n)$, they must factor $n$ into $p$ and $q$.
* With large enough primes (hundreds of digits long), factoring is practically impossible with today’s computers.

---

## **Final Thoughts**

RSA is a beautiful mix of:

* Simple number theory,
* Clever key sharing,
* And hard computational problems.

Simon Singh’s padlock analogy nails the intuition, but the real magic is in how $e$ and $d$ are linked by $\varphi(n)$, while $n$ acts as the public padlock.

Next time you see “🔒” in your browser, remember: somewhere, giant primes are keeping your secrets safe.

Fin.