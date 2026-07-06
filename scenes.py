# -*- coding: utf-8 -*-
"""プロンプトの部品定義。

人物ブロックは「明らかに成人・カジュアルな大人の服装・健全な日常スナップ」で
固定し、シーン/時間帯/天気を組み合わせてバリエーションを作る。
"""

# 人物の描写(全プロンプト共通)。
# 年齢・服装・構図を成人向けの健全なスナップに固定する。
PERSON_BLOCK = (
    "30代前半の日本人女性。落ち着いたカジュアルな大人の服装"
    "(例:ロングスカートとブラウス、ジーンズとニット、ワイドパンツとシャツなど)。"
    "自然な立ち姿や歩いている姿で、表情は柔らかい微笑み。"
    "性的な強調のない、健全な日常のスナップ写真。"
)

# 背景シーン。手前・中景・遠景を書くと奥行きが出る。
SCENES = {
    "residential": (
        "日本の郊外の住宅街の路地。手前にアスファルトのひび割れと側溝、"
        "中景に電柱と絡み合う電線、ブロック塀と植木鉢、"
        "遠景に低層の家並みと霞んだ空。"
    ),
    "station": (
        "地方都市の駅前ロータリー。手前にタイル張りの歩道と点字ブロック、"
        "中景にバス停の標識と駐輪場の自転車の列、遠景に駅舎と看板。"
    ),
    "shotengai": (
        "日本のアーケード商店街。店々の看板の蛍光灯やLEDの明かり、"
        "手前にステンレスの手すり、中景に飲食店の光、"
        "遠景はアーケードの奥に消えていく光の列。雑多な看板や自販機など"
        "生活感のあるディテールを豊かに。"
    ),
    "park": (
        "都市公園の遊歩道。手前にベンチと落ち葉、中景に街灯と植え込み、"
        "遠景に木々の間から見えるビル群。"
    ),
    "riverside": (
        "川沿いの土手の遊歩道。手前に草むらとフェンス、中景に橋と川面の反射、"
        "遠景に対岸の街並みと空。"
    ),
    "cafe": (
        "街角の喫茶店の前。手前に石畳の歩道、中景に店のガラス窓と手書きの看板、"
        "遠景に街路樹と通りの奥行き。"
    ),
}

TIMES = {
    "morning": "薄曇りの朝の柔らかい光。",
    "noon": "昼の拡散光。曇りの日の均一な明るさ。",
    "evening": "夕暮れ。空はオレンジから藍色へのグラデーション、街の明かりが灯り始める。",
    "night": "夜。街灯と看板の明かりが主光源で、少しノイズ感のある夜スナップ。",
}

WEATHERS = {
    "clear": "",
    "rain": "小雨上がり。濡れた路面に光が反射している。",
    "snow": "小雪がちらつき、路面にうっすら雪が積もっている。",
}

# 写真としての質感を決める共通の締め。
STYLE_BLOCK = (
    "iPhoneで手持ち撮影した何気ないスナップ写真のような実写風。"
    "自然な色味で彩度は控えめ。広告写真のような完璧さはなく、"
    "ありふれた日常の記録のような一枚。縦長構図。"
)


def build_prompt(scene: str, time: str, weather: str = "clear",
                 with_person: bool = True) -> str:
    """シーン・時間帯・天気からプロンプトを組み立てる。"""
    if scene not in SCENES:
        raise KeyError(f"unknown scene: {scene} (choices: {', '.join(SCENES)})")
    if time not in TIMES:
        raise KeyError(f"unknown time: {time} (choices: {', '.join(TIMES)})")
    if weather not in WEATHERS:
        raise KeyError(f"unknown weather: {weather} (choices: {', '.join(WEATHERS)})")

    parts = [SCENES[scene], TIMES[time]]
    if WEATHERS[weather]:
        parts.append(WEATHERS[weather])
    if with_person:
        parts.append(PERSON_BLOCK)
    else:
        parts.append("人物なし。")
    parts.append(STYLE_BLOCK)
    return "".join(parts)
