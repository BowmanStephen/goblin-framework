#!/usr/bin/env python3
"""
TRICKLE BOT — 16-color indexed pixel art banner
Strict arcade hardware constraints: no AA, no gradients, no soft lighting.
Pure programmatic pixel art at 320×180 (classic CPS2 resolution),
scaled 3× for display (960×540).
"""
from PIL import Image

# ── 16-color indexed palette ──
PALETTE = [
    (0,   0,   0),    # 0  BLACK
    (207, 181, 59),   # 1  MILLER HIGH LIFE GOLD #CFB53B
    (200, 16,  46),   # 2  RACING RED #C8102E
    (255, 255, 255),  # 3  PURE WHITE
    (170, 170, 170),  # 4  LIGHT SMOKE
    (119, 119, 119),  # 5  MID SMOKE
    (68,  68,  68),   # 6  DARK SMOKE
    (255, 230, 140),  # 7  HIGHLIGHT GOLD
    (140, 110, 30),   # 8  DARK GOLD / CIRCUIT TRACE
    (100, 8,   20),   # 9  DARK RED
    (34,  34,  34),   # 10 NEAR-BLACK CHECKER
    (85,  85,  85),   # 11 GRAY METAL
    (180, 180, 180),  # 12 LIGHT METAL
    (50,  50,  50),   # 13 DARK METAL
    (230, 200, 90),   # 14 BRIGHT GOLD ACCENT
    (160, 12,  35),   # 15 DEEP RED ACCENT
]

# ── Canvas ──
W, H = 320, 180   # native arcade resolution
PX = 1             # 1:1 pixels at native res
pw, ph = W, H

# ── Pixel grid ──
grid = [[0] * pw for _ in range(ph)]

def rect(x1, y1, w, h, ci):
    for y in range(y1, min(y1 + h, ph)):
        for x in range(x1, min(x1 + w, pw)):
            grid[y][x] = ci

def safe_set(x, y, ci):
    if 0 <= x < pw and 0 <= y < ph:
        grid[y][x] = ci

