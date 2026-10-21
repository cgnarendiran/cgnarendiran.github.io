---
layout: post
title:  "DeepSeek-OCR - Ninety-Eight Pages on a Postcard"
date:   2026-10-21
image:  images/blog48/cover.jpg
description: "A page costs a model about ten times fewer tokens as a picture of itself than as text, and at that reduction it still reads back 97% of the characters."
tags: [document-understanding, multimodal, deepseek, efficient-inference, vision-language-models]
---

*On the cover: a microfiche, seven rows of fourteen frames, ninety-eight newspaper pages photographed onto one card at twenty-four to one. Drawn rather than found, because Wikimedia Commons is blocked from the machine I write these on. Source: Author.*

Somebody hands you a sheet of film the size of a postcard. On it, in seven rows of fourteen, sit ninety-eight pages of a newspaper, each photographed and shrunk to about four millimetres across. A whole Tuesday is in your hand and it weighs nothing.

Now read it.

You can't, obviously. Hold it up to the window and you get ninety-eight grey smudges in a grid, like a chessboard left out in the rain. Useless to your eye, perfectly fine to a machine with a lamp and a lens. Somebody worked out in the 1930s that the cheapest way to store words was to stop storing words and store a picture of them.

Welcome to the era of **optical context compression**. This is the story of a 2025 paper that asked whether a language model should read a page or just look at it, and of what survives when you keep shrinking the picture.

## What a page costs to read

A language model does not see characters. It sees tokens, which are the chunks a [tokenizer](/blog/tokenizers-bpe/) chops your text into. For English prose a token is about four characters, so a dense A4 page comes to around a thousand tokens. Everything the model is holding at once, your question plus everything it has already read, is its **context**. A thousand tokens a page sounds pretty cheap until you want a few thousand pages in there.

And the cost does not grow politely. Attention compares every token with every other token, so doubling the context quadruples the work. That is the whole reason [KV caching](/blog/kv-caching-mla-is-attention-all-you-really-need/) exists. Ten thousand pages is ten million tokens, and the attention matrix for that has 10^14 entries. Nobody is renting that much memory to read a filing cabinet.

So here is the question the paper starts from. What if you did not give the model the words at all? What if you rendered the page as an image, the way a scanner would, and handed over the picture?

You might think that is obviously worse, and for a while it was. Chop a 1024 by 1024 image into little squares of 16 by 16 pixels, the way a [ViT](/blog/vit-pixels-to-tokens/) does, and hand each square over as one token. There are 4,096 of them in the page, which is four times what the text cost. A thousand tokens of writing has become four thousand tokens of picture of writing, which is a pretty expensive way to achieve nothing.

The number that has to come down is 4,096.

![Two tracks: a page going through a tokenizer to 1,000 text tokens, and the same page photographed and encoded to 100 vision tokens, both feeding one decoder](/images/blog48/two-ways-in.png) *Figure 1: the same page, two ways in. The 10x gap is the paper's headline claim and the 97% is the round number it quotes for that band, not any single row of its table. The per-setting numbers are further down and they are less tidy. Source: Author*

## Twenty-four to one

