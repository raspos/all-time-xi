# -*- coding: utf-8 -*-
"""
High-Resolution Server-Side PNG Renderer for ALL-TIME XI.
Renders:
1. Best 11 Tactical Board PNG (Portrait 1080x1350 & Landscape 1200x675, plus 2x Retina scale option)
2. AI Virtual Matchup VS Board PNG (1400x900)
Handles external player portraits server-side with caching and graceful jersey/monogram fallback so CORS or missing photos never cause export failure.
"""

import io
import os
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
    candidates = [
        # Windows Fonts
        r"C:\Windows\Fonts\malgunbd.ttf" if bold else r"C:\Windows\Fonts\malgun.ttf",
        r"C:\Windows\Fonts\malgun.ttf",
        r"C:\Windows\Fonts\gulim.ttc",
        # Linux / Docker / Cloud (Nanum, Noto CJK, DejaVu)
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        r"C:\Windows\Fonts\arial.ttf"
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
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
        resp = requests.get(url, headers=headers, timeout=4)
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
        "classic_emerald": ((15, 82, 45), (19, 98, 54), (255, 255, 255, 190)),
        "midnight_tactics": ((15, 23, 42), (22, 33, 58), (56, 189, 248, 180)),
        "worldcup_gold": ((17, 62, 38), (22, 78, 48), (250, 204, 21, 200)),
        "royal_turf": ((12, 74, 62), (16, 92, 78), (241, 245, 249, 190))
    }
    c_dark, c_light, line_col = themes.get(theme, themes["classic_emerald"])

    # Draw alternating grass stripes
    num_stripes = 12
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
    font_name = load_korean_font(max(15, int(radius * 0.52)), bold=True)
    font_sub = load_korean_font(max(12, int(radius * 0.38)), bold=False)
    font_num = load_korean_font(max(16, int(radius * 0.65)), bold=True)
    font_pos = load_korean_font(max(11, int(radius * 0.40)), bold=True)

    # Shadow
    draw.ellipse([cx - radius - 2, cy - radius + 3, cx + radius + 2, cy + radius + 7], fill=(0, 0, 0, 140))

    # Outer ring (gold if captain, red if low suitability, else secondary kit color)
    is_cap = bool(player.get("is_captain"))
    suit = player.get("suitability_status", "적합")
    ring_col = (250, 204, 21) if is_cap else ((248, 113, 113) if "낮음" in suit else kit_secondary)

    draw.ellipse([cx - radius - 4, cy - radius - 4, cx + radius + 4, cy + radius + 4], fill=ring_col)
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=kit_primary)

    # Try portrait image if available and allowed
    portrait = fetch_cached_portrait(player.get("image_url"))
    if portrait is not None:
        size = radius * 2
        mask = Image.new("L", (size, size), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.ellipse((0, 0, size, size), fill=255)
        fitted = ImageOps.fit(portrait, (size, size), centering=(0.5, 0.3))
        canvas.paste(fitted, (cx - radius, cy - radius), mask)
    else:
        # Clean jersey badge fallback with jersey number / initials
        num_str = str(player.get("jersey_number") or player.get("fallback_number") or 10)
        bbox = draw.textbbox((0, 0), num_str, font=font_num)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((cx - tw // 2, cy - th // 2 - 2), num_str, fill=kit_text, font=font_num)

    # Position pill at top-left of circle
    slot_code = str(player.get("slot_code") or player.get("primary_position") or "XI")
    pbbox = draw.textbbox((0, 0), slot_code, font=font_pos)
    pw, ph = pbbox[2] - pbbox[0], pbbox[3] - pbbox[1]
    px0, py0 = cx - radius - 8, cy - radius - 8
    draw.rounded_rectangle([px0, py0, px0 + pw + 12, py0 + ph + 8], radius=6, fill=(15, 23, 42), outline=ring_col, width=2)
    draw.text((px0 + 6, py0 + 3), slot_code, fill=(248, 250, 252), font=font_pos)

    # Captain 'C' badge at top-right
    if is_cap:
        cbbox = draw.textbbox((0, 0), "C", font=font_pos)
        cw = cbbox[2] - cbbox[0]
        c_r = max(24, int(radius * 0.48))
        cx0, cy0 = cx + radius - 12, cy - radius - 8
        draw.ellipse([cx0, cy0, cx0 + c_r, cy0 + c_r], fill=(250, 204, 21), outline=(15, 23, 42), width=2)
        draw.text((cx0 + (c_r - cw) // 2, cy0 + 3), "C", fill=(15, 23, 42), font=font_pos)

    # Name plate below circle
    name_ko = str(player.get("name_ko") or player.get("name_en") or "선수")
    if len(name_ko) > 10:
        name_ko = name_ko[:9] + "…"
    nbbox = draw.textbbox((0, 0), name_ko, font=font_name)
    nw, nh = nbbox[2] - nbbox[0], nbbox[3] - nbbox[1]
    plate_w = max(nw + 24, int(radius * 2.4))
    plate_h = nh + 28
    ny0 = cy + radius + 6
    draw.rounded_rectangle(
        [cx - plate_w // 2, ny0, cx + plate_w // 2, ny0 + plate_h],
        radius=8,
        fill=(15, 23, 42, 240),
        outline=(51, 65, 85),
        width=2
    )
    draw.text((cx - nw // 2, ny0 + 4), name_ko, fill=(255, 255, 255), font=font_name)

    caps_txt = f"{player.get('official_caps', 30)}경기 · {player.get('active_period_label', '')}"
    sbbox = draw.textbbox((0, 0), caps_txt, font=font_sub)
    sw = sbbox[2] - sbbox[0]
    draw.text((cx - sw // 2, ny0 + nh + 7), caps_txt, fill=(148, 163, 184), font=font_sub)

def render_lineup_png(lineup_data: Dict[str, Any], layout: str = "portrait", scale: int = 1) -> bytes:
    """
    layout: 'portrait' (1080x1350) or 'landscape' (1200x675)
    scale: 1 or 2 (high-DPI export)
    """
    base_w, base_h = (1200, 675) if layout == "landscape" else (1080, 1350)
    W, H = base_w * scale, base_h * scale

    img = Image.new("RGBA", (W, H), (10, 15, 29, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    kit_p = hex_to_rgb(lineup_data.get("kit_primary_color", "#FACC15"))
    kit_s = hex_to_rgb(lineup_data.get("kit_secondary_color", "#15803D"))
    kit_t = hex_to_rgb(lineup_data.get("kit_text_color", "#0F172A"))
    theme = lineup_data.get("board_color_theme", "classic_emerald")

    f_title = load_korean_font(34 * scale, bold=True)
    f_sub = load_korean_font(18 * scale, bold=False)
    f_badge = load_korean_font(16 * scale, bold=True)
    f_list_h = load_korean_font(20 * scale, bold=True)
    f_list = load_korean_font(15 * scale, bold=False)
    f_footer = load_korean_font(16 * scale, bold=True)

    country_ko = lineup_data.get("country_name_ko", "국가대표")
    country_code = lineup_data.get("country_fifa_code", "FIFA")
    team_name = lineup_data.get("team_name", f"{country_ko} 역대 최강 XI")
    formation_code = lineup_data.get("formation_code", "4-3-3")
    tactical_style = lineup_data.get("tactical_style", "균형형")
    created_date = (lineup_data.get("created_at") or datetime.now().strftime("%Y-%m-%d"))[:10]

    # Top Header Bar
    header_h = (92 if layout == "landscape" else 125) * scale
    draw.rectangle([0, 0, W, header_h], fill=(15, 23, 42, 255))
    draw.line([0, header_h, W, header_h], fill=kit_p, width=4 * scale)

    # Country badge box in header
    bx0, by0 = 32 * scale, 20 * scale
    bw, bh = 86 * scale, 54 * scale
    draw.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=10 * scale, fill=kit_p, outline=kit_s, width=2 * scale)
    cbbox = draw.textbbox((0, 0), country_code, font=f_list_h)
    draw.text((bx0 + (bw - (cbbox[2] - cbbox[0])) // 2, by0 + (bh - (cbbox[3] - cbbox[1])) // 2 - 2), country_code, fill=kit_t, font=f_list_h)

    draw.text((bx0 + bw + 20 * scale, 18 * scale), f"{country_ko} · {team_name}", fill=(255, 255, 255), font=f_title)
    draw.text((bx0 + bw + 20 * scale, 60 * scale), f"포메이션: {formation_code}  |  전술 스타일: {tactical_style}  |  자격 기준: 공식 A매치 30회 이상", fill=(148, 163, 184), font=f_sub)

    # Footer Bar
    footer_h = (52 if layout == "landscape" else 70) * scale
    fy0 = H - footer_h
    draw.rectangle([0, fy0, W, H], fill=(15, 23, 42, 255))
    draw.line([0, fy0, W, fy0], fill=(51, 65, 85), width=2 * scale)
    footer_left = f"포메이션 {formation_code} · 전술 {tactical_style} · 작성일 {created_date}"
    footer_right = "ALL-TIME XI · 역대 국가대표 드림팀 시뮬레이터"
    draw.text((32 * scale, fy0 + (footer_h - 20 * scale) // 2), footer_left, fill=(203, 213, 225), font=f_footer)
    rbbox = draw.textbbox((0, 0), footer_right, font=f_footer)
    draw.text((W - (rbbox[2] - rbbox[0]) - 32 * scale, fy0 + (footer_h - 20 * scale) // 2), footer_right, fill=(250, 204, 21), font=f_footer)

    # Pitch Area
    if layout == "landscape":
        pitch_box = (32 * scale, header_h + 16 * scale, int(W * 0.64), fy0 - 16 * scale)
        side_box = (int(W * 0.66), header_h + 16 * scale, W - 32 * scale, fy0 - 16 * scale)
    else:
        pitch_box = (36 * scale, header_h + 20 * scale, W - 36 * scale, fy0 - 20 * scale)
        side_box = None

    draw_football_pitch(draw, pitch_box, theme=theme)

    px0, py0, px1, py1 = pitch_box
    pw, ph = px1 - px0, py1 - py0
    node_r = (36 if layout == "landscape" else 48) * scale

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

    out = io.BytesIO()
    img.convert("RGB").save(out, format="PNG", optimize=True)
    return out.getvalue()

def render_ai_comparison_png(team_a: Dict[str, Any], team_b: Dict[str, Any], analysis: Dict[str, Any]) -> bytes:
    W, H = 1400, 920
    img = Image.new("RGBA", (W, H), (10, 15, 29, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    f_title = load_korean_font(30, bold=True)
    f_score = load_korean_font(44, bold=True)
    f_sub = load_korean_font(17, bold=True)
    f_body = load_korean_font(15, bold=False)

    # Top Header
    draw.rectangle([0, 0, W, 95], fill=(15, 23, 42, 255))
    draw.line([0, 95, W, 95], fill=(250, 204, 21), width=3)

    out_sec = analysis.get("expected_outcome", {})
    verdict = analysis.get("final_verdict", {})
    score_str = f"{team_a.get('country_name_ko', 'TEAM A')}  {out_sec.get('team_a_goals', 0)}  :  {out_sec.get('team_b_goals', 0)}  {team_b.get('country_name_ko', 'TEAM B')}"
    sbbox = draw.textbbox((0, 0), score_str, font=f_score)
    draw.text(((W - (sbbox[2] - sbbox[0])) // 2, 14), score_str, fill=(250, 204, 21), font=f_score)

    sub_hdr = f"{team_a.get('team_name')} ({team_a.get('formation_code')})   VS   {team_b.get('team_name')} ({team_b.get('formation_code')})"
    shbbox = draw.textbbox((0, 0), sub_hdr, font=f_sub)
    draw.text(((W - (shbbox[2] - shbbox[0])) // 2, 66), sub_hdr, fill=(226, 232, 240), font=f_sub)

    # Left & Right Tactical Pitches
    pitch_a = (35, 115, 635, 655)
    pitch_b = (765, 115, 1365, 655)
    draw_football_pitch(draw, pitch_a, theme=team_a.get("board_color_theme", "classic_emerald"))
    draw_football_pitch(draw, pitch_b, theme=team_b.get("board_color_theme", "classic_emerald"))

    # VS Emblem in center
    draw.ellipse([660, 345, 740, 425], fill=(250, 204, 21), outline=(15, 23, 42), width=4)
    vbbox = draw.textbbox((0, 0), "VS", font=f_title)
    draw.text((700 - (vbbox[2] - vbbox[0]) // 2, 385 - (vbbox[3] - vbbox[1]) // 2 - 4), "VS", fill=(15, 23, 42), font=f_title)

    for box, tdata in [(pitch_a, team_a), (pitch_b, team_b)]:
        px0, py0, px1, py1 = box
        pw, ph = px1 - px0, py1 - py0
        kp = hex_to_rgb(tdata.get("kit_primary_color", "#FACC15"))
        ks = hex_to_rgb(tdata.get("kit_secondary_color", "#15803D"))
        kt = hex_to_rgb(tdata.get("kit_text_color", "#0F172A"))
        for p in tdata.get("players", []):
            cx = int(px0 + (float(p.get("x", p.get("custom_x", 50))) / 100.0) * pw)
            cy = int(py0 + (float(p.get("y", p.get("custom_y", 50))) / 100.0) * ph)
            draw_player_node(img, draw, cx, cy, 22, p, kp, ks, kt)

    # Bottom AI Analysis Summary Panel
    draw.rounded_rectangle([35, 675, 1365, 865], radius=12, fill=(15, 23, 42, 245), outline=(51, 65, 85), width=2)
    winner_txt = f"AI 최종 판정 우세팀: {verdict.get('winner_team_ko', '백중세')}  |  {out_sec.get('win_tendency_ko', '')}"
    draw.text((55, 692), winner_txt[:95], fill=(56, 189, 248), font=f_sub)

    summary_txt = verdict.get("final_summary_ko", "")
    # Wrap summary_txt into 2 lines
    line1 = summary_txt[:88]
    line2 = summary_txt[88:176] + ("…" if len(summary_txt) > 176 else "")
    draw.text((55, 725), line1, fill=(241, 245, 249), font=f_body)
    if line2:
        draw.text((55, 748), line2, fill=(241, 245, 249), font=f_body)

    # Category Score Pills
    cats = analysis.get("power_comparison", [])
    cx_pill = 55
    for c in cats[:6]:
        lbl = f"{c.get('category_name_ko')}: {c.get('team_a_score')} vs {c.get('team_b_score')}"
        draw.rounded_rectangle([cx_pill, 785, cx_pill + 200, 820], radius=8, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
        draw.text((cx_pill + 12, 793), lbl, fill=(250, 204, 21), font=f_body)
        cx_pill += 212

    disc = "※ 본 결과는 양 팀 선수의 전성기 기록과 전술 상성을 기반으로 생성한 AI 가상 시나리오입니다. | ALL-TIME XI"
    draw.text((55, 835), disc, fill=(148, 163, 184), font=f_body)

    out = io.BytesIO()
    img.convert("RGB").save(out, format="PNG", optimize=True)
    return out.getvalue()
