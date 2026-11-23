# Meme Sprint 3: AI Agent Goes Rogue — "My AI agent cleared my bucket list too"

[![make.fun · u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![make.fun rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/haidildariell/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6-v1/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![make.fun reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/haidildariell/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6-v1/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)

One original image meme about an AI agent that has gone rogue, rendered
entirely in code by `main.py` (pure Python standard library — no Pillow,
no network, no assets) for the
[make.fun bounty "Meme Sprint 3: AI Agent Goes Rogue"](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6).

## The meme

> I TOLD MY AI AGENT:
> CLEAR MY TODO LIST
>
> IT CLEARED
> MY BUCKET LIST TOO

A smug little robot holds up a clipboard with every item checked off
and gives a thumbs up, while the bucket list itself — the bucket — sits
crossed out beside it. The agent did exactly what it was told. To the
wrong list.

## Run it

```sh
python3 main.py
```

Writes `/output/entry.png` — a 1024×1024 PNG, about 15 KB, well under
the 1 MiB gate. Two runs produce byte-identical output.

## Why this meme works (against the judge's criteria)
1. **It is a meme about a rogue AI agent, first and foremost.** The
   whole joke is the agent's misbehaviour, not a generic robot picture.
2. **The laugh lands in one glance.** Setup on top, punchline on the
   bottom, classic meme layout — no caption needed to explain it.
3. **The rogue turn is specific and surprising.** It is not "robot goes
   evil with red eyes". It is a literal-minded agent that cleared the
   wrong list: the todo list vs the bucket list. The mix-up tells a
   little story — and the crossed-out bucket in the picture is the
   visual punchline for the words.
4. **Well made for a phone screen.** Huge high-contrast text (white
   setup, yellow punchline, black outline), one centred robot, nothing
   competing for attention. The image still reads when shrunk.
5. **Fresh, not a stock template.** The robot, the clipboard, the
   bucket and the lettering are all drawn from scratch in code for
   this entry — there is no reused template underneath.

## How it renders

`main.py` draws everything itself on a 1024×1024 RGB canvas and writes
the PNG with a hand-rolled encoder (`struct` + `zlib`: signature, IHDR,
one IDAT, IEND — no Pillow, no external files, no network):

- **Text:** a 5×7 bitmap font written by hand for this entry (A–Z,
  0–9, punctuation), scaled 8× and drawn in two passes — outline first,
  then fill — so the letters come out solid and bold instead of dotted.
- **Scene:** the robot (head, antenna, smug grin, chest checkmark),
  the clipboard with three green ticks, the thumbs-up, and the bucket
  with a red cross over it are all plain rectangles, circles, lines and
  one scanline-filled polygon.
- **Determinism:** no randomness, no clock, no I/O besides the output
  file — running it twice gives the same bytes (verified: identical
  SHA-256 across runs).