The people who built microfilm bureaus had a good word for this ratio. **Reduction ratio**: how many times smaller the image is than the thing it photographed. A newspaper went onto film at 24:1, the standard the [ANSI/AIIM microfiche spec](https://nvlpubs.nist.gov/nistpubs/Legacy/FIPS/fipspub54-1-Jan17.pdf) was written around. The industry even bands the ratios by name: up to 15:1 low, 15 to 30 normal, 30 to 60 high, 60 to 90 very high. Past 90:1 you are making ultrafiche, and nothing up there is standardised at all, because almost nobody went there.

I want you to remember those bands, because this whole paper lives inside the first two.

One caveat first. A film reduction is linear, so 24:1 shrank each side 24 times and the area about 576. The ratio below is a count over a count, so this is borrowed vocabulary and not a comparison.

The quantity we care about is the same ratio, counted in tokens. In words it is what the page would have cost as text, divided by what the picture of it costs,

$$\frac{\text{what the page costs as words}}{\text{what the picture of the page costs}}$$

specifically,

$$r = \frac{N_{\text{text}}}{N_{\text{vision}}}$$

where $N_{\text{text}}$ is the number of text tokens the page would have been chopped into, and $N_{\text{vision}}$ is the number of vision tokens the encoder emits for the image of it. A ratio of 10 means ten tokens' worth of cost bought for one. At four characters a token, that is each vision token carrying about forty characters of page. The paper chasing this is [DeepSeek-OCR: Contexts Optical Compression](https://arxiv.org/abs/2510.18234) (Wei, Sun and Li, DeepSeek-AI, October 2025), and it is really a measurement of how far you can push $r$ before the page stops coming back.

## The camera they had to build

Nobody had measured this properly because of the encoder. An **encoder** is the part that turns a picture into tokens. And the existing ones are all bad at exactly the thing you need here, which is keeping the token count down on a big page. Three families, three problems:

1. **Dual-tower** encoders like [Vary](https://arxiv.org/abs/2312.06109) run two vision models side by side, and need a second image pipeline to feed them.
2. **Tile-based** encoders like the [InternVL](https://arxiv.org/abs/2404.16821) line cut the page into squares and encode each one alone. A sentence crossing a tile boundary is never seen whole.
3. **Adaptive-resolution** encoders like [Qwen2-VL](https://arxiv.org/abs/2409.12191) keep the page's native shape. Lovely for a photograph, ruinous for a newspaper, because the token count climbs with the page.

So DeepSeek built their own, called **DeepEncoder**, three pieces in a row. First comes [SAM](https://arxiv.org/abs/2304.02643)-base (80M parameters), the Meta model trained to cut objects out of photographs. It runs **window attention**, so each square only looks at its own small neighbourhood. That stays cheap at 4,096 tokens precisely because nothing looks far. Then a convolutional compressor: two layers sliding a 3 by 3 window across the grid in steps of 2, each halving the grid both ways, so the pair squeeze 16 tokens into 1. Then [CLIP](https://arxiv.org/abs/2103.00020)-large (300M parameters), OpenAI's image-and-text model, running **global attention**, where every token does see every other one. That is the expensive piece, and it only runs after the count has dropped.

Let's do the arithmetic by hand, because it comes out exact and that almost never happens.

Take a Base-mode page at 1024 by 1024 pixels. Patch it at 16 by 16 and you get 64 patches per side, so $64 \times 64 = 4{,}096$ patch tokens. Now the compressor: two convolutions at stride 2 halve each side twice, so 64 becomes 32 and then 16. That is $16 \times 16 = 256$ tokens going into CLIP. In general,

$$N_{\text{vision}} = \frac{H}{16} \cdot \frac{W}{16} \cdot \frac{1}{16} = \frac{HW}{4096}$$

where $H$ and $W$ are the image height and width in pixels. The first two sixteens are the patch size in each direction. The third is the compressor, which is 4 in each direction and so 16 over the grid. The same 16 three times over. That is either disciplined engineering or somebody's favourite number, and I am not going to pretend I can tell which.

The order of those three pieces is the whole design. Global attention over 4,096 tokens means building a 4,096 by 4,096 table of comparisons and holding it in GPU memory. Over 256 tokens that table is 256 times smaller and costs almost nothing. So the compressor does two jobs that want the same thing. It lets CLIP afford the whole page, and the 256 tokens it leaves are the same 256 the decoder pays for.

![DeepEncoder as four boxes: patchify, SAM with window attention over 4096 tokens, a 16x convolutional compressor, CLIP with global attention over 256 tokens, with a zoom panel on the compressor](/images/blog48/deepencoder.png) *Figure 2: blue looks only at its own corner, orange looks at the whole page, and the green box between them is what makes the orange one affordable. The zoom is the squeeze itself: a 4 by 4 block of patch tokens in, one token out, 256 times over. Source: Author*

## Five settings on the dial

Once the encoder exists, the reduction ratio is just an input resolution you pick. Four fixed modes, plus a tiling one:

| Mode | Resolution | Vision tokens | What it is for |
|---|---|---|---|
| Tiny | 512² | 64 | a slide or a receipt, anything with big type |
| Small | 640² | 100 | a book page; the one the paper leans on |
| Base | 1024² | 256 | a dense paper, padded square |
| Large | 1280² | 400 | small print and footnotes |
| Gundam | n×640² tiles + one 1024² view | n×100 + 256, n from 2 to 9 | a newspaper spread, where one view will not do |

Tiny and Small just resize the image, so a tall page gets squashed and the type with it. Base and Large pad it out to a square instead, which keeps the letters the right shape. You pay for the blank margin either way, because the formula only counts pixels. Gundam does both. It tiles the page for the small print and keeps one whole-page view for the layout, so the model can tell a two-column spread from a one-column one. The authors never say where the name comes from, and the usual story is the mecha anime, where the suit is a frame with panels bolted on. Take that as the usual story.

## The machine upstairs

The thing reading the fiche is a **DeepSeek3B-MoE** decoder. It holds about 3B parameters but does not run them all at once. The model is cut into groups called experts. A small router picks a few per token and leaves the rest off, so roughly 570M parameters do the work on any one. That is the [mixture-of-experts](/blog/moe-is-attention-all-you-really-need/) trick of keeping a big model and paying for a small one.

And this is not an OCR engine in the old sense, which matters for every number below. An old OCR engine looks at a glyph, decides it is an "e", and moves on. This thing is a language model handed some blurry evidence. It does not identify characters. It writes the most likely page, given what it can make out.

That is why the curve further down bends instead of falling off a cliff. Blur a word and a glyph classifier returns garbage, while a language model fills in whatever fits. It is also why the failure mode is unpleasant: when it cannot read a word, it does not tell you. It writes a plausible one, in the right font, in the right place.

## Where the grain wins

So how far can you actually push the dial? The paper tests it on [Fox](https://arxiv.org/abs/2405.14295), a document benchmark, on 100 English pages carrying 600 to 1,300 text tokens each. Fox ships the real text of each page, so the score is the fraction of characters the model got right against it. The paper calls that precision.

| Vision tokens | Text on the page | Reduction | Precision | What that means for you |
|---|---|---|---|---|
| 100 | 600-700 tokens | ~6.7x | 98.5% | one wrong character in 67, a slip or two a paragraph |
| 64 | ~670 tokens | ~10.5x | 96.5% | one in 29, two or three per line of this post |
| 100 | 1200-1300 tokens | ~12.6x | 87.1% | one in 8; you would notice inside a sentence |
| 64 | ~960 tokens | ~15x | 85.8% | one in 7, and the layout starts drifting too |
| 64 | 1200-1300 tokens | ~20x | 59.1% | two characters in five are invented |

That last row is the ablation, which means moving one knob and leaving everything else alone to see what the knob was worth. And it is the punchline of the paper. Look at rows two and five. Same weights, and the same 64 vision tokens off the same 512 by 512 square. The one thing that moved is how much text got crammed into that square, about 670 tokens against about 1,250. So each vision token goes from carrying roughly 42 characters to roughly 80, and 96.5% becomes 59.1%. At that point the model is writing fan fiction about a document it half saw, confidently, in Times New Roman.

A microfilm bureau would shrug at that table, since their silver grain held up fine at ratios of that size. The grain here is the patch, 16 pixels on a side. On row two a patch has two or three characters in it. On row five it has about five, and the compressor folds sixteen patches into one token regardless. Somewhere in between, the letters stop being separable and no amount of language modelling gets them back.

![Precision against compression ratio for 64 and 100 vision tokens, falling from 98.5% at 6.7x to 59.1% at 20x, with the microfilm reduction bands shaded behind](/images/blog48/fox-compression-curve.png) *Figure 3: the same curve the table describes. The shaded bands are the microfilm industry's names for ratios of that size, borrowed as vocabulary rather than as a measurement, since their ratio is linear and this one is a count. Source: Author*

## What it beats, and on how little

The compression study is the interesting half. The half that got the attention was the OCR, because the model is small and it wins anyway.

The scoreboard is [OmniDocBench](https://arxiv.org/abs/2412.07626), a document-parsing benchmark graded by edit distance. That counts the single-character fixes needed to turn the output into the truth and then divides by the length, so 0 is perfect and lower is better. DeepSeek-OCR beats [GOT-OCR2.0](https://arxiv.org/abs/2409.01704), the previous small-model favourite, on 100 vision tokens a page against its 256. And it beats [MinerU2.0](https://arxiv.org/abs/2409.18839), a full document-parsing pipeline that averages over 6,000 tokens a page, while staying under 800, which means it is running in Gundam mode with a handful of tiles.

The training set is 30M PDF pages scraped off the internet in about 100 languages, 25M of them Chinese and English. Training ran on 160 A100-40G cards, Nvidia's 2020 datacentre part.

And then the throughput, the number I keep thinking about. One A100-40G chews through over 200,000 pages a day, and the paper puts the full 160-card cluster at 33 million. The [British Newspaper Archive](https://www.britishnewspaperarchive.co.uk/) has been going since 2010 and is somewhere past 100 million pages. This model would read the lot in three days, on hardware you can rent by the hour. And I am genuinely unsure whether that is a triumph or just a different kind of sad.

## Shrinking the old pages on purpose

Now the idea the paper is really fishing for.

If precision degrades smoothly with resolution, then resolution is a dial you can turn *during* a conversation. Keep the last few exchanges at 1280 by 1280. Re-render the ones from an hour ago at 1024, yesterday's at 640, last week's at 512. Older context takes less room and comes back less exactly, which is a fair description of what your own memory does with last Tuesday.

The nice part is the framing, because the blur stops being a defect and becomes the mechanism. We already treat "far away" and "hard to make out" as the same fact about the world, and a model could too.

![The same paragraph rendered four times at falling resolutions from 1280 down to 512, each one blurrier than the last](/images/blog48/optical-forgetting.png) *Figure 4: optical forgetting, drawn with only the model's four real native modes so the ratios are honest. A demonstration of what the resolution drop does to a paragraph, not output from DeepSeek-OCR. Source: Author*

Nobody has shipped this. The paper calls it a direction rather than a result, draws the picture, and leaves it there. It is not free either, since every step down the dial means rendering and encoding that stretch again. Survivable on old context you demote on a schedule. Not survivable if something keeps changing, which is the complaint two sections down.

## Where things are going

- **[Glyph](https://arxiv.org/abs/2510.17800) (Zhipu, 2025)** renders long text into images and trains a vision-language model on them. About 3.3x average compression on [LongBench](https://arxiv.org/abs/2308.14508), a long-context test suite, and it reads its input up to 4.8x faster. Lower ratios than DeepSeek's, but measured on reasoning rather than character recovery.
- **Context Cascade Compression** ([2511.15244](https://arxiv.org/abs/2511.15244)) reports 93% at 40x by cascading two language models and skipping pixels entirely, and **DeepSeek-OCR 2** ([2601.20552](https://arxiv.org/abs/2601.20552)) reports 0.100 edit distance on OmniDocBench v1.5 against the original's 0.129. I have read neither set of tables, so both are single-sourced.
- **Token pruning**, like [RTPrune](https://arxiv.org/abs/2605.00392), drops the vision tokens the decoder turns out not to need, since a page of mostly margin should not cost what a page of equations costs.

## The double fold test

In December 2025, three researchers published [Optical Context Compression Is Just (Bad) Autoencoding](https://arxiv.org/abs/2512.03643) (Lee, Yang and Berg-Kirkpatrick). They held the decoder and the training data fixed, and swapped the vision encoder for two dumber things. One was a learned hierarchical encoder. The other was mean pooling. Every token is already a list of numbers inside the model, so mean pooling slides a window along and averages each group into one. It is the sort of baseline you write in an afternoon. On reconstruction, both matched or beat the vision encoder at every compression ratio. Then they gave each the same token budget and asked the model to carry on writing. On that test the vision route did about as well as truncation, which means binning the old context and replacing it with nothing. That is the uncomfortable part, because getting 97% of the characters back is not the same as being able to use them. A page you can transcribe and cannot reason over is worth roughly what deleting it was worth. On the evidence I have seen, their conclusion that the excitement is running ahead of it is right.

Then there is what the format cannot do. Text tokens are addressable, so you can cache the first half of a document and append to it. A rendered page is not addressable. Change one sentence and you re-render and re-encode the whole image it sits on, so the [KV cache](/blog/kv-caching-mla-is-attention-all-you-really-need/) reuse that makes long chats affordable stops working at the page boundary. Nobody has shown how editing is supposed to work here, and I do not think it is a small problem.

The measurement is thinner than the headline too. Fox here is 100 English pages. Chinese ought to be where this pays most, because a character carries more meaning per token, and that case I have not seen measured. Write-ups also quote 96.5%, 96.8% and 97.3% for the same 10x result. And I have been rounding to 97% all post, so I am part of that problem.

And my usual caveat, which is getting tiresome to type. Both arXiv and Wikimedia are blocked from the machine I write these on, so every number here comes from published tables as they appear in search results and write-ups, not from the PDFs. The ones I would most like checked are the five Fox rows and the 570M activated-parameter figure.

American libraries spent fifty years microfilming newspapers and throwing away the bound originals. The justification was the **double fold test**: fold a corner of a page back and forth until it tears, and if it fails early the paper is brittle and the volume may go. Nicholson Baker took that apart in [Double Fold](https://en.wikipedia.org/wiki/Double_Fold) (2001). The test was a poor measure of whether a book was dying, and the film was often worse than what it replaced. The institutions ran a cheap test, believed it, and binned the originals. I am not saying optical compression is that. I am saying 97% is a number off a 100-page benchmark, and nobody should be deleting their text on the strength of it yet.

## Conclusion

Ninety-eight pages on a postcard, and you cannot read a word of it without the machine. Microfilm offered that deal and this offers the same one. You give up direct access to the words, you get the storage back, and a lamp and a lens sit between you and your own archive from then on.

What DeepSeek actually built is a vision encoder designed from the start to be stingy with tokens, plus a measurement of how far that stinginess goes. Ten times fewer tokens buys about 97% of your characters. Twenty times buys 59%, which is to say a document that looks right and isn't. And then a near-parameterless average turned up and matched the whole thing, which either kills an idea or sharpens it.

My bet is that the compression framing fades and the encoder survives. Every long-document model will need something that holds its token count flat as the page gets bigger, and DeepEncoder is the first built for that deliberately rather than by accident. The forgetting idea I find lovely and would not build on yet, because for now it is a figure in a paper and a curve that bends the right way.

But keep the bound volumes. The last lot who trusted a reduction ratio and threw out the originals have been apologising for it for twenty years.

And now you know. Fin.
