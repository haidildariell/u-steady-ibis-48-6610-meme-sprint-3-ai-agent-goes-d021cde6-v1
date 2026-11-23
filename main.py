#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue -- v1.

Renders ONE original meme to /output/entry.png using pure Python
standard library only (os, struct, zlib, math). No Pillow, no network.

The joke (written by me for this entry):
    top:    I TOLD MY AI AGENT: / CLEAR MY TODO LIST
    bottom: IT CLEARED / MY BUCKET LIST TOO
A smug little robot holds up a clipboard with everything checked off,
next to a crossed-out bucket. The agent did exactly what it was told --
to the wrong list.

Deterministic: two runs produce byte-identical PNG output.
"""

import math
import os
import struct
import zlib

W = 1024
H = 1024
OUT = os.environ.get("ENTRY_PNG", "/output/entry.png")

# ---------------------------------------------------------------- font 5x7
# Each glyph: 7 rows of 5 bits, written by hand for this entry.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11100", "10010", "10001", "10001", "10001", "10010", "11100"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    ":": ("00000", "01100", "00000", "00000", "00000", "01100", "00000"),
    ";": ("00000", "01100", "00000", "00000", "01100", "00100", "01000"),
}

# ---------------------------------------------------------------- canvas
# RGB bytearray, row-major.
buf = bytearray(W * H * 3)


def fill(color):
    """Fill the whole canvas with one RGB color."""
    rgb = bytes(color)
    row = rgb * W
    for y in range(H):
        buf[y * W * 3:(y + 1) * W * 3] = row


def fill_rect(x, y, w, h, color):
    """Axis-aligned filled rectangle, clipped to the canvas."""
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    rgb = bytes(color)
    span = rgb * (x1 - x0)
    for yy in range(y0, y1):
        off = (yy * W + x0) * 3
        buf[off:off + len(span)] = span


def rect_outline(x, y, w, h, color, t=3):
    fill_rect(x, y, w, t, color)
    fill_rect(x, y + h - t, w, t, color)
    fill_rect(x, y, t, h, color)
    fill_rect(x + w - t, y, t, h, color)


def fill_circle(cx, cy, r, color):
    rgb = bytes(color)
    for dy in range(-r, r + 1):
        dx = int(math.sqrt(r * r - dy * dy))
        x0 = max(0, cx - dx)
        x1 = min(W, cx + dx + 1)
        yy = cy + dy
        if 0 <= yy < H and x1 > x0:
            span = rgb * (x1 - x0)
            off = (yy * W + x0) * 3
            buf[off:off + len(span)] = span


def draw_line(x0, y0, x1, y1, color, t=6):
    """Thick line via Bresenham + filled circles at each step."""
    steps = max(abs(x1 - x0), abs(y1 - y0), 1)
    r = max(1, t // 2)
    for i in range(steps + 1):
        x = x0 + (x1 - x0) * i // steps
        y = y0 + (y1 - y0) * i // steps
        fill_circle(x, y, r, color)


def draw_arc(cx, cy, r, a0, a1, color, t=8):
    """Arc of a circle, angles in degrees, 0 = east, going clockwise down."""
    steps = max(8, int(abs(a1 - a0)))
    for i in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * i / steps)
        x = int(cx + r * math.cos(a))
        y = int(cy + r * math.sin(a))
        fill_circle(x, y, max(1, t // 2), color)


def fill_polygon(points, color):
    """Scanline fill for a simple polygon (list of (x, y))."""
    ys = [p[1] for p in points]
    for y in range(max(0, min(ys)), min(H, max(ys) + 1)):
        xs = []
        n = len(points)
        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]
            if (y0 <= y < y1) or (y1 <= y < y0):
                xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            fill_rect(int(xs[i]), y, max(1, int(xs[i + 1]) - int(xs[i])), 1, color)


# ---------------------------------------------------------------- text
def text_width(text, scale):
    return (len(text) * 6 - 1) * scale


def draw_text(text, x, y, scale, color, outline=None):
    """Draw text at top-left (x, y). outline: optional outline color.

    Two passes: every lit cell's outline first, then every lit cell's
    fill. (One interleaved pass lets a later cell's outline paint over
    an earlier cell's fill, which leaves dotted gaps between cells.)
    """
    cells = []
    cx = x
    for ch in text:
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    cells.append((cx + col * scale, y + row * scale))
        cx += 6 * scale
    if outline is not None:
        for px, py in cells:
            fill_rect(px - 2, py - 2, scale + 4, scale + 4, outline)
    for px, py in cells:
        fill_rect(px, py, scale, scale, color)


def draw_text_centered(text, y, scale, color, outline=None):
    x = (W - text_width(text, scale)) // 2
    draw_text(text, x, y, scale, color, outline)


# ---------------------------------------------------------------- PNG out
def _chunk(kind, data):
    c = struct.pack(">I", len(data)) + kind + data
    c += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return c


def write_png(path):
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter: none
        raw += buf[y * W * 3:(y + 1) * W * 3]
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# ---------------------------------------------------------------- the meme
# Palette
BG = (16, 28, 46)        # deep navy
PANEL = (24, 42, 66)     # stage panel
PANEL_EDGE = (52, 84, 120)
WHITE = (255, 255, 255)
BLACK = (8, 10, 16)
YELLOW = (255, 210, 63)   # punchline
HEAD = (215, 222, 232)    # robot head
BODY = (78, 138, 201)     # robot body
DARK = (14, 22, 38)       # screens / outlines
GREEN = (34, 197, 94)     # checkmarks
RED = (229, 72, 77)       # crossed-out bucket
CLIP = (245, 245, 245)    # clipboard paper
GRAY_LINE = (140, 150, 165)


def render():
    fill(BG)

    # --- top text: the setup (white, scale 8) ---
    draw_text_centered("I TOLD MY AI AGENT:", 46, 8, WHITE, BLACK)
    draw_text_centered("CLEAR MY TODO LIST", 132, 8, WHITE, BLACK)

    # --- stage panel ---
    fill_rect(64, 232, 896, 516, PANEL)
    rect_outline(64, 232, 896, 516, PANEL_EDGE, 4)

    # --- robot: antenna ---
    draw_line(512, 268, 512, 316, DARK, 8)
    fill_circle(512, 256, 15, RED)
    fill_circle(512, 256, 8, (255, 120, 120))

    # --- robot: ears + head ---
    fill_rect(368, 356, 22, 52, BODY)
    fill_rect(634, 356, 22, 52, BODY)
    fill_rect(382, 316, 260, 152, HEAD)
    rect_outline(382, 316, 260, 152, DARK, 4)

    # eyes: wide, pleased with itself; pupils looking up-right (smug)
    fill_circle(456, 372, 26, WHITE)
    fill_circle(568, 372, 26, WHITE)
    fill_circle(462, 366, 11, DARK)
    fill_circle(574, 366, 11, DARK)
    # smug grin
    draw_arc(512, 396, 58, 20, 160, DARK, 9)
    # blush of pride
    fill_circle(428, 420, 10, (244, 130, 130))
    fill_circle(596, 420, 10, (244, 130, 130))

    # --- neck + body ---
    fill_rect(484, 468, 56, 26, DARK)
    fill_rect(362, 494, 300, 190, BODY)
    rect_outline(362, 494, 300, 190, DARK, 4)
    # chest screen with a big green check
    fill_rect(452, 528, 120, 92, DARK)
    draw_line(472, 578, 498, 602, GREEN, 10)
    draw_line(498, 602, 556, 542, GREEN, 10)

    # --- left arm + clipboard: everything checked off ---
    fill_rect(300, 560, 62, 30, BODY)
    rect_outline(300, 560, 62, 30, DARK, 3)
    fill_rect(196, 500, 118, 158, CLIP)
    rect_outline(196, 500, 118, 158, DARK, 4)
    fill_rect(232, 492, 46, 18, (120, 90, 60))  # clipboard clip
    for i, yy in enumerate((528, 566, 604)):
        draw_line(238, yy + 12, 252, yy + 24, GREEN, 7)
        draw_line(252, yy + 24, 272, yy - 2, GREEN, 7)
        fill_rect(282, yy + 2, 24, 8, GRAY_LINE)
    # clipboard check lines (the list itself)
    # (checks above already sit left of each line)

    # --- right arm: thumbs up ---
    fill_rect(662, 560, 62, 30, BODY)
    rect_outline(662, 560, 62, 30, DARK, 3)
    fill_circle(742, 540, 26, HEAD)
    rect_outline(716, 514, 52, 52, DARK, 3)  # fist outline block
    fill_rect(728, 498, 22, 38, HEAD)        # thumb sticking up
    rect_outline(728, 498, 22, 38, DARK, 3)

    # --- feet ---
    fill_rect(402, 684, 70, 26, DARK)
    fill_rect(552, 684, 70, 26, DARK)

    # --- the bucket, crossed out (bottom-right of the stage) ---
    # Bigger bucket, red X centred on it so the cross-out reads at once.
    fill_polygon([(730, 706), (852, 706), (832, 630), (750, 630)], (138, 148, 166))
    fill_rect(724, 622, 124, 12, (110, 120, 138))  # bucket rim
    draw_line(736, 606, 846, 682, RED, 12)
    draw_line(846, 606, 736, 682, RED, 12)

    # --- bottom text: the punchline (yellow, scale 8) ---
    draw_text_centered("IT CLEARED", 786, 8, YELLOW, BLACK)
    draw_text_centered("MY BUCKET LIST TOO", 872, 8, YELLOW, BLACK)


def main():
    render()
    n = write_png(OUT)
    print("wrote %s (%d bytes, %dx%d)" % (OUT, n, W, H))


if __name__ == "__main__":
    main()
