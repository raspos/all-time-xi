import os
import io
import json
import hashlib
import requests
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageOps

CACHE_DIR = "/tmp/image_cache"
try:
    os.makedirs(CACHE_DIR, exist_ok=True)
except Exception:
    pass

def load_korean_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    font_filename = "NanumGothic-Bold.ttf" if bold else "NanumGothic-Regular.ttf"

    search_dirs = [
        # Relative to server directory
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "fonts"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "fonts"),
        # Relative to CWD
        os.path.join(os.getcwd(), "data", "fonts"),
        os.path.join(os.getcwd(), "api", "data", "fonts"),
        # Vercel / Lambda environment
        "/var/task/data/fonts",
        "/var/task/api/data/fonts",
        "/tmp/fonts",
    ]

    for d in search_dirs:
        p = os.path.join(d, font_filename)
        if os.path.isfile(p):
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                pass

    # Windows fallback
    win_font = r"C:\Windows\Fonts\malgunbd.ttf" if bold else r"C:\Windows\Fonts\malgun.ttf"
    if os.path.isfile(win_font):
        try:
            return ImageFont.truetype(win_font, size=size)
        except Exception:
            pass

    # Linux system fallbacks
    sys_candidates = [
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    for sp in sys_candidates:
        if os.path.isfile(sp):
            try:
                return ImageFont.truetype(sp, size=size)
            except Exception:
                pass

    return ImageFont.load_default()

def hex_to_rgb(hex_str: str, default: Tuple[int, int, int] = (30, 41, 59)) -> Tuple[int, int, int]:
    if not hex_str:
        return default
    h = hex_str.lstrip("#")
    if len(h) == 6:
        try:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
        except Exception:
            return default
    return default

def fetch_cached_portrait(url: Optional[str]) -> Optional[Image.Image]:
    if not url or not url.startswith("http"):
        return None
    h = hashlib.md5(url.encode("utf-8")).hexdigest()
    cpath = os.path.join(CACHE_DIR, f"{h}.png")
    if os.path.exists(cpath):
        try:
            return Image.open(cpath).convert("RGBA")
        except Exception:
            pass
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=1.5)
        if resp.status_code == 200 and len(resp.content) > 500:
            img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
            img.thumbnail((200, 200), Image.Resampling.LANCZOS)
            img.save(cpath, "PNG")
            return img
    except Exception:
        return None
    return None

