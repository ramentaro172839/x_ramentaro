# -*- coding: utf-8 -*-
"""画像を生成してXに投稿するツール。

使い方:
    # プロンプトの確認だけ(APIを呼ばない)
    python generate_post.py --scene shotengai --time evening --dry-run

    # 画像を生成して out/ に保存
    python generate_post.py --scene station --time morning

    # 生成してそのままXに投稿
    python generate_post.py --scene riverside --time evening --post

    # 人物なしの風景のみ
    python generate_post.py --scene park --time noon --no-person

必要な環境変数:
    GEMINI_API_KEY                       画像生成(Gemini API)
    X_API_KEY / X_API_SECRET             X APIのconsumer key/secret
    X_ACCESS_TOKEN / X_ACCESS_SECRET     Xのユーザーアクセストークン
"""

import argparse
import datetime
import os
import random
import sys
from pathlib import Path

from scenes import SCENES, TIMES, WEATHERS, build_prompt

# NanoBanana Pro。無印NanoBananaなら gemini-2.5-flash-image
DEFAULT_MODEL = "gemini-3-pro-image-preview"

OUT_DIR = Path(__file__).parent / "out"

SCENE_LABELS = {
    "residential": "住宅街の路地",
    "station": "駅前",
    "shotengai": "商店街",
    "park": "公園",
    "riverside": "川沿い",
    "cafe": "喫茶店の前",
}
TIME_LABELS = {
    "morning": "朝",
    "noon": "昼",
    "evening": "夕方",
    "night": "夜",
}


def generate_image(prompt: str, model: str) -> bytes:
    """Gemini APIで画像を1枚生成してPNGバイト列を返す。"""
    from google import genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    resp = client.models.generate_content(model=model, contents=prompt)
    for part in resp.candidates[0].content.parts:
        if part.inline_data is not None:
            return part.inline_data.data
    raise RuntimeError(f"画像が返ってきませんでした: {resp}")


def build_caption(scene: str, time: str) -> str:
    openers = [
        "今日の一枚📷",
        "ふらっと散歩中✨",
        "この時間の空気が好き",
        "なんでもない日の風景",
    ]
    return (
        f"{random.choice(openers)}\n"
        f"{TIME_LABELS[time]}の{SCENE_LABELS[scene]}にて。\n"
        "※画像はAI生成です\n"
        "#AI画像 #AIphoto"
    )


def post_to_x(image_path: Path, text: str) -> str:
    """画像付きポストを投稿してポストIDを返す。"""
    import tweepy

    ck = os.environ["X_API_KEY"]
    cs = os.environ["X_API_SECRET"]
    at = os.environ["X_ACCESS_TOKEN"]
    ats = os.environ["X_ACCESS_SECRET"]

    # メディアアップロードはv1.1、ポスト作成はv2
    api = tweepy.API(tweepy.OAuth1UserHandler(ck, cs, at, ats))
    media = api.media_upload(str(image_path))

    client = tweepy.Client(
        consumer_key=ck, consumer_secret=cs,
        access_token=at, access_token_secret=ats,
    )
    resp = client.create_tweet(text=text, media_ids=[media.media_id])
    return resp.data["id"]


def main() -> int:
    p = argparse.ArgumentParser(description="画像を生成してXに投稿する")
    p.add_argument("--scene", choices=sorted(SCENES), default=None,
                   help="背景シーン(省略時はランダム)")
    p.add_argument("--time", choices=sorted(TIMES), default=None,
                   help="時間帯(省略時はランダム)")
    p.add_argument("--weather", choices=sorted(WEATHERS), default="clear")
    p.add_argument("--no-person", action="store_true", help="人物なしの風景のみ")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--post", action="store_true", help="生成後にXへ投稿する")
    p.add_argument("--dry-run", action="store_true",
                   help="プロンプトと投稿文を表示するだけでAPIを呼ばない")
    args = p.parse_args()

    scene = args.scene or random.choice(sorted(SCENES))
    time = args.time or random.choice(sorted(TIMES))

    prompt = build_prompt(scene, time, args.weather,
                          with_person=not args.no_person)
    caption = build_caption(scene, time)

    print("--- プロンプト ---")
    print(prompt)
    print("--- 投稿文 ---")
    print(caption)

    if args.dry_run:
        return 0

    print(f"--- 生成中 ({args.model}) ---")
    png = generate_image(prompt, args.model)

    OUT_DIR.mkdir(exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = OUT_DIR / f"{stamp}_{scene}_{time}.png"
    image_path.write_bytes(png)
    print(f"保存しました: {image_path}")

    if args.post:
        post_id = post_to_x(image_path, caption)
        print(f"投稿しました: https://x.com/i/status/{post_id}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
