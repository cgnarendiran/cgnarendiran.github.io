---
layout: post
title:  "DeepSeek-OCR - Ninety-Eight Pages on a Postcard"
date:   2026-10-21
image:  images/blog48/cover.jpg
description: "A page costs a model about ten times fewer tokens as a picture of itself than as text, and at that reduction it still reads back 97% of the characters."
tags: [document-understanding, multimodal, deepseek, efficient-inference, vision-language-models]
---

*On the cover: a microfiche. One sheet of film, 105 by 148 millimetres, seven rows of fourteen frames, with ninety-eight pages of a newspaper photographed onto it at a reduction of twenty-four to one. Drawn rather than photographed, because Wikimedia Commons is blocked from the machine I write these on. Source: Author.*

Somebody hands you a sheet of film about the size of a postcard. On it, in seven rows of fourteen, sit ninety-eight pages of a newspaper. Each page has been photographed and shrunk until it is roughly four millimetres across. A whole Tuesday is in your hand and it weighs nothing.

Now read it.

You can't, obviously. Hold it up to the window and you get ninety-eight grey smudges in a grid, like a chessboard left out in the rain. The card is useless to your eye and perfectly fine to a machine with a lamp and a lens. That trade is the whole product. Somebody worked out in the 1930s that the cheapest way to store words was to stop storing words and store a picture of them instead.

Welcome to the era of **optical context compression**. This is the story of a 2025 paper that asked whether a language model should read a page or just look at it, and of what survives when you keep shrinking the picture.

## What a page costs to read

A language model does not see characters. It sees tokens, which are the chunks a [tokenizer](/blog/tokenizers-bpe/) chops your text into. For English prose a token is about four characters, so a dense A4 page of a paper comes to somewhere around a thousand tokens. That sounds pretty cheap until you want the model to hold a few thousand pages at once.

And the cost does not grow politely. Attention compares every token with every other token. So doubling the context quadruples the work, which is the whole reason [KV caching and MLA](/blog/kv-caching-mla-is-attention-all-you-really-need/) exist. Ten thousand pages is ten million tokens, and the attention matrix for that has 10^14 entries in it. Nobody is renting that much memory to read a filing cabinet.

So here is the question the paper starts from. What if you did not give the model the words at all? What if you rendered the page as an image, the way a scanner would, and handed over the picture?

You might think that is obviously worse, and for a while it was. Chop a 1024 by 1024 image into 16 by 16 pixel patches, the way a [ViT](/blog/vit-pixels-to-tokens/) does, and you get 4,096 patch tokens out of one page. That is four times what the text cost. You have taken a thousand tokens of writing and turned it into four thousand tokens of picture of writing, which is a pretty expensive way to achieve nothing.

The number that has to come down is 4,096.

![Two tracks: a page going through a tokenizer to 1,000 text tokens, and the same page photographed and encoded to 100 vision tokens, both feeding one decoder](/images/blog48/two-ways-in.png) *Figure 1: the same page, two ways in. The 10x gap at the bottom is the claim, and the 97% is what the paper says comes back out. Source: Author*

## Twenty-four to one

