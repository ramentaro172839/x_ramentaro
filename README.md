# x_ramentaro

X運用を Claude Code Company 方式で回すためのリポジトリ。

## 構成

```
company/
├── CLAUDE.md                      # 社長室：会社全体の方針・共通ルール
├── employee/
│   ├── 01_account-scout/CLAUDE.md # 交流アカ選定社員
│   ├── 02_reply/CLAUDE.md         # リプ周り社員
│   ├── 03_like/CLAUDE.md          # いいね回り社員
│   ├── 04_quote/CLAUDE.md         # 引用ポスト社員
│   ├── 05_post/CLAUDE.md          # ポスト・記事ポスト社員
│   ├── 06_product/CLAUDE.md       # 商品作成社員
│   └── 07_line/CLAUDE.md          # ライン構築社員
└── context/
    ├── about-me.md                # 自分のプロフィール・発信軸（要記入）
    ├── target.md                  # ターゲット情報（要記入）
    └── strategy.md                # X戦略・マネタイズ方針（要記入）
```

## 最初にやること（重要）

`company/context/` の3ファイルを自分の内容で埋める。
ここが空のままだと社員は誰として・誰に向けて・何のために動けばいいか分からない。

## 使い方：3つのモード

### 社長モード（朝・5〜10分）
```
cd company
claude
```
→「今日の運用タスクをリストアップして、各社員への指示書を作成してください」

### 並列モード（日中・10〜15分）
ターミナルを複数開いて各社員を同時に動かす。
```
# ウィンドウ①
cd company/employee/02_reply && claude
# ウィンドウ②
cd company/employee/05_post && claude
```
朝の指示書をコピペして各社員に渡す。

### 個別モード（夕方・5〜10分）
特定の社員フォルダで claude を起動して品質確認・調整。
出力にズレがあればその社員の CLAUDE.md を直す（翌日から永続的に反映される）。

## プラグイン

このリポジトリには cc-company プラグイン（Shin-sibainu/cc-company）が
`.claude/settings.json` で設定済み。新しいセッションで承認すると
`/company` コマンドが使える。

## 注意

社員の出力はすべて「下書き・候補リスト」。X への投稿・フォロー・いいねの
実行は社長（自分）が確認して手動で行う。完全自動のbot運用は X の
ルール（プラットフォーム操作ポリシー）に違反するのでやらない。
