#!/usr/bin/env python3
"""カルーセル画像生成: HTMLテンプレート→Chromiumスクリーンショット(1080x1920)"""
import os, subprocess, tempfile

CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
OUT = "/home/user/x_ramentaro/assets/carousel_quit_signs_v1"
os.makedirs(OUT, exist_ok=True)

BASE_CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:1080px; height:1920px; overflow:hidden; }
body {
  font-family:'Noto Sans CJK JP', sans-serif;
  background:#12172b;
  color:#f5f1e8;
  display:flex; flex-direction:column;
  padding:96px 84px;
  position:relative;
}
.eyebrow { font-size:34px; letter-spacing:0.18em; color:#ffc857; font-weight:700; }
.footer { position:absolute; bottom:72px; left:84px; right:84px;
  display:flex; justify-content:space-between; align-items:center;
  font-size:30px; color:rgba(245,241,232,0.55); }
.watermark { position:absolute; top:40px; right:64px;
  font-size:400px; font-weight:900; color:rgba(255,200,87,0.08); line-height:1; }
.swipe { color:#ffc857; font-weight:700; }
.bar { width:120px; height:10px; background:#ffc857; border-radius:6px; margin:48px 0; }
"""

def cover():
    return f"""
    <div class="eyebrow">20代のキャリア迷子図鑑</div>
    <div style="flex:1; display:flex; flex-direction:column; justify-content:center;">
      <div style="font-size:64px; color:rgba(245,241,232,0.85); font-weight:700;">もしかして、</div>
      <div style="font-size:104px; font-weight:900; line-height:1.25; margin-top:16px;">
        限界の<span style="color:#ffc857;">サイン</span><br>出てない？
      </div>
      <div class="bar"></div>
      <div style="font-size:46px; line-height:1.6; color:rgba(245,241,232,0.9);">
        仕事を辞めたい人に出ている<br>
        <b style="color:#ffc857;">7つのサイン</b>を集めました。
      </div>
    </div>
    <div class="footer"><span>@career_mayoi</span><span class="swipe">スワイプ →</span></div>
    """

def sign(n, main, sub):
    return f"""
    <div class="watermark">{n}</div>
    <div class="eyebrow">サイン {n}/7</div>
    <div style="flex:1; display:flex; flex-direction:column; justify-content:center;">
      <div style="font-size:84px; font-weight:900; line-height:1.4;">{main}</div>
      <div class="bar"></div>
      <div style="font-size:44px; line-height:1.7; color:rgba(245,241,232,0.75);">{sub}</div>
    </div>
    <div class="footer"><span>@career_mayoi</span><span class="swipe">スワイプ →</span></div>
    """

def last():
    return f"""
    <div class="eyebrow">チェック結果</div>
    <div style="flex:1; display:flex; flex-direction:column; justify-content:center;">
      <div style="font-size:76px; font-weight:900; line-height:1.4;">
        <span style="color:#ffc857;">3つ以上</span>当てはまったら、
      </div>
      <div style="font-size:84px; font-weight:900; line-height:1.4; margin-top:12px;">
        それは<br>&quot;動き出していい&quot;<br>サイン。
      </div>
      <div class="bar"></div>
      <div style="font-size:44px; line-height:1.8; color:rgba(245,241,232,0.9);">
        いま全部やらなくていい。<br>
        まずはこの投稿を<b style="color:#ffc857;">保存</b>して、<br>
        自分のペースで見返してね。
      </div>
      <div style="margin-top:64px; background:rgba(255,200,87,0.12); border:3px solid #ffc857;
                  border-radius:24px; padding:44px 48px; font-size:42px; line-height:1.7;">
        誰かに話を聞いてほしいときは、<br>
        DMで<b style="color:#ffc857;">『相談』</b>と送ってください。
      </div>
    </div>
    <div class="footer"><span>@career_mayoi</span><span class="swipe">保存して見返す</span></div>
    """

signs = [
    ("日曜の夜になると、<br>気分が沈む", "月曜が近づくだけで重くなるのは、心のSOSかもしれない。"),
    ("朝、体が布団から<br>動かない日がある", "それは甘えじゃなくて、疲労が積み重なっているだけ。"),
    ("仕事の話をすると、<br>笑えなくなった", "感情がすり減っているサイン。楽しかった頃を思い出せる？"),
    ("「あと何年これ<br>続けるんだろう」と考える", "未来にワクワクできない場所に、居続けなくていい。"),
    ("休日も仕事のことが<br>頭から離れない", "心が休まる時間がゼロなら、それはもう休日じゃない。"),
    ("頑張っても評価されない<br>気がする", "あなたの問題じゃなくて、環境が合っていないだけかも。"),
    ("気づいたら転職サイトを<br>眺めている", "本音はもう、答えを出してるんじゃない？"),
]

slides = [("01_cover", cover())]
slides += [(f"{i+2:02d}_sign{i+1}", sign(i+1, m, s)) for i, (m, s) in enumerate(signs)]
slides += [("09_cta", last())]

for name, body in slides:
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}</style></head><body>{body}</body></html>"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html); path = f.name
    out = f"{OUT}/{name}.png"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--screenshot=" + out, "--window-size=1080,1920",
                    "--hide-scrollbars", "--force-device-scale-factor=1",
                    "file://" + path], check=True, capture_output=True)
    os.unlink(path)
    print("OK", out)
