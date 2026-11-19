# 19 November 2026 — World News in One Image

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/joyrichh/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/joyrichh/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Make.Fun competition entry ([`news-image-20261119`](https://make.fun/bounty/news-image-20261119)) by [@joyrichh](https://github.com/joyrichh).
A program that writes one image summing up the world's news of Thursday,
19 November 2026, to `/output/entry.png`.

## The image

A 1024×1024 PNG infographic — "19 November 2026: the day's biggest stories,
in one image" — with six main stories and an "Also today" strip:

1. **Entertainment** — GTA VI begins global rollout as gamers enter Vice City.
   After 13 years, Rockstar's blockbuster unlocks at midnight in each market,
   starting in New Zealand, to rave early reviews.
2. **Diplomacy** — Trump, Xi and Putin meet in Shenzhen in first three-way summit.
   The leaders of the U.S., China and Russia sit down together for the first
   time, with nuclear arms, Iran and Ukraine on the table.
3. **Ukraine** — Crimean Bridge hit a third time this week, traffic halted.
   Russia's installed governor in Crimea said the bridge was attacked again;
   damage is being assessed, days after its road span collapsed.
4. **Culture** — Van Gogh sells for record $190.4m after Nazi-era row settled.
   Blossoming Chestnut Trees smashed the artist's auction record at Sotheby's,
   a day after a deal with the Fischer heirs.
5. **Tech** — Anthropic raises $81.3bn in biggest IPO of all time.
   Shares priced at $83 value the Claude maker at about $1.5tn; it starts
   trading on the Nasdaq on Thursday as ANT.
6. **Justice** — World court delivers Myanmar genocide verdict today.
   The ICJ rules in The Gambia's case over the 2017 crackdown that drove
   700,000+ Rohingya to Bangladesh.

Also today:

- EU proposes a €45bn Ukraine loan, repayable only once Russia pays reparations.
- Israeli tanks cross Gaza's Yellow Line in a rare ground operation; Hamas calls it a ceasefire breach.
- Democrats nominate Hakeem Jeffries, 251-11, set to be the first Black House Speaker.

The stories and verification note are supplied by the competition brief and
retained in `news.json`. Sources credited in the image footer are Reuters,
AP, NASA and Pew Research Center. The build performs no network requests.

## How it works

- `main.ts` (Node 22, standard library only) decodes the bundled
  `entry.png.b64`, checks the PNG magic bytes, and writes `/output/entry.png`.
  The base64 bundle keeps the entry suitable for plain UTF-8 repositories.
  No network, randomness or timestamps: repeated runs write identical bytes.
- `news.json` holds all six stories, three additional stories, date and sources.
- `build_image.py` renders the PNG using Pillow 10.2.0 and system DejaVu fonts.
  It measures every line, fits headlines to at most two lines and summaries
  to at most three, and asserts text stays within its containing bounds.
  No words are truncated. The finished PNG is encoded as `entry.png.b64`.
- `.makefun/owner.json` names the entry wallet for this account.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# out/entry.png — 1024x1024 PNG, 142,520 bytes
```

Rebuild the bundled image (Pillow 10.2.0 and DejaVu fonts required):

```sh
python3 build_image.py
base64 -w0 entry.png > entry.png.b64
```

Determinism check:

```sh
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 node main.ts
MAKEFUN_OUTPUT_DIR=out2 node main.ts
sha256sum out1/entry.png out2/entry.png   # identical hashes
```

## License

MIT — see `LICENSE`.
