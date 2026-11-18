# makefun-news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/haidil011/makefun-news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/haidil011/makefun-news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

One day's world news as a single front page: Tuesday 17 November 2026. Iran's drones and the
answering strike at Qeshm, the Kerch bridge span in the sea, Manila's minerals pact and the AI-chip
licence list — set in ivory newsprint, ink and vermilion with a halftone locator map of the Gulf.

`entry.png` is 1024×1024 and 153 KB. `main.py` only copies it; `gen.py` draws it again from the
committed fonts and coastline data.

## Run it

```sh
python3 main.py     # writes /output/entry.png, no network, stdlib only
python3 gen.py      # redraws entry.png here (needs Pillow and the fonts/ folder)
```
