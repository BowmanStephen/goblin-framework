#!/usr/bin/env python3
"""
TRICKLE BOT — 16-color indexed pixel art banner
Strict arcade hardware constraints: no AA, no gradients, no soft lighting.
"""
from PIL import Image
import struct

# ── 16-color indexed palette (index 0 = transparency/unused) ──
PALETTE = [
    (0,   0,   0),    # 0  black
    (207, 181, 59),   # 1  Miller High Life gold #CFB53B
    (200, 16,  46),   # 2  racing red #C8102E
    (255, 255, 255),  # 3  pure white
    (170, 170, 170),  # 4  light gray (smoke)
    (119, 119, 119),  # 5  mid gray (smoke)
    (68,  68,  68),   # 6  dark gray (smoke)
    (255, 230, 140),  # 7  highlight gold
    (140, 110, 30),   # 8  dark gold / circuit trace
    (100, 8,   20),   # 9  dark red
    (34,  34,  34),   # 10 near-black grid
    (85,  85,  85),   # 11 gray metal (robot hand)
    (180, 180, 180),  # 12 light metal
    (50,  50,  50),   # 13 dark metal
    (230, 200, 90),   # 14 bright gold accent
    (0,   0,   0),    # 15 spare / bg fill
]

W, H = 320, 180  # classic arcade low-res
PX = 3            # pixel block size for that chunky 8-bit feel
PW, PH = W // PX, H // PX  # logical pixel grid: 106 x 60

def idx(r, g, b):
    """Find nearest palette index by Euclidean distance."""
    best, best_d = 0, 1e9
    for i, (pr, pg, pb) in enumerate(PALETTE):
        d = (r - pr)**2 + (g - pg)**2 + (b - pb)**2
        if d < best_d:
            best, best_d = i, d
    return best

# ── Build the logical pixel grid ──
grid = [[0] * PW for _ in range(PH)]

# ── ENVIRONMENT: checkerboard dissolving into gold circuitry ──
for y in range(PH):
    for x in range(PW):
        # Checkerboard phase: left 60% of image
        if x < int(PW * 0.6):
            if (x + y) % 2 == 0:
                grid[y][x] = 3   # white
            else:
                grid[y][x] = 10  # near-black
        # Dissolve zone: 60-80%
        elif x < int(PW * 0.8):
            # Fade checkerboard, sprinkle gold circuit traces
            import random
            random.seed(x * 137 + y * 31)  # deterministic
            if random.random() < 0.35:
                grid[y][x] = 1   # gold
            elif random.random() < 0.15:
                grid[y][x] = 14  # bright gold accent
            elif random.random() < 0.1:
                grid[y][x] = 8   # dark gold trace
            elif (x + y) % 2 == 0:
                grid[y][x] = 3
            else:
                grid[y][x] = 10
        # Right 20%: aggressive gold circuitry on black
        else:
            random.seed(x * 251 + y * 73)
            r = random.random()
            if r < 0.25:
                grid[y][x] = 1   # gold line
            elif r < 0.35:
                grid[y][x] = 14  # bright gold
            elif r < 0.42:
                grid[y][x] = 8   # dark gold
            elif r < 0.48:
                grid[y][x] = 7   # highlight gold
            else:
                grid[y][x] = 0   # black

# ── Helper: draw a rectangle of palette indices ──
def rect(gx, gy, gw, gh, ci):
    for y in range(gy, min(gy + gh, PH)):
        for x in range(gx, min(gx + gw, PW)):
            grid[y][x] = ci

# ── SUBJECT_A: "311" in heavy brutalist pixel font ──
# Hand-crafted pixel numerals, each ~7 wide x 10 tall, with 1px spacing
# Positioned center-left, upper portion
ox, oy = 18, 8  # top-left of "3"

# --- "3" ---
dig3 = [
    " ####",
    "##   ",
    "    #",
    "    #",
    " ###",
    "    #",
    "    #",
    "##   ",
    " ####",
    "##   ",
]
for row_i, row in enumerate(dig3):
    for col_i, ch in enumerate(row):
        if ch == '#':
            grid[oy + row_i][ox + col_i] = 1  # gold body
            # Red outline on left/right edges
            if col_i == 0 or (col_i < len(row) and (col_i == 0 or col_i == len(row.rstrip()) - 1 and row.rstrip()[-1] == '#')):
                pass  # will add red accents below