# ══════════════════════════════════════════
# ENVIRONMENT: Checkerboard → gold circuitry
# ══════════════════════════════════════════
import random
for y in range(ph):
    for x in range(pw):
        pct = x / pw
        if pct < 0.55:
            # Clean checkerboard
            grid[y][x] = 3 if (x // 16 + y // 16) % 2 == 0 else 10
        elif pct < 0.75:
            # Dissolve zone
            random.seed(x * 137 + y * 31)
            if random.random() < 0.30:
                grid[y][x] = 1
            elif random.random() < 0.15:
                grid[y][x] = 14
            elif random.random() < 0.10:
                grid[y][x] = 8
            else:
                grid[y][x] = 3 if (x // 16 + y // 16) % 2 == 0 else 10
        else:
            # Aggressive gold circuitry on black
            random.seed(x * 251 + y * 73)
            r = random.random()
            if r < 0.18:
                grid[y][x] = 1
            elif r < 0.25:
                grid[y][x] = 14
            elif r < 0.30:
                grid[y][x] = 8
            elif r < 0.33:
                grid[y][x] = 7
            else:
                grid[y][x] = 0

# ══════════════════════════════════════════
# SUBJECT_A: "311" — heavy brutalist pixel font
# ══════════════════════════════════════════
# Custom 12×16 brutalist numerals, 3px stroke weight
ox, oy = 40, 25

dig3 = [
    "  ########  ",
    "  ########  ",
    "  ##    ##  ",
    "  ##    ##  ",
    "       ##   ",
    "       ##   ",
    "    ####    ",
    "    ####    ",
    "       ##   ",
    "       ##   ",
    "  ##    ##  ",
    "  ##    ##  ",
    "  ########  ",
    "  ########  ",
    "  ##        ",
    "  ##        ",
]

dig1 = [
    "      ##    ",
    "  ##  ##    ",
    "  ####      ",
    "    ##      ",
    "    ##      ",
    "    ##      ",
    "    ##      ",
    "    ##      ",
    "    ##      ",
    "    ##      ",
    "    ##      ",
    "    ##      ",
    "    ##      ",
    "    ##      ",
    "  ########  ",
    "  ########  ",
]

def draw_digit(glyph, bx, by, body_ci, edge_ci):
    """Draw a digit glyph with body + edge colors."""
    rows = glyph
    for ri, row in enumerate(rows):
        for ci, ch in enumerate(row):
            if ch != ' ':
                gy = by + ri
                gx = bx + ci
                if 0 <= gx < pw and 0 <= gy < ph:
                    # Top/bottom 2 rows → edge color
                    if ri < 2 or ri >= len(rows) - 2:
                        grid[gy][gx] = edge_ci
                    # Rightmost column → edge
                    elif ci >= len(row.rstrip()) - 1 and ch != ' ':
                        grid[gy][gx] = edge_ci
                    else:
                        grid[gy][gx] = body_ci

# Draw "3"
draw_digit(dig3, ox, oy, 1, 2)
# Draw "1"
o1x = ox + 15
draw_digit(dig1, o1x, oy, 1, 2)
# Draw second "1"
o2x = o1x + 15
draw_digit(dig1, o2x, oy, 1, 2)

# White outline buffer (1px around all digits)
def outline_digit(glyph, bx, by, ci=3):
    for ri, row in enumerate(glyph):
        for ci2, ch in enumerate(row):
            if ch != ' ':
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue
                        ny, nx = by + ri + dy, bx + ci2 + dx
                        if 0 <= nx < pw and 0 <= ny < ph:
                            if grid[ny][nx] not in [1, 2, 3, 7, 14]:
                                grid[ny][nx] = 3

outline_digit(dig3, ox, oy)
outline_digit(dig1, o1x, oy)
outline_digit(dig1, o2x, oy)

# Gold glow behind 311 (2px, very subtle)
def glow(glyph, bx, by, ci=7):
    for ri, row in enumerate(glyph):
        for ci2, ch in enumerate(row):
            if ch != ' ':
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        ny, nx = by + ri + dy, bx + ci2 + dx
                        if 0 <= nx < pw and 0 <= ny < ph:
                            if grid[ny][nx] in [0, 10]:
                                grid[ny][nx] = ci

glow(dig3, ox, oy, 7)
glow(dig1, o1x, oy, 7)
glow(dig1, o2x, oy, 7)

# ══════════════════════════════════════════
# SUBJECT_B: Mechanized robotic hand + cigarette
# ══════════════════════════════════════════
hx, hy = 230, 55

# Forearm (tall rectangle)
rect(hx, hy + 30, 28, 55, 11)     # gray metal main
rect(hx, hy + 30, 4, 55, 12)      # light edge
rect(hx + 24, hy + 30, 4, 55, 13) # dark edge
# Forearm rivets/seams
for yy in range(hy + 35, hy + 80, 8):
    rect(hx + 2, yy, 3, 2, 13)
    rect(hx + 23, yy, 3, 2, 13)
# Red stripe on forearm (racing detail)
rect(hx + 4, hy + 32, 20, 3, 2)
rect(hx + 4, hy + 50, 20, 3, 15)

# Wrist joint (wider, mechanical)
rect(hx - 4, hy + 22, 36, 8, 13)  # dark metal joint
rect(hx - 2, hy + 23, 32, 6, 11)  # inner
rect(hx - 4, hy + 22, 36, 2, 12)  # light edge top
rect(hx - 4, hy + 28, 36, 2, 12)  # light edge bottom
# Joint bolts
safe_set(hx - 2, hy + 24, 3)
safe_set(hx + 30, hy + 24, 3)
safe_set(hx - 2, hy + 26, 13)
safe_set(hx + 30, hy + 26, 13)

# Palm (wide, blocky)
rect(hx - 8, hy + 4, 44, 18, 11)  # gray metal palm
rect(hx - 8, hy + 4, 44, 3, 13)   # dark top
rect(hx - 8, hy + 19, 44, 3, 13)  # dark bottom
rect(hx + 32, hy + 4, 4, 18, 13)  # dark right edge
# Palm circuit detail
rect(hx + 8, hy + 8, 20, 2, 1)    # gold trace line
rect(hx + 8, hy + 14, 20, 2, 1)   # gold trace line
safe_set(hx + 18, hy + 9, 14)      # junction node
safe_set(hx + 18, hy + 15, 14)

# INDEX FINGER (pinching cigarette from left)
rect(hx - 12, hy - 8, 10, 14, 11)  # light metal
rect(hx - 12, hy - 8, 10, 3, 13)   # dark tip
rect(hx - 12, hy + 3, 10, 3, 13)   # dark base
# Knuckle joint
rect(hx - 10, hy - 2, 6, 2, 2)    # red joint

# MIDDLE FINGER (pinching from right of cigarette)
rect(hx + 12, hy - 8, 10, 14, 11)
rect(hx + 12, hy - 8, 10, 3, 13)
rect(hx + 12, hy + 3, 10, 3, 13)
rect(hx + 14, hy - 2, 6, 2, 2)     # red joint

# THUMB (opposing grip, below cigarette)
rect(hx - 8, hy + 2, 8, 6, 13)    # dark metal
rect(hx - 8, hy + 6, 8, 3, 11)    # light tip
# Thumb joint
rect(hx - 6, hy + 3, 4, 2, 2)     # red

# ── CIGARETTE (horizontal, gripped between fingers) ──
cx, cy = hx - 14, hy - 14

# Filter (gold section)
rect(cx, cy, 18, 6, 1)       # gold filter
rect(cx, cy, 4, 6, 8)       # dark gold stripe near mouth
# Filter band
rect(cx + 16, cy, 2, 6, 13)  # dark band

# White paper body
rect(cx - 30, cy, 32, 6, 3)   # white paper

# Lit tip (cherry end, pointing left)
rect(cx - 34, cy, 4, 6, 2)    # red cherry
rect(cx - 38, cy + 1, 4, 4, 9)  # dark red ember core
# Bright ember spot
safe_set(cx - 36, cy + 2, 2)
safe_set(cx - 36, cy + 3, 15)

# ── SMOKE: blocky discrete gray pixel plumes rising from cherry ──
smoke = [
    # Column 1 (close, dense)
    (-40, -3, 6), (-38, -3, 4), (-42, -4, 5), (-39, -4, 6),
    (-41, -5, 4), (-37, -5, 5), (-43, -6, 6), (-38, -6, 4),
    # Column 2 (spreading)
    (-44, -8, 5), (-39, -8, 4), (-42, -9, 6), (-36, -9, 5),
    (-45, -11, 4), (-38, -11, 6), (-41, -12, 5), (-34, -12, 4),
    # Column 3 (wide, dissipating)
    (-46, -14, 6), (-40, -14, 4), (-34, -14, 5),
    (-48, -17, 5), (-42, -17, 6), (-36, -17, 4),
    (-49, -20, 4), (-44, -20, 6), (-38, -20, 5),
    # Last wisps
    (-50, -23, 6), (-43, -23, 4),
    (-47, -26, 5),
]
for dx, dy, ci in smoke:
    sx, sy = cx + dx, cy + dy
    safe_set(sx, sy, ci)

# ══════════════════════════════════════════
# Gold circuit traces connecting 311 to hand
# ══════════════════════════════════════════
# Main horizontal bus
trace_y = oy + 20
for x in range(ox + 15, hx + 12, 2):
    safe_set(x, trace_y, 1)
    # Junction nodes every 20px
    if x % 20 < 2 and x > ox + 30:
        safe_set(x, trace_y - 3, 14)
        safe_set(x, trace_y - 2, 14)
        safe_set(x, trace_y - 1, 8)
        safe_set(x, trace_y + 1, 8)
        safe_set(x, trace_y + 2, 14)
        safe_set(x, trace_y + 3, 14)

# Vertical drop to hand
for y in range(trace_y, hy + 30, 2):
    safe_set(hx + 14, y, 1)
    if y % 8 < 2:
        safe_set(hx + 15, y, 8)

# Branch circuits radiating from the main bus
branches = [
    (130, trace_y, 0, -15, 3),   # up
    (150, trace_y, 0, 15, 3),    # down
    (180, trace_y, 0, -20, 4),   # up
    (200, trace_y, 0, 12, 2),    # down
    (170, trace_y - 5, 10, 0, 2),# right
]
for bx, by, dx, dy, length in branches:
    step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
    step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
    for i in range(abs(dx) + abs(dy)):
        px = bx + i * step_x
        py = by + i * step_y
        safe_set(px, py, 1)
        if i % 4 == 0:
            safe_set(px + step_y, py + step_x, 14)  # corner node

# ══════════════════════════════════════════
# TYPOGRAPHY: "TRICKLE BOT" at bottom
# ══════════════════════════════════════════
# 5×7 monospaced terminal pixel font
FONT = {
    'T': ["#####","  #  ","  #  ","  #  ","  #  ","  #  ","  #  "],
    'R': ["#### ","#   #","#### ","# #  ","#  # ","#   #","#   #"],
    'I': ["#####","  #  ","  #  ","  #  ","  #  ","  #  ","#####"],
    'C': [" ####","#    ","#    ","#    ","#    ","#    "," ####"],
    'K': ["#  #","# # ","##  ","# # ","# # ","#  #","#  #"],
    'L': ["#    ","#    ","#    ","#    ","#    ","#    ","#####"],
    'E': ["#####","#    ","#### ","#    ","#    ","#    ","#####"],
    'B': ["#### ","#   #","#   #","#### ","#   #","#   #","#### "],
    'O': [" ### ","#   #","#   #","#   #","#   #","#   #"," ### "],
    ' ': ["     ","     ","     ","     ","     ","     ","     "],
}

text = "TRICKLE BOT"
char_w = 6  # 5px glyph + 1px spacing
total_w = len(text) * char_w - 1
text_x = (pw - total_w) // 2
text_y = ph - 14

for i, ch in enumerate(text):
    bx = text_x + i * char_w
    glyph = FONT.get(ch, FONT[' '])
    for ri, row in enumerate(glyph):
        for ci, px_ch in enumerate(row):
            if px_ch != ' ':
                gx = bx + ci
                gy = text_y + ri
                if 0 <= gx < pw and 0 <= gy < ph:
                    grid[gy][gx] = 3  # pure white

# Red underline bar
rect(text_x, text_y + 9, total_w, 2, 2)
# Gold endcaps
rect(text_x, text_y + 9, 3, 2, 1)
rect(text_x + total_w - 3, text_y + 9, 3, 2, 1)

# ══════════════════════════════════════════
# RENDER: Indexed PNG, zero anti-aliasing
# ══════════════════════════════════════════
img = Image.new('P', (W, H))

# Set strict 16-color palette
flat = []
for r, g, b in PALETTE:
    flat.extend([r, g, b])
flat.extend([0] * (768 - len(flat)))
img.putpalette(flat)

pixels = img.load()
for y in range(H):
    for x in range(W):
        pixels[x, y] = grid[y][x]

out = '/home/hermes/trickle_bot_banner.png'
img.save(out, 'PNG', optimize=False)
print(f"✓ Saved {out} ({W}×{H}, 16-color indexed, zero AA)")

# Also save 3× scaled version for display
img3x = img.resize((W * 3, H * 3), Image.NEAREST)
out3 = '/home/hermes/trickle_bot_banner_3x.png'
img3x.save(out3, 'PNG', optimize=False)
print(f"✓ Saved {out3} ({W*3}×{H*3}, NEAREST upscale, zero AA)")