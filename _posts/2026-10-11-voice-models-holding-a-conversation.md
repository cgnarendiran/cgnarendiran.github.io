---
layout: post
title:  "Voice Models - Press to Talk"
date:   2026-10-11 12:00:00
image:  images/blog45/cover.jpg
description: "A model that can hear and speak still cannot hold a conversation. The hard part is knowing when to start, and being willing to stop."
tags: [speech, llms, multimodal, audio-codecs, efficient-inference]
---

*On the cover: a sergeant at Fort Myer, Virginia, demonstrating a walkie-talkie in August 1942. The set carries one voice at a time, and a button on its side decides whose. [Public domain](https://commons.wikimedia.org/wiki/File:A_sergeant_at_Fort_Myer,_Virginia_demonstrates_a_%22walkie-talkie%22_in_the_field._August,_1942._(49750489543).jpg), via Wikimedia Commons.*

In the [last post](/blog/voice-models-sound-to-tokens/) we got a second of sound down to a hundred whole numbers, written in eight passes, cheap enough that a language model can read them and write them back. The student in the fifth row can finally take the concert down and sing it back.

So put that model on a phone call.

It waits for you to stop talking. You pause to think of the street name and it answers the half-sentence you were in the middle of. You say "no, wait, not that one" and it keeps going for twenty seconds, in a lovely voice, about the wrong thing.

Welcome to the era of **full-duplex speech**. This is the story of what it takes to talk and listen at the same time, and of how much of a conversation turns out to be about who is allowed to speak when.

One bit of vocabulary first, because the whole post hangs on it. Duplex is a word from telecoms, and it describes how many directions a line carries at once. **Half duplex** is one direction at a time, which is a walkie-talkie. **Full duplex** is both at once, which is a telephone.

I want you to sit in a call-taxi office in Chennai for a bit. A call taxi is one you book over the phone, and the dispatcher has two things on her desk. On her left is a radio base station with a handset, and fifty drivers out there on one channel. On her right is a telephone, which is how the customer reaches her. She moves between the two all shift, and they do not work the same way at all.

## Two instruments, two sets of manners

On the radio she can either talk or hear, never both. She holds the button down, says her piece, lets go and waits. The drivers do the same. Fifty people share one channel, so if two of them key up together, both get chopped into noise. The protocol exists for a reason: you say "over" because the other side has no other way to know you have finished.

The telephone asks nothing of her. She can say "mm-hm" while the customer is still describing the landmark near his building, and he can cut in while she reads the fare back. Nobody says "over" on a phone call, and nobody misses it.

Now the point of all this. Every voice assistant you have ever used is the radio. It is half duplex. The only difference is that nobody told you to say "over", so a program has to guess when you would have said it. That guess is most of what goes wrong.

## Three desks and a slip of paper

Start with how these things are actually put together, because almost everything in production still works this way.

A customer calls. The call-taker listens and writes the address on a slip of paper, which is **speech recognition (ASR)** turning sound into text. The slip goes to the manager, who decides which driver gets it, and that is the **language model**. The decision goes to the dispatcher, who reads it out over the radio, which is **text to speech (TTS)**. Three desks, one slip travelling between them. The whole arrangement is called a **cascade**.

![Four boxes in a row from the endpointer through ASR, LLM and TTS, above a bar chart adding 700, 300, 500 and 200 milliseconds](/images/blog45/cascade-latency.png) *Figure 1: the four stages and what they cost. The milliseconds are a typical budget rather than a measurement, and the 700 at the front is the part nobody expects. Source: Author*

Nobody keeps this design out of nostalgia. The slip of paper is a transcript, so you can log it, search it and show it to a regulator. And the manager can be the best text model money can rent, with tools and function calls that nobody has rebuilt for sound.

What it costs is time. The clock does not start when you finish your sentence. It starts when a program becomes convinced you have, and then runs through three more desks. In words, the time before you hear anything is the wait to be sure you stopped, plus the transcribing, plus the thinking, plus the speaking. Specifically,

$$T_{\text{first sound}} = t_{\text{end}} + t_{\text{asr}} + t_{\text{llm}} + t_{\text{tts}}$$

where $t_{\text{end}}$ is the silence waited out before your turn is called over, $t_{\text{asr}}$ is the wait for a final transcript, $t_{\text{llm}}$ is the time to the model's first word and $t_{\text{tts}}$ is the time to the first sound of it.

Let's do one by hand. Say the endpointer waits 700 ms, the recogniser takes 300 ms to commit, the model's first token comes back in 500 ms and the voice starts 200 ms after that. Add them: 1,700 ms before the first sound. Real budgets move around, but those four terms are always there and the first one is usually the largest.

Against what? [Stivers and ten co-authors](https://www.pnas.org/doi/10.1073/pnas.0903616106) timed conversations in ten languages in 2009, from Italian to Yélî Dnye, and found people answering each other with gaps around a fifth of a second. Languages differ, but within about 250 ms of each other. Divide 1,700 by 200 and the cascade is about eight of those gaps late. The slip of paper also only carries the words. Your sigh does not survive the trip to the manager's desk.

## The stopwatch on the desk

So what is that 700 ms at the front, and why is it the biggest number?

Two different jobs hide in there. **Voice activity detection (VAD)** asks whether there is speech in this 20 ms of audio at all, and it is cheap and old and works. **Endpointing** asks the harder question, which is whether you have finished your turn. The usual answer is a stopwatch: if the VAD says silence for 500 ms, call it your turn.

![Two speech waveforms with identical 500 millisecond gaps, one in the middle of a sentence and one at the end](/images/blog45/endpointing.png) *Figure 2: the same silence, twice. In the top lane the timer fires while she is still thinking of the street name. Source: Author*

So think about what that stopwatch is being asked to do. "I need a cab to ... Anna Nagar" has a pause in the middle of it. "I need a cab to Anna Nagar" has one at the end. Both pauses are 500 ms of nothing. The timer has one signal and two situations, so it has to be wrong somewhere. [Deepgram's analysis](https://deepgram.com/learn/turn-detection-voice-agents-silence-vad-semantic-models) ran the numbers on a 500 ms threshold. It sits out 56 to 60% of the pauses that happen mid-turn, which is what you want. It also fires on only 47 to 51% of the pauses that really were the end of a turn, and that second number is a coin flip wearing a config file. They are the vendor's own figures, so take them as the shape of the problem rather than as physics.

Push the timer up to 800 ms and the interruptions get rarer. [LiveKit](https://livekit.com/blog/turn-detection-voice-agents-vad-endpointing-model-based-detection) points out what you bought it with: nearly a second added to every single reply, including the ones where the user obviously finished. Nobody ran an ablation over 480 ms and 520 ms either. 500 is a round number somebody typed once, and a good chunk of the world's dead air is calibrated to it.

The fix that is winning is to stop listening to the silence and read the words instead. **Semantic VAD**, also called a turn detector, takes the transcript so far and asks a small model whether that was a finished thought. Deepgram claims its own model cuts false interruptions by about 30% and takes 200 to 600 ms off the response, again vendor-reported. The number is marketing and the idea is still right, because it is the first thing in the stack that uses what you said to decide whether you were done.

## Cutting in

The driver who hears "proceed to Besant Nagar" and keys up with "sir, that road is flooded" is doing something a stopwatch cannot help with. The dispatcher has to let go of her button to hear him. That is **barge-in**, and it is the thing people miss most when they first talk to a machine (watch anyone's face the first time one will not stop).

For an agent to notice you cutting in, the microphone has to stay open while the speaker is playing. Which means the microphone hears the speaker. On a laptop or in a car, its own voice comes back off the wall as the loudest thing in the room, a few milliseconds late and bent out of shape.

![A loop diagram where the agent's speech reaches the microphone through the room and an adaptive filter subtracts its guess at that echo](/images/blog45/echo-cancellation.png) *Figure 3: acoustic echo cancellation. The agent knows exactly what it played, which is the only advantage it has here. Source: Author*

**Acoustic echo cancellation (AEC)** is the fix, and it is older than any of this. The system knows the signal it sent to the speaker. So it learns a filter that predicts what that signal sounds like coming back, and subtracts it. In words, what the model listens to is what the microphone heard minus its best guess at its own voice. Specifically,

$$e(n) = d(n) - \sum_{k=0}^{L-1} \hat{h}_k\, x(n-k)$$

where $n$ counts audio samples, so at 16 kHz one step of $n$ is a sixteen-thousandth of a second. $x(n)$ is what was sent to the speaker and $d(n)$ is what the microphone picked up. The hat on $\hat{h}_k$ means a guess rather than a measurement: the filter's own estimate of the room's echo path, one number per sample of delay. $L$ is how far back the echo may reach, a couple of hundred milliseconds for a normal room, and $e(n)$ is what is left over.

Cancellers are graded in decibels of **echo return loss enhancement**, and thirty of them means a ratio of a thousand. So the agent's own voice comes back a thousandth of the power it arrived with, which sounds like plenty until you remember it started louder than you did.

Here is the part that matters for barge-in. The filter can only learn the room while exactly one side is talking, because with both going it cannot tell which part of the mixture to blame on itself. Both at once is called **double-talk**, and it is the single case the canceller cannot learn from. It is also, of course, the case you need it for. What ships is a compromise: a detector spots double-talk and freezes the filter while it lasts, so the room model coasts instead of learning nonsense. That works on a headset. On a speakerphone in a car it is why you sometimes say "stop" twice.

## Picking up the phone

Now the other instrument. What does a machine have to look like if it is built as a telephone from the start?

The first honest attempt was [dGSLM](https://arxiv.org/abs/2203.16502) (Meta, 2022). It takes two-channel audio, one channel per speaker, and models both at once with two stacks that read each other's working as they go. There is no text in it anywhere. Trained on 2,000 hours of telephone calls, it produces pauses, overlaps, laughter and backchannels (the "mm-hm" you make while the other person is still talking) with timing that sounds like a real conversation. It also talks absolute nonsense, because nothing in it was taught what words mean. The authors say so themselves. That is the useful part: turn-taking can be learnt from raw audio alone, and meaning cannot.

[Moshi](https://arxiv.org/abs/2410.00037) (Kyutai, 2024) is the one that put both halves together. Kyutai never explained the name as far as I can tell, and the story everyone tells is that moshi moshi is what you say in Japan when you pick up the phone. It runs on Mimi, the codec from part 1, which writes 12.5 frames a second with 8 codes in each. That is the hundred numbers a second from the first paragraph, and it makes one frame 80 ms long. Every 80 ms Moshi reads one frame of your audio and writes one frame of its own, and both streams run for the whole conversation.

![Three parallel token streams per frame feeding a large temporal transformer, with a zoom panel showing the order inside one frame](/images/blog45/moshi-streams.png) *Figure 4: one step per frame. The small transformer writes the text token first and the eight codes after it, which is why the words lead the voice. Source: Author*

A 7B Transformer called Helium takes one step per frame and carries the conversation. A much smaller Transformer then writes the tokens inside that frame in order, which is part 1's trick for not paying eight times over for eight codebooks. Then comes the third stream, which is the clever bit. Moshi predicts its own **text** for each frame before its own audio, aligned in time. The paper calls it the Inner Monologue, and it improves the linguistic quality of the speech by a lot. Lining them up also gives you streaming recognition and synthesis out of the same model for free.

So there are three streams in all. There is yours, which it only ever reads. Then its own audio and its own text, which it writes. In words, the model gives a probability to everything it writes in this frame: its text token, then each of its eight audio codes, conditioned on every frame before it and on yours. Specifically,

$$p(V) = \prod_{s=1}^{S} \prod_{k=1}^{K} p\left(v_{s,k} \mid v_{<s,\cdot},\, v_{s,<k}\right)$$

where $V$ is the whole conversation written out, $s$ is which 80 ms frame we are on and $S$ is how many of them the conversation has run for. $k$ is which of the $K = 9$ tokens inside the frame we are writing, in the order the figure shows: the text token, then the eight codes. $v_{s,k}$ is that one token, $v_{<s,\cdot}$ is everything from earlier frames, yours included, and $v_{s,<k}$ is what has already been written inside this frame.

That formula has no listening mode and no speaking mode in it, so there is no moment where anything decides your turn is over. The model writes a frame every 80 ms whatever is happening, and silence is one of the things it can write. So what stops it talking over you? Nothing explicit. When to start and when to shut up are learnt from recordings of people doing it, which is a fine idea until you look at what the recordings are. Moshi spends most of a conversation predicting silence twelve and a half times a second, which is a pretty expensive way to keep your mouth shut. It is also why it can come in half a beat after you stop.

![Two timelines, one with strict alternation and a gap, one with overlapping speech, a backchannel and a barge-in](/images/blog45/half-and-full-duplex.png) *Figure 5: the same half minute. The little empty boxes in the bottom lane are frames where the model predicted silence, which it has to do anyway. Source: Author*

The latency falls out of that design. One Mimi frame is 80 ms. Moshi writes its audio codes one frame behind its text on purpose, which adds another 80. So 160 ms in theory, and the authors measure about 200 ms on an L4, a mid-range datacentre GPU. That is inside the human range from Stivers, and about a tenth of the cascade budget we added up earlier.

Getting there took four stages. Seven million hours of English audio first, transcribed by [Whisper](https://arxiv.org/abs/2212.04356) large-v3, which is a machine copying another machine's homework with nobody reading it to check. Then two-channel data faked by pulling single-channel recordings apart into one track per speaker. Then fine-tuning on [Fisher](https://catalog.ldc.upenn.edu/LDC2004S13), a 2003 corpus of calls with each speaker on their own channel, which is where the duplex manners come from. Then instruction tuning on synthetic dialogues.

| Setup | What decides it is your turn | First sound | What it loses | Verdict |
|---|---|---|---|---|
| Cascade, silence timer | a stopwatch, 500 to 800 ms of quiet | about 1.5 to 2 s | your tone, and the first half of your sentence | ships today, everywhere |
| Cascade, semantic endpointer | a small model reading the transcript so far | a few hundred ms less | the same tone, fewer wrong guesses | the cheapest real fix |
| One model, speech in and speech out, still one turn each | still a timer, sitting outside the model | 232 ms at best, 320 ms typical (GPT-4o) | the transcript in the middle | fast, and still a walkie-talkie |
| Three streams, full duplex | nothing does; it writes silence or speech every 80 ms | 200 ms (Moshi) | tool calls and control, though its text stream is a transcript | right design, early days |

That third row is worth a line of its own. [GPT-4o](https://openai.com/index/hello-gpt-4o/) answers audio in as little as 232 ms, and 320 ms on average, against 2.8 s and 5.4 s for the cascaded Voice Mode it replaced. OpenAI's write-up says the old pipeline threw away tone, multiple speakers and background noise on the way through text. Deleting the slip of paper bought the speed, and it is also what the compliance team will ask you about.

Which raises the obvious question: if a half-duplex model already answers in 232 ms, what is the fourth row for? Speed is not what it buys. One turn each means the model is deaf while it speaks, so the decision to stop still comes from a VAD bolted on outside it. And it cannot say "mm-hm" at the right moment, because it has nowhere to put the sound. The fourth row buys the overlap itself, which a turn-based design has no slot for at any speed.

## Where things are going

- **The timer becomes a model.** Semantic endpointing is the one upgrade that helps a cascade without rebuilding it, and LiveKit and Deepgram both ship one.
- **Benchmarks that grade the interaction.** [Full-Duplex-Bench](https://arxiv.org/abs/2503.04721) (2025) scores pause handling, backchannels, turn-taking and interruptions. Version 1.5 adds overlapping speech, and version 2 runs whole conversations with an automated examiner.
- **Semi-cascaded hybrids.** Keep the text in the middle for the logs and the tools, and bolt a duplex controller on the front to do the listening. Most 2026 production systems are heading here rather than to one end-to-end model.
- **Cheaper listening.** A Transformer's cost grows with everything it has heard, and a duplex model hears all day at 12.5 frames a second. Which is the argument the [Mamba posts](/blog/mamba-is-attention-all-you-really-need/) made for architectures whose cost per step stays flat.

## Static on the line

The first thing I would push back on is the backchanneling. Full-Duplex-Bench puts Moshi's takeover rate on backchannels at 1.000, which is every single one the examiner throws at it. Say "mm-hm" while it is talking and it stops and answers you, as though you had interrupted. [Freeze-Omni](https://arxiv.org/abs/2411.00774) (Tencent, 2024) takes over on about 78% of them and almost never makes a backchannel of its own. So the models can generate overlap, and they cannot yet tell the two kinds apart: the kind that means "go on" and the kind that means "stop".

Then the data, which is worse than part 1's complaint about read-aloud English, because here the interaction itself is what is scarce. You cannot learn turn-taking from a single mixed channel, since you cannot tell who overlapped whom. So you need each speaker on their own channel. The big public source of that is Fisher: 11,699 calls and about 1,960 hours. They were recorded in 2003 from American strangers, put on the line by an automatic dialler and told what to talk about. Every full-duplex model you have spoken to learnt its manners there. No Indian English, no two people switching between Tamil and English mid-sentence, no call taken on a scooter at a signal. The gaps are not universal either, since Stivers's ten languages clustered tightly but not identically.

The field's answer to that shortage is to manufacture conversations. The [ICASSP 2026 HumDial challenge](https://arxiv.org/abs/2601.05564) built its dual-channel set by having professional actors perform scripts drafted by a language model, over 100 hours of it in Chinese and English. It is a reasonable thing to do and I would have done it too. It also means we grade models' conversations against a model's idea of a conversation, performed by people paid to sound natural.

And the cloning problem from part 1 gets a live wire attached to it here. Three seconds of audio was already enough to copy a voice. A duplex stack makes the copy interactive, so it can hold the pauses and come in on cue. The [FCC ruled in February 2024](https://www.fcc.gov/document/fcc-makes-ai-generated-voices-robocalls-illegal) that AI voices in robocalls fall under the existing ban on artificial and prerecorded messages, and Tennessee's ELVIS Act covers commercial voice replicas. Both are about using somebody's voice, and neither does much about a machine that sounds like a person on a call you did not expect.

My sourcing is the same as last time, and I will keep saying it. Both arXiv and Wikimedia are blocked from the machine I write these on, so the Moshi and dGSLM internals come from abstracts and write-ups rather than from the figures. The endpointing percentages are vendor-published and I cannot reproduce them. The numbers I would most like checked are Moshi's 200 ms on an L4 and the Full-Duplex-Bench takeover rates.

## Conclusion

Part 1 was about getting sound onto the page: a second of audio as a hundred numbers, cheap enough to put in a language model's mouth. None of that tells you when to open it.

The other half is a scheduling problem in an audio costume. A cascade is a radio channel with three desks behind it, and it spends its first 700 ms waiting to be sure you stopped. A full-duplex model never waits, because it writes a frame every 80 ms anyway and silence is one of the things it can write. The price is that it listens while it talks, so it hears itself. And that is why an echo canceller built for speakerphones sits underneath the newest thing in speech.

My bet is that the next real jump comes from the recordings rather than the model. What is missing is two-channel audio of people interrupting each other in more than two languages, labelled for which overlaps meant "go on" and which meant "stop". The models can already hold the line open. They just have terrible manners, which is what you get from learning them off 11,699 phone calls recorded in 2003.

So the dispatcher puts the radio handset down, and picks up the phone.

And now you know. Fin.