# Add red edge highlights to "3"
for row_i in range(len(dig3)):
    row = dig3[row_i].rstrip()
    for col_i, ch in enumerate(row):
        if ch == '#':
            # top/bottom edges → red
            if row_i == 0 or row_i == len(dig3) - 1:
                grid[oy + row_i][ox + col_i] = 2
            # right edge → red
            elif col_i == len(row) - 1:
                grid[oy + row_i][ox + col_i] = 2
            else:
                grid[oy + row_i][ox + col_i] = 1

# --- "1" ---
o1x = ox + 7
dig1 = [
    "  #",
    " ##",
    "  #",
    "  #",
    "  #",
    "  #",
    "  #",
    "  #",
    "  #",
    " ###",
]
for row_i, row in enumerate(dig1):
    for col_i, ch in enumerate(row):
        if ch == '#':
            if row_i == len(dig1) - 1 or row_i == 0:
                grid[oy + row_i][o1x + col_i] = 2  # red caps
            else:
                grid[oy + row_i][o1x + col_i] = 1

# --- second "1" ---
o2x = o1x + 5
for row_i, row in enumerate(dig1):
    for col_i, ch in enumerate(row):
        if ch == '#':
            if row_i == len(dig1) - 1 or row_i == 0:
                grid[oy + row_i][o2x + col_i] = 2
            else:
                grid[oy + row_i][o2x + col_i] = 1

# White highlight/outline around "311" for pop
for row_i in range(len(dig3)):
    row = dig3[row_i].rstrip()
    for col_i in range(len(row)):
        if row[col_i] == '#':
            # Paint white 1px border around entire number group
            for dy in [-1, 1]:
                ny = oy + row_i + dy
                if 0 <= ny < PH:
                    for dx in [-1, 1]:
                        nx = ox + col_i + dx
                        if 0 <= nx < PW and grid[ny][nx] not in [1, 2, 3]:
                            grid[ny][nx] = 3

# Same white outline for both "1"s
for base_x in [o1x, o2x]:
    for row_i, row in enumerate(dig1):
        for col_i, ch in enumerate(row):
            if ch == '#':
                for dy in [-1, 1]:
                    ny = oy + row_i + dy
                    if 0 <= ny < PH:
                        for dx in [-1, 1]:
                            nx = base_x + col_i + dx
                            if 0 <= nx < PW and grid[ny][nx] not in [1, 2, 3]:
                                grid[ny][nx] = 3

# ── SUBJECT_B: Mechanized robotic hand holding lit cigarette ──
# Positioned right-center area
hx, hy = 72, 16  # hand top-left

# Robot forearm
rect(hx, hy + 6, 4, 8, 11)      # light metal forearm
rect(hx, hy + 6, 1, 8, 12)      # highlight edge
rect(hx + 3, hy + 6, 1, 8, 13)  # dark edge

# Wrist joint
rect(hx + 1, hy + 5, 2, 1, 2)   # red wrist joint

# Palm
rect(hx + 2, hy + 2, 5, 4, 11)  # light metal palm
rect(hx + 2, hy + 2, 5, 1, 13)  # dark metal top
rect(hx + 6, hy + 2, 1, 4, 13)  # dark metal right

# Fingers gripping (index + middle pinching cigarette)
# Index finger
rect(hx + 3, hy, 1, 2, 11)      # light metal
rect(hx + 3, hy, 1, 1, 13)      # dark tip
# Middle finger
rect(hx + 5, hy, 1, 2, 11)
rect(hx + 5, hy, 1, 1, 13)      # dark tip

# Thumb (opposing, below)
rect(hx + 2, hy + 3, 1, 2, 13)  # dark metal thumb
rect(hx + 1, hy + 4, 1, 1, 11)  # thumb tip

# ── CIGARETTE ──
cx, cy = hx + 4, hy - 3
# Filter (gold)
rect(cx, cy + 1, 2, 2, 1)       # gold filter
rect(cx, cy + 1, 1, 2, 8)       # dark gold stripe
# White body
rect(cx, cy - 1, 2, 2, 3)       # white paper
# Lit tip (red/orange glow)
rect(cx, cy - 2, 2, 1, 2)       # red cherry
grid[cy - 3][cx] = 9             # dark red ember core
grid[cy - 3][cx + 1] = 2         # red ember

