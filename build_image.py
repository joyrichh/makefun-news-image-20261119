#!/usr/bin/env python3
"""Render the supplied 19 November 2026 news as a deterministic 1024x1024 PNG.

Build-time dependencies: Pillow 10.2.0 and system DejaVu fonts. The Node entry
program uses only the standard library and the bundled entry.png.b64.
All text is measured before drawing; overlong content raises an error instead
of being truncated. TEXT_LAYOUT records the measured bounds for verification.
"""

import json
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
NAVY = "#0E2A47"
GOLD = "#E8B84B"
INK = "#111827"
GREY = "#475569"
LIGHT = "#F1F5F9"
CARD_BORDER = "#CBD5E1"
WHITE = "#FFFFFF"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_B = FONT_DIR / "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR / "DejaVuSans.ttf"
SANS_B = FONT_DIR / "DejaVuSans-Bold.ttf"
NEWS = json.loads((HERE / "news.json").read_text(encoding="utf-8"))
NEWS_DATE = date.fromisoformat(NEWS["date"])
DATE_TITLE = f"{NEWS_DATE.day} {NEWS_DATE.strftime('%B')} {NEWS_DATE.year}"
TEXT_LAYOUT = []
img = Image.new("RGB", (W, H), WHITE)
draw = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(str(path), size)


def wrap(text, face, max_width):
    lines = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=face) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit(text, path, preferred_size, max_width, max_lines):
    for size in range(preferred_size, 13, -1):
        face = font(path, size)
        lines = wrap(text, face, max_width)
        if len(lines) <= max_lines and all(
            draw.textlength(line, font=face) <= max_width
            and draw.textbbox((0, 0), line, font=face)[2] <= max_width
            for line in lines
        ):
            assert " ".join(lines) == text
            return face, lines
    raise ValueError(f"Text does not fit: {text}")


def text_at(position, text, face, fill, bounds, label, anchor=None):
    bbox = draw.textbbox(position, text, font=face, anchor=anchor)
    left, top, right, bottom = bounds
    assert left <= bbox[0] <= bbox[2] <= right, (label, text, bbox, bounds)
    assert top <= bbox[1] <= bbox[3] <= bottom, (label, text, bbox, bounds)
    TEXT_LAYOUT.append({
        "label": label,
        "text": text,
        "bbox": bbox,
        "bounds": bounds,
        "width": draw.textlength(text, font=face),
        "font_size": face.size,
    })
    draw.text(position, text, font=face, fill=fill, anchor=anchor)


def render():
    assert len(NEWS["stories"]) == 6
    assert len(NEWS["also_today"]) == 3
    assert NEWS_DATE.strftime("%A") == NEWS["day"]
    TEXT_LAYOUT.clear()
    draw.rectangle([0, 0, W, H], fill=WHITE)
    draw.rectangle([0, 0, W, 168], fill=NAVY)
    draw.rectangle([0, 168, W, 172], fill=GOLD)
    header_bounds = (24, 0, 812, 168)
    text_at((36, 26), f"WORLD NEWS • {NEWS['day'].upper()}",
            font(SANS_B, 21), GOLD, header_bounds, "kicker")
    text_at((36, 56), DATE_TITLE, font(SERIF_B, 58), WHITE,
            header_bounds, "title")
    text_at((36, 126), "The day's biggest stories, in one image",
            font(SANS, 23), "#BACDE0", header_bounds, "subtitle")
    badge_bounds = (828, 34, 988, 132)
    draw.rounded_rectangle(badge_bounds, radius=12, outline=GOLD, width=2)
    text_at((908, 48), NEWS_DATE.strftime("%b").upper(), font(SANS_B, 21),
            GOLD, badge_bounds, "badge month", anchor="mt")
    text_at((908, 74), str(NEWS_DATE.day), font(SERIF_B, 40), WHITE,
            badge_bounds, "badge day", anchor="mt")

    margin, start_y, gap = 24, 192, 16
    card_width = (W - 2 * margin - gap) // 2
    card_height = 204
    for index, story in enumerate(NEWS["stories"]):
        column, row = index % 2, index // 2
        left = margin + column * (card_width + gap)
        top = start_y + row * (card_height + gap)
        right, bottom = left + card_width, top + card_height
        card_bounds = (left + 20, top + 12, right - 20, bottom - 10)
        draw.rounded_rectangle([left, top, right, bottom], radius=14,
                               fill=WHITE, outline=CARD_BORDER, width=1)
        draw.rounded_rectangle([left, top, left + 8, bottom], radius=4,
                               fill=story["color"])
        tag_font = font(SANS_B, 17)
        tag_width = draw.textlength(story["tag"], font=tag_font) + 20
        draw.rounded_rectangle([left + 22, top + 16,
                                left + 22 + tag_width, top + 44],
                               radius=7, fill=story["color"])
        text_at((left + 32, top + 21), story["tag"], tag_font, WHITE,
                card_bounds, f"story {index + 1} tag")
        headline_font, headline_lines = fit(
            story["headline"], SANS_B, 25, card_width - 44, 2)
        for line_index, line in enumerate(headline_lines):
            text_at((left + 22, top + 56 + line_index * 30), line,
                    headline_font, INK, card_bounds,
                    f"story {index + 1} headline")
        summary_font, summary_lines = fit(
            story["summary"], SANS, 19, card_width - 44, 3)
        for line_index, line in enumerate(summary_lines):
            text_at((left + 22, top + 122 + line_index * 25), line,
                    summary_font, GREY, card_bounds,
                    f"story {index + 1} summary")

    also_top = start_y + 3 * card_height + 2 * gap + 16
    strip_bounds = (margin + 22, also_top + 6, W - margin - 22, also_top + 98)
    draw.rounded_rectangle([margin, also_top, W - margin, also_top + 100],
                           radius=14, fill=LIGHT)
    text_at((margin + 22, also_top + 10), "ALSO TODAY", font(SANS_B, 19),
            NAVY, strip_bounds, "also heading")
    also_lines = [f"•  {line}" for line in NEWS["also_today"]]
    also_size = next(size for size in range(19, 13, -1) if all(
        draw.textlength(line, font=font(SANS, size)) <= W - 2 * margin - 44
        for line in also_lines
    ))
    for line_index, line in enumerate(also_lines):
        text_at((margin + 22, also_top + 35 + line_index * 21), line,
                font(SANS, also_size), INK, strip_bounds, "also story")

    sources = f"Sources: {' · '.join(NEWS['sources'])}  —  {DATE_TITLE}"
    text_at((W // 2, 978), sources, font(SANS, 15), GREY,
            (24, 970, W - 24, H - 16), "footer", anchor="mt")
    output = HERE / "entry.png"
    img.save(output, "PNG", optimize=True)
    assert output.stat().st_size <= 1048576
    print(f"saved {output}: {W}x{H}, {output.stat().st_size:,} bytes; "
          f"{len(TEXT_LAYOUT)} text lines checked")


if __name__ == "__main__":
    render()
