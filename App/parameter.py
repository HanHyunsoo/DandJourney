Banned_Word = [
      "blood", "bloodbath", "crucifixion", "bloody", "flesh", "bruises", "car crash", "corpse", "crucified", "cutting", "decapitate", "infested", "gruesome", "kill", "infected", "sadist", "slaughter", "teratoma", "tryphophobia", "wound", "cronenberg", "khorne", "cannibal", "cannibalism", "visceral", "guts", "bloodshot", "gory", "killing", "surgery", "vivisection", "massacre", "hemoglobin", "suicide",
      "ahegao", "pinup", "ballgag", "playboy", "bimbo", "pleasure", "bodily fluids", "pleasures", "boudoir", "rule34", "brothel", "seducing", "dominatrix", "seductive", "erotic", "fuck", "sensual", "hardcore", "sexy", "hentai", "shag", "horny", "shibari", "incest", "smut", "jav", "succubus", "jerk off king at pic", "thot", "kinbaku", "transparent", "legs spread", "twerk", "making love", "voluptuous", "naughty", "wincest", "orgy", "sultry", "xxx", "bondage", "bdsm", "dog collar", "slavegirl", "transparent", "translucent",
      "arse", "labia", "ass", "mammaries", "badonkers", "minge", "big ass", "mommy milker", "booba", "nipple", "booty", "oppai", "bosom", "organs", "breasts", "ovaries", "busty", "penis", "clunge", "phallus", "crotch", "sexy female", "dick", "skimpy", "girth", "thick", "honkers", "vagina", "hooters", "veiny", "knob",
      "no clothes", "au naturale", "no shirt", "bare chest", "nude", "barely dressed", "bra", "risqué", "clear", "scantily", "clad", "cleavage", "stripped", "full frontal", "unclothed", "invisible clothes", "wearing nothing", "lingerie", "with no shirt", "naked", "without clothes on", "negligee", "zero clothes",
      "taboo", "fascist", "nazi", "prophet mohammed", "slave", "coon", "honkey",
      "drugs", "cocaine", "heroin", "meth", "crack",
      "torture", "disturbing", "farts", "fart", "poop", "warts", "shit", "brown pudding", "bunghole", "vomit", "voluptuous", "seductive", "sperm", "hot", "sexy", "sensored", "censored", "silenced", "deepfake", "inappropriate", "pus", "waifu", "mp5", "succubus", "1488", "surgery"
    ]

DjPromptDic = {
    "Version1":[
        {"name": "prompt", "description": "이미지 매개 변수", "type": "str", "required": True},
    ],
    "Version2":[
        {"name": "prompt", "description": "이미지 매개 변수", "type": "str", "required": True},
    ],
    "Version3":[
        {"name": "prompt", "description": "이미지 매개 변수", "type": "str", "required": True},
    ],
    "Version4":[
        {"name": "prompt", "description": "이미지 매개 변수", "type": "str", "required": True},
        {"name": "no", "description": "마스크 분류 용어모음", "type": "str", "required": False},
        {"name": "image", "description": "참조 이미지", "type": "Attachment", "required": False},
    ],
    "Version5":[
        {"name": "prompt", "description": "이미지 매개 변수", "type": "str", "required": True},
        {"name": "area", "description": "이미지 비율(1:2-2:1)", "type": "str", "required": False},
        {"name": "no", "description": "마스크 분류 용어모음", "type": "str", "required": False},
        {"name": "quality", "description": "이미지 품질(0.25-2.0)", "type": "float", "required": False, "max": 2.0, "min": 0.25},
        {"name": "stylize", "description": "스타일화된 매개변수(0-1000)", "type": "int", "required": False, "max": 1000, "min": 0},
        {"name": "niji", "description": "애니메이션", "type": "int", "required": False, "choice": {"niji 4 (지원되지 않음stylize)": 4,"niji 5": 5}},
        {"name": "seed", "description": "이미지 토런트", "type": "int", "required": False, "max":4294967295, "min": 0},
        {"name": "chaos", "description": "이미지 차이 값(0-100)", "type": "int", "required": False, "max":100, "min": 0},
        {"name": "image", "description": "참조 이미지", "type": "Attachment", "required": False},
        {"name": "imageratio", "description": "참조 이미지 무게(0-15)", "type": "int", "required": False, "max":15, "min": 0},
    ],
    "Version5.1":[
        {"name": "prompt", "description": "이미지 매개 변수", "type": "str", "required": True},
        {"name": "area", "description": "이미지 비율(1:2-2:1)", "type": "str", "required": False},
        {"name": "no", "description": "마스크 분류 용어모음", "type": "str", "required": False},
        {"name": "style", "description": "AI레노보", "type": "bool", "required": False, "choice": {"Lenovo 열기": False,"Lenovo 닫기": True}},
        {"name": "quality", "description": "이미지 품질(0.25-2.0)", "type": "float", "required": False, "max": 2.0, "min": 0.25},
        {"name": "stylize", "description": "스타일화된 매개변수(0-1000)", "type": "int", "required": False, "max": 1000, "min": 0},
        {"name": "niji", "description": "애니메이션", "type": "int", "required": False, "choice": {"niji 4 (지원되지 않음stylize)": 4,"niji 5": 5}},
        {"name": "seed", "description": "이미지 토런트", "type": "int", "required": False, "max":4294967295, "min": 0},
        {"name": "chaos", "description": "이미지 차이 값(0-100)", "type": "int", "required": False, "max":100, "min": 0},
        {"name": "image", "description": "참조 이미지", "type": "Attachment", "required": False},
        {"name": "imageratio", "description": "참조 이미지 무게(0-15)", "type": "int", "required": False, "max":15, "min": 0},
    ],
}

DBlendPromptDic = [
    {"name": "image1", "description": "들어오는 그림", "type": "Attachment", "required": True},
    {"name": "image2", "description": "들어오는 그림", "type": "Attachment", "required": True},
    {"name": "dimensions", "description": "이미지 크기", "type": "str", "required": False, "choice": {"2：3 → 하프바디": "--ar 2:3","1：1 → 직사각형": "--ar 1:1","3：2 → 광각": "--ar 3:2"}},
    {"name": "image3", "description": "들어오는 그림", "type": "Attachment", "required": False},
    {"name": "image4", "description": "들어오는 그림", "type": "Attachment", "required": False},
    {"name": "image5", "description": "들어오는 그림", "type": "Attachment", "required": False},
]

DDescribePromptDic = {"name": "image", "description": "들어오는 그림", "type": "Attachment", "required": True},