# ── SMOKE: blocky gray pixel plumes ──
smoke_pixels = [
    # First puff (right above cherry)
    (cx + 3, cy - 3, 4), (cx + 4, cy - 3, 5),
    (cx + 3, cy - 4, 5), (cx + 2, cy - 4, 6),
    # Second puff
    (cx + 4, cy - 5, 4), (cx + 5, cy - 5, 6),
    (cx + 3, cy - 5, 5), (cx + 5, cy - 6, 5),
    # Third puff (wider, lighter)
    (cx + 4, cy - 7, 4), (cx + 5, cy - 7, 6),
    (cx + 6, cy - 7, 5), (cx + 3, cy - 7, 6),
    # Fourth puff
    (cx + 5, cy - 8, 6), (cx + 6, cy - 8, 4),
    (cx + 4, cy - 9, 5), (cx + 6, cy - 9, 6),
    # Dissipating top
    (cx + 5, cy - 10, 4), (cx + 7, cy - 10, 6),
    (cx + 6, cy - 11, 5), (cx + 3, cy - 11, 6),
]
for sx, sy, ci in smoke_pixels:
    if 0 <= sx < PW and 0 <= sy < PH:
        grid[sy][sx] = ci

# Red LED eye on the hand (robot detail)
grid[hy + 3][hx + 4] = 2  # red eye

# ── Gold circuit traces connecting 311 to the hand ──
# Horizontal gold trace from 311 area toward the hand
trace_x_start, trace_x_end = 30, 70
trace_y = 20
for x in range(trace_x_start, trace_x_end):
    grid[trace_y][x] = 1
    if x % 4 == 0:
        grid[trace_y - 1][x] = 14  # bright gold node
        grid[trace_y + 1][x] = 14
# Vertical connector down to hand
for y in range(trace_y, hy + 8):
    grid[y][trace_x_end - 1] = 1
    if y % 3 == 0:
        grid[y][trace_x_end] = 8   # dark gold branch

# Branch traces in the dissolve zone
for i in range(5):
    bx = 55 + i * 4
    by = 22 + (i % 3)
    rect(bx, by, 1, 3, 1 if i % 2 == 0 else 8)
    rect(bx, by - 1, 1, 1, 14)  # node

# ── TYPOGRAPHY: "TRICKLE BOT" at bottom ──
# 4x5 pixel font, monospaced terminal style
FONT = {
    'T': ["###","# ","###"," # "," # "],
    'R': ["## ","# #","###","# #","# #"],
    'I': ["###"," # "," # "," # ","###"],
    'C': [" ##","#  ","#  ","#  "," ##"],
    'K': ["# #","# #","## ","# #","# #"],
    'L': ["#  ","#  ","#  ","#  ","###"],
    'E': ["###","#  ","## ","#  ","###"],
    'B': ["## ","# #","## ","# #","## "],
    'O': ["###","# #","# #","# #","###"],
    ' ': ["   ","   ","   ","   ","   "],
}

text = "TRICKLE BOT"
char_w = 4  # width per char including 1px spacing
total_w = len(text) * char_w - 1
text_x = (PW - total_w) // 2
text_y = PH - 8

for ci, ch in enumerate(text):
    cx = text_x + ci * char_w
    glyph = FONT.get(ch, FONT[' '])
    for row_i, row in enumerate(glyph):
        for col_i, px in enumerate(row):
            if px != ' ':
                gy = text_y + row_i
                gx = cx + col_i
                if 0 <= gx < PW and 0 <= gy < PH:
                    grid[gy][gx] = 3  # pure white

# Subtle red underline beneath the text
for x in range(text_x, text_x + total_w):
    if 0 <= x < PW:
        grid[text_y + 5][x] = 2   # red
# Gold accents at ends
grid[text_y + 5][text_x] = 1
grid[text_y + 5][text_x + total_w - 1] = 1

# ── RENDER to indexed PNG ──
img = Image.new('P', (W, H))
# Set palette
flat_palette = []
for r, g, b in PALETTE:
    flat_palette.extend([r, g, b])
# Pad to 256 colors (768 values)
flat_palette.extend([0] * (768 - len(flat_palette)))
img.putpalette(flat_palette)

# Draw pixels (each logical pixel = PX×PX block)
pixels = img.load()
for gy in range(PH):
    for gx in range(PW):
        ci = grid[gy][gx]
        for dy in range(PX):
            for dx in range(PX):
                px_x = gx * PX + dx
                px_y = gy * PX + dy
                if px_x < W and px_y < H:
                    pixels[px_x, px_y] = ci

# Save with strict settings (no dithering, indexed)
img.save('/home/hermes/trickle_bot_banner.png', 'PNG', optimize=False)
print("✓ Saved trickle_bot_banner.png (320×180, 16-color indexed, zero AA)")