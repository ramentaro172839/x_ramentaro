#!/usr/bin/env python3
"""TikTokカルーセル投稿パッケージ生成ツール

使い方:
    python3 scripts/generate_carousel.py content/queue/post_001_quit_signs/slides.json

slides.json の形式:
{
  "slug": "post_001_quit_signs",
  "type": "共感型",              # 共感型 / 情報型 / 体験談型
  "account": "@career_mayoi",
  "eyebrow": "20代のキャリア迷子図鑑",
  "slides": [
    {"kind": "cover", "lead": "もしかして、", "title": "限界の<em>サイン</em><br>出てない？", "sub": "..."},
    {"kind": "point", "n": 1, "total": 7, "label": "サイン", "title": "...", "sub": "..."},
    {"kind": "cta", "title": "...", "body": "...", "dm_box": "...またはnull", "footer_right": "保存して見返す"}
  ],
  "caption": "キャプション本文 #ハッシュタグ",
  "pinned_comment": "固定コメント文"
}

<em>...</em> はアクセント色、<br> は改行。
出力: slides.json と同じディレクトリに img/*.png, caption.txt, comment.txt
"""
import json, os, subprocess, sys, tempfile

CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

BASE_CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:1080px; height:1920px; overflow:hidden; }
body { font-family:'Noto Sans CJK JP', sans-serif; background:#12172b; color:#f5f1e8;
  display:flex; flex-direction:column; padding:96px 84px; position:relative; }
em { font-style:normal; color:#ffc857; }
.eyebrow { font-size:34px; letter-spacing:0.18em; color:#ffc857; font-weight:700; }
.footer { position:absolute; bottom:72px; left:84px; right:84px; display:flex;
  justify-content:space-between; align-items:center; font-size:30px; color:rgba(245,241,232,0.55); }
.watermark { position:absolute; top:40px; right:64px; font-size:400px; font-weight:900;
  color:rgba(255,200,87,0.08); line-height:1; }
.accent { color:#ffc857; font-weight:700; }
.bar { width:120px; height:10px; background:#ffc857; border-radius:6px; margin:48px 0; }
.center { flex:1; display:flex; flex-direction:column; justify-content:center; }
.dmbox { margin-top:64px; background:rgba(255,200,87,0.12); border:3px solid #ffc857;
  border-radius:24px; padding:44px 48px; font-size:42px; line-height:1.7; }
"""

def render_cover(s, meta):
    lead = f'<div style="font-size:64px; color:rgba(245,241,232,0.85); font-weight:700;">{s["lead"]}</div>' if s.get("lead") else ""
    return f"""
    <div class="eyebrow">{meta["eyebrow"]}</div>
    <div class="center">
      {lead}
      <div style="font-size:100px; font-weight:900; line-height:1.3; margin-top:16px;">{s["title"]}</div>
      <div class="bar"></div>
      <div style="font-size:46px; line-height:1.6; color:rgba(245,241,232,0.9);">{s["sub"]}</div>
    </div>
    <div class="footer"><span>{meta["account"]}</span><span class="accent">スワイプ →</span></div>"""

def render_point(s, meta):
    wm = f'<div class="watermark">{s["n"]}</div>' if s.get("n") else ""
    eyebrow = f'{s.get("label","POINT")} {s["n"]}/{s["total"]}' if s.get("n") else s.get("label", meta["eyebrow"])
    return f"""
    {wm}
    <div class="eyebrow">{eyebrow}</div>
    <div class="center">
      <div style="font-size:82px; font-weight:900; line-height:1.4;">{s["title"]}</div>
      <div class="bar"></div>
      <div style="font-size:44px; line-height:1.7; color:rgba(245,241,232,0.78);">{s["sub"]}</div>
    </div>
    <div class="footer"><span>{meta["account"]}</span><span class="accent">スワイプ →</span></div>"""

def render_cta(s, meta):
    dm = f'<div class="dmbox">{s["dm_box"]}</div>' if s.get("dm_box") else ""
    return f"""
    <div class="eyebrow">{s.get("label", "まとめ")}</div>
    <div class="center">
      <div style="font-size:82px; font-weight:900; line-height:1.45;">{s["title"]}</div>
      <div class="bar"></div>
      <div style="font-size:44px; line-height:1.8; color:rgba(245,241,232,0.9);">{s["body"]}</div>
      {dm}
    </div>
    <div class="footer"><span>{meta["account"]}</span><span class="accent">{s.get("footer_right", "保存して見返す")}</span></div>"""

RENDERERS = {"cover": render_cover, "point": render_point, "cta": render_cta}

def main(json_path):
    with open(json_path) as f:
        pkg = json.load(f)
    base = os.path.dirname(os.path.abspath(json_path))
    img_dir = os.path.join(base, "img")
    os.makedirs(img_dir, exist_ok=True)
    meta = {"account": pkg.get("account", "@career_mayoi"),
            "eyebrow": pkg.get("eyebrow", "20代のキャリア迷子図鑑")}

    for i, s in enumerate(pkg["slides"], 1):
        body = RENDERERS[s["kind"]](s, meta)
        html = f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}</style></head><body>{body}</body></html>"
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
            f.write(html); path = f.name
        out = os.path.join(img_dir, f"{i:02d}_{s['kind']}.png")
        subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                        "--screenshot=" + out, "--window-size=1080,1920",
                        "--hide-scrollbars", "--force-device-scale-factor=1",
                        "file://" + path], check=True, capture_output=True)
        os.unlink(path)

    with open(os.path.join(base, "caption.txt"), "w") as f:
        f.write(pkg["caption"] + "\n")
    with open(os.path.join(base, "comment.txt"), "w") as f:
        f.write(pkg["pinned_comment"] + "\n")
    print(f"OK {pkg['slug']}: {len(pkg['slides'])} slides -> {img_dir}")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
