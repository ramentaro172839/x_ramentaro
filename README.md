# x_ramentaro

日本の日常風景(+成人の人物)のAI画像を生成して、Xに投稿するツール。

- 画像生成: Gemini API(NanoBanana Pro / `gemini-3-pro-image-preview`)
- 投稿: X API(tweepy)
- プロンプトはテンプレート式: 背景シーン × 時間帯 × 天気 の組み合わせでバリエーションを量産

## セットアップ

```bash
pip install -r requirements.txt
```

環境変数を設定:

| 変数 | 内容 |
| --- | --- |
| `GEMINI_API_KEY` | Google AI Studio のAPIキー |
| `X_API_KEY` / `X_API_SECRET` | X developer portal の consumer key / secret |
| `X_ACCESS_TOKEN` / `X_ACCESS_SECRET` | 投稿するアカウントのアクセストークン(Read and Write権限) |

## 使い方

```bash
# プロンプトと投稿文の確認だけ(APIを呼ばない)
python generate_post.py --scene shotengai --time evening --dry-run

# 画像を生成して out/ に保存
python generate_post.py --scene station --time morning

# 生成してそのままXに投稿
python generate_post.py --scene riverside --time evening --post

# 人物なしの風景のみ
python generate_post.py --scene park --time noon --no-person

# シーン・時間帯を省略するとランダム
python generate_post.py --post
```

シーン: `residential`(住宅街) / `station`(駅前) / `shotengai`(商店街) / `park`(公園) / `riverside`(川沿い) / `cafe`(喫茶店の前)
時間帯: `morning` / `noon` / `evening` / `night`
天気: `clear` / `rain` / `snow`

シーンの追加・調整は `scenes.py` を編集する。

## コンテンツ方針

- 人物は**明らかに成人**(30代前半)・カジュアルな大人の服装・健全な日常スナップに固定(`scenes.py` の `PERSON_BLOCK`)
- 投稿文には「※画像はAI生成です」の表記を必ず含める