The people who built microfilm bureaus had a word for this ratio and it is a good one. **Reduction ratio**: how many times smaller the image is than the thing it photographed. A newspaper went onto film at 24:1, which is the standard the [ANSI/AIIM microfiche spec](https://nvlpubs.nist.gov/nistpubs/Legacy/FIPS/fipspub54-1-Jan17.pdf) was written around. The industry even bands the ratios by name. Up to 15:1 is low reduction. From 15:1 to 30:1 is normal. Past 90:1 you are making ultrafiche, and at that point nothing is standardised any more, because almost nobody ever went there.

I want you to remember those bands, because this whole paper lives inside the first two.

The quantity we care about is the same ratio, counted in tokens. In words it is what the page would have cost as text, divided by what the picture of it costs,

$$\frac{\text{what the page costs as words}}{\text{what the picture of the page costs}}$$

specifically,

$$r = \frac{N_{\text{text}}}{N_{\text{vision}}}$$

where $N_{\text{text}}$ is the number of text tokens the page would have been chopped into, and $N_{\text{vision}}$ is the number of vision tokens the encoder emits for the image of it. A ratio of 10 means ten words' worth of cost bought for one. The paper chasing this is [DeepSeek-OCR: Contexts Optical Compression](https://arxiv.org/abs/2510.18234) (Wei, Sun and Li, DeepSeek-AI, October 2025), and the name undersells it. It is filed as an OCR model, and it is really a measurement of how far you can push $r$ before the page stops coming back.

## The camera they had to build

Nobody had measured this properly because the existing vision encoders are all bad at exactly the thing you need here, which is keeping the token count down on a big image. Three families, three problems:

1. **Dual-tower** encoders like [Vary](https://arxiv.org/abs/2312.06109) run two separate vision models side by side, and add a whole second image preprocessing pipeline to do it.
2. **Tile-based** encoders like the [InternVL](https://arxiv.org/abs/2404.16821) line cut the page into squares and encode each one at low resolution. So a sentence that crosses a tile boundary gets split between two experts who never speak.
3. **Adaptive-resolution** encoders like [Qwen2-VL](https://arxiv.org/abs/2409.12191) keep the page's native shape, which is lovely for a photograph and ruinous for a newspaper, because the token count climbs with the page.

So DeepSeek built their own, called **DeepEncoder**, and it is three pieces in a row. First comes [SAM](https://arxiv.org/abs/2304.02643)-base (80M parameters), Meta's segmentation backbone, running **window attention**, which means each patch only looks at its own small neighbourhood. That stays cheap at 4,096 tokens precisely because nothing is looking far. Then a convolutional compressor, two layers with a 3 by 3 kernel and stride 2, which squeezes 16 patch tokens into 1. Then [CLIP](https://arxiv.org/abs/2103.00020)-large (300M parameters), OpenAI's image-and-text model, running **global attention**, where every token does see every other token. That is the expensive one, and it only runs after the count has already dropped.

Let's do the arithmetic by hand, because it comes out exact and that almost never happens.

Take a Base-mode page at 1024 by 1024 pixels. Patch it at 16 by 16 and you get 64 patches per side, so $64 \times 64 = 4{,}096$ patch tokens. Now the compressor: two convolutions at stride 2 halve each side twice, so 64 becomes 32 and then 16. That is $16 \times 16 = 256$ tokens going into CLIP. In general,

$$N_{\text{vision}} = \frac{H}{16} \cdot \frac{W}{16} \cdot \frac{1}{16} = \frac{HW}{4096}$$

where $H$ and $W$ are the image height and width in pixels, the first two sixteens are the patch size, and the third is the compressor's factor. The same 16 three times over. That is either disciplined engineering or somebody's favourite number, and I am not going to pretend I can tell which.

The order of those three pieces is the whole design. Global attention over 4,096 tokens is what blows up your activation memory, because the thing it builds is 4,096 by 4,096 entries wide. Global attention over 256 tokens costs almost nothing. So the compressor exists so that CLIP can afford to look at the whole page at once, and saving the decoder some work is a side effect.

![DeepEncoder as four boxes: patchify, SAM with window attention over 4096 tokens, a 16x convolutional compressor, CLIP with global attention over 256 tokens, with a zoom panel on the compressor](/images/blog48/deepencoder.png) *Figure 2: blue looks only at its own corner, orange looks at the whole page, and the green box in between is what makes the orange one affordable. The zoom shows the actual squeeze: 16 patch tokens in, 1 token of 256 numbers out, done 256 times over. Source: Author*

## Five settings on the dial

Once the encoder exists, the reduction ratio is just an input resolution you pick. Four fixed modes, plus a tiling one:

| Mode | Resolution | Vision tokens | What it is for |
|---|---|---|---|
| Tiny | 512² | 64 | a slide, a receipt, anything with big type |
| Small | 640² | 100 | a book page; this is the one the paper leans on |
| Base | 1024² | 256 | a dense paper, padded to keep the aspect ratio |
| Large | 1280² | 400 | small print and footnotes |
| Gundam | n×640² tiles + one 1024² view | n×100 + 256, n from 2 to 9 | a newspaper spread, where one view is not enough |

Tiny and Small just resize the image. Base and Large pad it instead, so a tall page does not get squashed into a square. Gundam is the interesting one, because it does both. It tiles the page for the small print and keeps one whole-page view for the layout, so the model can tell a two-column spread from a one-column one. The authors never say where the name comes from, and the usual story is that it is the mecha anime, where the suit is a frame with panels bolted onto it. Take that as the usual story rather than a fact.

## The machine upstairs

The thing reading the fiche is a **DeepSeek3B-MoE** decoder. It holds about 3B parameters in total with roughly 570M of them live on any given token, which is the [mixture-of-experts](/blog/moe-is-attention-all-you-really-need/) trick of keeping a big model and paying for a small one.

And this is not an OCR engine in the old sense, which matters for every number below. An old OCR engine looks at a glyph, decides it is an "e", and moves on. This thing is a language model that has been handed some blurry evidence. It does not identify characters. It writes the most likely page, given what it can make out.

That is why the accuracy curve bends instead of falling off a cliff. Blur a word in the middle of a sentence and a glyph classifier returns garbage, while a language model fills in whatever fits. And it is also why the failure mode is so unpleasant, because when the model cannot read a word it does not tell you. It writes a plausible word, in the right font, in the right place.

## Where the grain wins

So how far can you actually push the dial? The paper tests it on [Fox](https://arxiv.org/abs/2405.14295), a document benchmark, using 100 English pages that carry between 600 and 1,300 text tokens each. Then it counts how many characters come back correctly.

| Vision tokens | Text on the page | Reduction | Precision | What that means for you |
|---|---|---|---|---|
| 100 | 600-700 tokens | ~6.7x | 98.5% | effectively lossless; a slip every few hundred characters |
| 64 | ~670 tokens | ~10.5x | 96.5% | roughly one wrong character per line of this post |
| 100 | 1200-1300 tokens | ~12.6x | 87.1% | you would notice while reading it |
| 64 | ~960 tokens | ~15x | 85.8% | same, and now the layout starts drifting too |
| 64 | 1200-1300 tokens | ~20x | 59.1% | two characters in five are invented |

That last row is the ablation, and it is the punchline of the whole paper. Nothing about the model changed between row two and row five, because it is the same weights reading the same page. The only thing that moved was how many pixels the page was allowed to occupy, and 96.5% became 59.1%. At that point the model is writing fan fiction about a document it half saw, confidently, in Times New Roman.

A microfilm bureau would look at that table and shrug, because 20:1 is still inside the band they called *normal reduction*. The silver grain on their film held up fine there. The grain here is the patch, and the patch is 16 pixels across. Once a letter is smaller than that, there is nothing left to recover.

![Precision against compression ratio for 64 and 100 vision tokens, falling from 98.5% at 6.7x to 59.1% at 20x, with the microfilm reduction bands shaded behind](/images/blog48/fox-compression-curve.png) *Figure 3: the same curve the table describes. The shaded bands are the microfilm industry's own names for these ratios, which should tell you how modest the compression here actually is. Source: Author*

## What it beats, and on how little

The compression study is the interesting half. The half that got the attention was the OCR, because the model is small and it wins anyway.

The scoreboard is [OmniDocBench](https://arxiv.org/abs/2412.07626), a document-parsing benchmark graded by edit distance (how many single-character fixes it takes to turn the output into the truth, so lower is better). DeepSeek-OCR beats [GOT-OCR2.0](https://arxiv.org/abs/2409.01704), the previous small-model favourite, while spending 100 vision tokens a page against its 256. And it beats [MinerU2.0](https://arxiv.org/abs/2409.18839), a full document-parsing pipeline that averages over 6,000 tokens a page, while staying under 800.

The training set is 30M PDF pages in about 100 languages, scraped off the internet, 25M of them Chinese and English and 5M everything else. Training ran on 20 nodes of 8 A100-40G each, which is 160 of Nvidia's 2020 datacentre cards.

And then the throughput number, which is the one I keep thinking about. One A100-40G generates over 200,000 pages a day. Put the 160 back together and you get 33 million pages a day. The [British Newspaper Archive](https://www.britishnewspaperarchive.co.uk/), which the British Library has been building with a commercial partner since 2010, is somewhere past 100 million pages. This model would read the lot in three days, on hardware you can rent by the hour. And I am genuinely unsure whether that is a triumph or just a different kind of sad.

## Shrinking the old pages on purpose

Now the idea the paper is really fishing for, which it is careful to call a direction rather than a result.

If precision degrades smoothly with resolution, then resolution is a dial you can turn *during* a conversation. Keep the last few exchanges rendered at 1280 by 1280. Re-render the ones from an hour ago at 1024, yesterday's at 640, last week's at 512. Older context takes up less room and comes back less exactly, which is a fair description of what your own memory does with last Tuesday.

The paper's own framing is the nice part, because the blur stops being a defect and becomes the mechanism. A thing far away is hard to see. We already treat "far away" and "hard to make out" as the same fact about the world, and a model could too.

![The same paragraph rendered four times at falling resolutions from 1280 down to 512, each one blurrier than the last](/images/blog48/optical-forgetting.png) *Figure 4: optical forgetting, drawn with only the model's four real native modes so the ratios are honest. This is a demonstration of what the resolution drop does to a paragraph, not output from DeepSeek-OCR. Source: Author*

I want to be clear that nobody has shipped this. The paper proposes it, draws the picture, and leaves it there. What exists today is the encoder, the decoder, and a table showing the curve that would make such a thing possible.

## Where things are going

- **[Glyph](https://arxiv.org/abs/2510.17800) (Zhipu, 2025)** does the same trick for long context directly, rendering text into images and training a vision-language model on them. It reports about 3.3x average effective compression on [LongBench](https://arxiv.org/abs/2308.14508), a long-context test suite, and up to 4.8x faster prefill. Lower ratios than DeepSeek's, measured on actual reasoning tasks rather than on character recovery.
- **Context Cascade Compression** ([2511.15244](https://arxiv.org/abs/2511.15244)) reports 93% at 40x by cascading two language models instead of going through pixels at all. I have not read its tables, so treat that number as single-sourced.
- **DeepSeek-OCR 2** ([2601.20552](https://arxiv.org/abs/2601.20552)) reports 0.100 edit distance on OmniDocBench v1.5, against the original's 0.129. Also single-sourced here.
- **Token pruning at inference**, like [RTPrune](https://arxiv.org/abs/2605.00392), drops the vision tokens the decoder turns out not to need. The obvious next move, since a page of mostly whitespace should not cost what a page of equations costs.

## The double fold test

In December 2025, three researchers published [Optical Context Compression Is Just (Bad) Autoencoding](https://arxiv.org/abs/2512.03643) (Lee, Yang and Berg-Kirkpatrick). They held the decoder and the training data fixed, and swapped out the vision encoder for two dumber things. One was a learned hierarchical encoder. The other was mean pooling, which is a sliding-window average over token embeddings with essentially no learned parameters at all, the sort of baseline you write in an afternoon. On reconstruction, the simple methods matched or beat the vision encoder at every compression ratio. On language modelling at matched token budgets, the vision route did about as well as truncation, and truncation means throwing the old context in the bin. Their conclusion is that the excitement is running ahead of the evidence, and on the evidence I have seen, they are right. If what you want is a smaller context, a picture of the page is not obviously a better way to get one than averaging some numbers.

Then there are the things the format itself cannot do. Text tokens are addressable, so you can cache the first half of a document and append to it. A rendered page is not addressable. Change one sentence and you re-render and re-encode the whole image it lives on, which means the [KV cache](/blog/kv-caching-mla-is-attention-all-you-really-need/) reuse that makes long chats affordable stops working at the page boundary. Nobody has shown how editing is supposed to work in this world, and I do not think it is a small problem.

The measurement is thinner than the headline suggests, too. Fox here is 100 English pages. Chinese ought to be where optical compression pays most, because a character carries more meaning per token, and that is the case I most want to see measured and have not. Different write-ups also quote 96.5%, 96.8% and 97.3% for what is supposedly the same 10x result.

And my usual caveat, which is getting tiresome to type. Both arXiv and Wikimedia are blocked from the machine I write these on, so every number here comes from published tables as they appear in search results and write-ups, not from the PDFs. The ones I would most like checked are the five Fox rows and the 570M activated-parameter figure.

American libraries spent fifty years microfilming newspapers and throwing away the bound originals. The justification was the **double fold test**: fold a corner of a page back and forth until it tears, and if it fails early the paper is brittle and the volume may go. Nicholson Baker took that apart in [Double Fold](https://en.wikipedia.org/wiki/Double_Fold) (2001). The test was a poor measure of whether a book was dying, the film was often worse than what it replaced, and some of that film has aged less well than the paper would have. The institutions ran a cheap test, believed it, and binned the originals. I am not saying optical compression is that. I am saying 97% is a number off a 100-page benchmark, and nobody should be deleting their text on the strength of it yet.

## Conclusion

Ninety-eight pages on a postcard, and you cannot read a word of it without the machine. Microfilm offered that deal and this offers the same one. You give up direct access to the words, you get the storage back, and from then on a lamp and a lens sit between you and your own archive.

What DeepSeek actually built is a vision encoder designed from the start to be stingy with tokens, which nobody had really done on purpose before. Alongside it they built a measurement of how far that stinginess goes before the page stops coming back. Ten times fewer tokens buys you 97% of your characters. Twenty times buys you 59%, which is to say it buys you a document that looks right and isn't. The follow-up work has already been rude about whether pixels were the right medium for any of this. A sliding-window average currently matches them, and that is the sort of result that either kills an idea or sharpens it.

My bet is that the compression framing fades and the encoder survives. Every long-document model is going to need something that holds its token count flat as the page gets bigger, and DeepEncoder is the first one built for that deliberately rather than by accident. The forgetting idea I find lovely and would not build on yet, because for now it is a figure in a paper and a curve that happens to bend the right way.

But keep the bound volumes. The last lot who trusted a reduction ratio and threw out the originals have been apologising for it for twenty years.

And now you know. Fin.