def draw_football_pitch(draw: ImageDraw.ImageDraw, box: Tuple[int, int, int, int], theme: str = "classic_emerald"):
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0

    themes = {
        "classic_emerald": ((15, 82, 45), (19, 98, 54), (255, 255, 255, 200)),
        "midnight_tactics": ((15, 23, 42), (22, 33, 58), (56, 189, 248, 190)),
        "worldcup_gold": ((17, 62, 38), (22, 78, 48), (250, 204, 21, 200)),
        "royal_turf": ((12, 74, 62), (16, 92, 78), (241, 245, 249, 190))
    }
    c_dark, c_light, line_col = themes.get(theme, themes["classic_emerald"])

    # Draw alternating grass stripes
    num_stripes = 10
    stripe_h = h / num_stripes
    for i in range(num_stripes):
        sy0 = int(y0 + i * stripe_h)
        sy1 = int(y0 + (i + 1) * stripe_h)
        draw.rectangle([x0, sy0, x1, sy1], fill=c_light if i % 2 == 0 else c_dark)

    # Outer pitch boundary
    pad = int(min(w, h) * 0.045)
    px0, py0, px1, py1 = x0 + pad, y0 + pad, x1 - pad, y1 - pad
    pw, ph = px1 - px0, py1 - py0
    lw = max(2, int(min(w, h) * 0.004))

    draw.rectangle([px0, py0, px1, py1], outline=line_col[:3], width=lw)

    # Halfway line & Center circle
    mid_y = (py0 + py1) // 2
    mid_x = (px0 + px1) // 2
    draw.line([px0, mid_y, px1, mid_y], fill=line_col[:3], width=lw)
    cr = int(min(pw, ph) * 0.12)
    draw.ellipse([mid_x - cr, mid_y - cr, mid_x + cr, mid_y + cr], outline=line_col[:3], width=lw)
    draw.ellipse([mid_x - 4, mid_y - 4, mid_x + 4, mid_y + 4], fill=line_col[:3])

    # Direction watermark inside top penalty area: ▲ ATTACK (공격 방향)
    f_dir = load_korean_font(max(12, int(min(w, h) * 0.022)), bold=True)
    dir_txt = "▲ ATTACK (공격 방향)"
    dbbox = draw.textbbox((0, 0), dir_txt, font=f_dir)
    dw = dbbox[2] - dbbox[0]
    draw.text((mid_x - dw // 2, py0 + 8), dir_txt, fill=(255, 255, 255, 120), font=f_dir)

    # Top & Bottom Penalty Boxes & Goals
    pen_w = int(pw * 0.56)
    pen_h = int(ph * 0.155)
    six_w = int(pw * 0.26)
    six_h = int(ph * 0.055)
    goal_w = int(pw * 0.14)
    goal_h = int(pad * 0.45)

    # Top (Attack target goal)
    draw.rectangle([mid_x - pen_w // 2, py0, mid_x + pen_w // 2, py0 + pen_h], outline=line_col[:3], width=lw)
    draw.rectangle([mid_x - six_w // 2, py0, mid_x + six_w // 2, py0 + six_h], outline=line_col[:3], width=lw)
    draw.rectangle([mid_x - goal_w // 2, py0 - goal_h, mid_x + goal_w // 2, py0], outline=line_col[:3], width=lw)
    arc_r = int(pw * 0.09)
    draw.arc([mid_x - arc_r, py0 + pen_h - arc_r, mid_x + arc_r, py0 + pen_h + arc_r], start=20, end=160, fill=line_col[:3], width=lw)

    # Bottom (Own GK goal)
    draw.rectangle([mid_x - pen_w // 2, py1 - pen_h, mid_x + pen_w // 2, py1], outline=line_col[:3], width=lw)
    draw.rectangle([mid_x - six_w // 2, py1 - six_h, mid_x + six_w // 2, py1], outline=line_col[:3], width=lw)
    draw.rectangle([mid_x - goal_w // 2, py1, mid_x + goal_w // 2, py1 + goal_h], outline=line_col[:3], width=lw)
    draw.arc([mid_x - arc_r, py1 - pen_h - arc_r, mid_x + arc_r, py1 - pen_h + arc_r], start=200, end=340, fill=line_col[:3], width=lw)

def draw_player_node(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    radius: int,
    player: Dict[str, Any],
    kit_primary: Tuple[int, int, int],
    kit_secondary: Tuple[int, int, int],
    kit_text: Tuple[int, int, int]
):
    font_name = load_korean_font(max(14, int(radius * 0.44)), bold=True)
    font_sub = load_korean_font(max(11, int(radius * 0.34)), bold=False)
    font_num = load_korean_font(max(16, int(radius * 0.62)), bold=True)
    font_pos = load_korean_font(max(10, int(radius * 0.36)), bold=True)

    # Shadow
    draw.ellipse([cx - radius - 2, cy - radius + 3, cx + radius + 2, cy + radius + 7], fill=(0, 0, 0, 140))

    # Outer ring (gold if captain, red if low suitability, else secondary kit color)
    is_cap = bool(player.get("is_captain"))
    suit = player.get("suitability_status", "적합")
    ring_col = (250, 204, 21) if is_cap else ((248, 113, 113) if "낮음" in suit else kit_secondary)

    draw.ellipse([cx - radius - 4, cy - radius - 4, cx + radius + 4, cy + radius + 4], fill=ring_col)
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=kit_primary)

    # Portrait image if available
    portrait = fetch_cached_portrait(player.get("image_url"))
    if portrait is not None:
        size = radius * 2
        mask = Image.new("L", (size, size), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.ellipse((0, 0, size, size), fill=255)
        fitted = ImageOps.fit(portrait, (size, size), centering=(0.5, 0.3))
        canvas.paste(fitted, (cx - radius, cy - radius), mask)
    else:
        num_str = str(player.get("jersey_number") or player.get("fallback_number") or 10)
        bbox = draw.textbbox((0, 0), num_str, font=font_num)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((cx - tw // 2, cy - th // 2 - 2), num_str, fill=kit_text, font=font_num)

    # Position pill at top-left of circle
    slot_code = str(player.get("slot_code") or player.get("primary_position") or "XI")
    pbbox = draw.textbbox((0, 0), slot_code, font=font_pos)
    pw, ph = pbbox[2] - pbbox[0], pbbox[3] - pbbox[1]
    px0, py0 = cx - radius - 6, cy - radius - 6
    draw.rounded_rectangle([px0, py0, px0 + pw + 10, py0 + ph + 6], radius=5, fill=(15, 23, 42), outline=ring_col, width=2)
    draw.text((px0 + 5, py0 + 2), slot_code, fill=(248, 250, 252), font=font_pos)

    # Captain 'C' badge at top-right
    if is_cap:
        cbbox = draw.textbbox((0, 0), "C", font=font_pos)
        cw = cbbox[2] - cbbox[0]
        c_r = max(22, int(radius * 0.44))
        cx0, cy0 = cx + radius - 10, cy - radius - 6
        draw.ellipse([cx0, cy0, cx0 + c_r, cy0 + c_r], fill=(250, 204, 21), outline=(15, 23, 42), width=2)
        draw.text((cx0 + (c_r - cw) // 2, cy0 + 2), "C", fill=(15, 23, 42), font=font_pos)

    # Name plate below circle: Matches web app formatting exactly: "호마리우 (Romário)"
    ko = (player.get("name_ko") or "").strip()
    en = (player.get("name_en") or "").strip()
    if ko and en and ko.lower() != en.lower():
        name_str = f"{ko} ({en})"
    else:
        name_str = ko or en or "선수"

    if len(name_str) > 17:
        name_str = name_str[:16] + "…"

    caps = player.get("official_caps", 30)
    period = player.get("active_period_label") or ""
    caps_txt = f"{caps}경기 · {period}" if period else f"{caps}경기"

    nbbox = draw.textbbox((0, 0), name_str, font=font_name)
    nw, nh = nbbox[2] - nbbox[0], nbbox[3] - nbbox[1]
    sbbox = draw.textbbox((0, 0), caps_txt, font=font_sub)
    sw, sh = sbbox[2] - sbbox[0], sbbox[3] - sbbox[1]

    plate_w = max(nw + 20, sw + 20, int(radius * 2.3))
    plate_h = nh + sh + 12
    ny0 = cy + radius + 4

    # Dark rounded box with subtle border
    draw.rounded_rectangle(
        [cx - plate_w // 2, ny0, cx + plate_w // 2, ny0 + plate_h],
        radius=7,
        fill=(15, 23, 42, 235),
        outline=(51, 65, 85, 240),
        width=2
    )
    draw.text((cx - nw // 2, ny0 + 3), name_str, fill=(255, 255, 255), font=font_name)
    draw.text((cx - sw // 2, ny0 + nh + 5), caps_txt, fill=(148, 163, 184), font=font_sub)

def render_lineup_png(lineup_data: Dict[str, Any], layout: str = "portrait", scale: int = 1) -> bytes:
    """
    layout: 'portrait' (1080x1350) or 'landscape' (1200x675)
    scale: 1 or 2 (high-DPI export)
    """
    base_w, base_h = (1200, 675) if layout == "landscape" else (1080, 1350)
    W, H = base_w * scale, base_h * scale

    # Dark navy theme background matching web canvas (#070b14)
    img = Image.new("RGBA", (W, H), (7, 11, 20, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    kit_p = hex_to_rgb(lineup_data.get("kit_primary_color", "#FACC15"))
    kit_s = hex_to_rgb(lineup_data.get("kit_secondary_color", "#15803D"))
    kit_t = hex_to_rgb(lineup_data.get("kit_text_color", "#0F172A"))
    theme = lineup_data.get("board_color_theme", "classic_emerald")

    f_title = load_korean_font(32 * scale, bold=True)
    f_badge = load_korean_font(18 * scale, bold=True)
    f_meta = load_korean_font(20 * scale, bold=True)
    f_footer = load_korean_font(15 * scale, bold=True)
    f_list_h = load_korean_font(20 * scale, bold=True)
    f_list = load_korean_font(15 * scale, bold=False)

    country_ko = lineup_data.get("country_name_ko", "국가대표")
    country_code = lineup_data.get("country_fifa_code", "FIFA")
    team_name = lineup_data.get("team_name", f"{country_ko} 역대 최강 XI")
    formation_code = lineup_data.get("formation_code", "4-3-3")
    tactical_style = lineup_data.get("tactical_style", "균형형")
    created_date = (lineup_data.get("created_at") or datetime.now().strftime("%Y-%m-%d"))[:10]

    # Clean Top Header: Exact match to web app screenshot: [BR] 브라질 역대 최강 XI (4-3-3)   배치: 11/11명
    header_h = (75 if layout == "landscape" else 95) * scale
    draw.rectangle([0, 0, W, header_h], fill=(11, 17, 32, 255))
    draw.line([0, header_h, W, header_h], fill=(30, 41, 59), width=2 * scale)

    # Country code gold badge
    bx0, by0 = 36 * scale, 22 * scale
    bw, bh = 64 * scale, 50 * scale
    draw.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=8 * scale, fill=kit_p, outline=kit_s, width=2 * scale)
    cbbox = draw.textbbox((0, 0), country_code[:3], font=f_badge)
    cw, ch = cbbox[2] - cbbox[0], cbbox[3] - cbbox[1]
    draw.text((bx0 + (bw - cw) // 2, by0 + (bh - ch) // 2 - 2), country_code[:3], fill=kit_t, font=f_badge)

    # Title
    draw.text((bx0 + bw + 18 * scale, by0 + 7 * scale), team_name, fill=(255, 255, 255), font=f_title)

    # Formation pill
    tbbox = draw.textbbox((0, 0), team_name, font=f_title)
    tw = tbbox[2] - tbbox[0]
    fx0 = bx0 + bw + 18 * scale + tw + 16 * scale
    fbbox = draw.textbbox((0, 0), formation_code, font=f_badge)
    fw, fh = fbbox[2] - fbbox[0], fbbox[3] - fbbox[1]
    draw.rounded_rectangle([fx0, by0 + 8 * scale, fx0 + fw + 18 * scale, by0 + 8 * scale + fh + 12 * scale], radius=6 * scale, fill=(15, 23, 42), outline=(245, 158, 11), width=2 * scale)
    draw.text((fx0 + 9 * scale, by0 + 13 * scale), formation_code, fill=(251, 191, 36), font=f_badge)

    # Right side: 배치: 11/11명
    right_meta = "배치: 11/11명"
    rmbbox = draw.textbbox((0, 0), right_meta, font=f_meta)
    rmw = rmbbox[2] - rmbbox[0]
    draw.text((W - rmw - 36 * scale, by0 + 13 * scale), right_meta, fill=(203, 213, 225), font=f_meta)

    # Footer Bar
    footer_h = (45 if layout == "landscape" else 55) * scale
    fy0 = H - footer_h
    draw.rectangle([0, fy0, W, H], fill=(7, 11, 20, 255))
    draw.line([0, fy0, W, fy0], fill=(30, 41, 59), width=2 * scale)
    footer_left = f"포메이션 {formation_code} · {tactical_style} · {created_date}"
    footer_right = "ALL-TIME XI · 역대 국가대표 드림팀"
    draw.text((36 * scale, fy0 + (footer_h - 18 * scale) // 2), footer_left, fill=(148, 163, 184), font=f_footer)
    rbbox = draw.textbbox((0, 0), footer_right, font=f_footer)
    draw.text((W - (rbbox[2] - rbbox[0]) - 36 * scale, fy0 + (footer_h - 18 * scale) // 2), footer_right, fill=(250, 204, 21), font=f_footer)

    # Pitch Area: Rounded rectangle border exactly like web canvas
    if layout == "landscape":
        pitch_box = (32 * scale, header_h + 16 * scale, int(W * 0.64), fy0 - 16 * scale)
        side_box = (int(W * 0.66), header_h + 16 * scale, W - 32 * scale, fy0 - 16 * scale)
    else:
        pitch_box = (36 * scale, header_h + 18 * scale, W - 36 * scale, fy0 - 18 * scale)
        side_box = None

    draw_football_pitch(draw, pitch_box, theme=theme)

    px0, py0, px1, py1 = pitch_box
    pw, ph = px1 - px0, py1 - py0
    node_r = (36 if layout == "landscape" else 46) * scale

    players = lineup_data.get("players", [])
    for p in players:
        x_pct = float(p.get("x", p.get("custom_x", 50)))
        y_pct = float(p.get("y", p.get("custom_y", 50)))
        cx = int(px0 + (x_pct / 100.0) * pw)
        cy = int(py0 + (y_pct / 100.0) * ph)
        draw_player_node(img, draw, cx, cy, node_r, p, kit_p, kit_s, kit_t)

    # Side squad list in landscape mode
    if side_box is not None:
        sx0, sy0, sx1, sy1 = side_box
        draw.rounded_rectangle([sx0, sy0, sx1, sy1], radius=12 * scale, fill=(15, 23, 42, 240), outline=(51, 65, 85), width=2 * scale)
        draw.text((sx0 + 20 * scale, sy0 + 16 * scale), "STARTING XI (선발 11명 명단)", fill=(250, 204, 21), font=f_list_h)
        ry = sy0 + 52 * scale
        row_h = int((sy1 - ry - 12 * scale) / max(11, len(players)))
        for idx, p in enumerate(players[:11]):
            if idx % 2 == 0:
                draw.rounded_rectangle([sx0 + 12 * scale, ry, sx1 - 12 * scale, ry + row_h - 2], radius=6 * scale, fill=(30, 41, 59, 180))
            slot_lbl = str(p.get("slot_code", ""))
            p_name = f"{p.get('name_ko', '')} ({p.get('name_en', '')})"
            if len(p_name) > 22:
                p_name = p_name[:21] + "…"
            c_mark = " [C]" if p.get("is_captain") else ""
            meta = f"{p.get('official_caps', 30)}경기 {p.get('official_goals', 0)}골"
            draw.text((sx0 + 20 * scale, ry + 6 * scale), f"{slot_lbl:4s}", fill=(56, 189, 248), font=f_badge)
            draw.text((sx0 + 74 * scale, ry + 6 * scale), f"{p_name}{c_mark}", fill=(255, 255, 255), font=f_list)
            mbbox = draw.textbbox((0, 0), meta, font=f_list)
            draw.text((sx1 - (mbbox[2] - mbbox[0]) - 20 * scale, ry + 6 * scale), meta, fill=(148, 163, 184), font=f_list)
            ry += row_h

    # Convert to PNG bytes
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()
