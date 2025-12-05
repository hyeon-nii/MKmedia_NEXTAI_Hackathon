"""
난이도 레벨 정의 및 프롬프트 템플릿 (5단계 + 예시 포함)
"""
from additional_examples import ADDITIONAL_EXAMPLES

# 난이도 레벨 정의 (1~5단계)
DIFFICULTY_LEVELS = {
    1: {
        "name": "동화책 수준 (초등 저)",
        "description": "어려운 단어는 순우리말, 문장은 아주 짧게 (15자 내외)",
        "features": ["순우리말 사용", "짧은 문장", "친근한 말투(~해요)", "전문용어 금지"]
    },
    2: {
        "name": "초등 고학년 수준",
        "description": "일상 어휘 사용, 명확하고 쉬운 표현 (20~30자)",
        "features": ["일상 어휘", "어려운 한자어 대체", "명확한 문장"]
    },
    3: {
        "name": "중학생 수준 (표준)",
        "description": "일반적인 대중 뉴스 표준 (교과서 어휘)",
        "features": ["표준 어휘", "논리적 흐름", "자연스러운 문체"]
    },
    4: {
        "name": "고등/성인 수준 (고급)",
        "description": "전문 용어와 추상적 개념어 사용 가능",
        "features": ["전문 용어", "복합 문장", "정보 밀도 높음"]
    },
    5: {
        "name": "원문 수준",
        "description": "원문 그대로 유지",
        "features": ["변환 없음"]
    }
}

# 기본 변환 예시 데이터 (서현 님이 주신 것)
CONVERSION_EXAMPLES = {
    "example_1": {
        "original": "경제학에서 수요와 공급의 법칙은 시장 가격 결정의 근본적인 메커니즘이다. 재화의 가격은 수요와 공급이 균형을 이루는 지점에서 형성된다.",
        "level_1": "물건 값은 사고 싶은 사람과 팔고 싶은 사람이 만나서 정해져요. 사고 싶은 사람이 많으면 값이 올라가고, 팔고 싶은 사람이 많으면 값이 내려가요.",
        "level_2": "경제에서 물건 값은 어떻게 정해질까요? 사람들이 사고 싶어 하는 양과 팔고 싶어 하는 양이 만나는 곳에서 값이 정해집니다. 이것을 수요와 공급의 법칙이라고 해요.",
        "level_3": "경제학에서 수요와 공급의 법칙은 시장 가격이 어떻게 정해지는지 설명하는 기본 원리입니다. 물건의 가격은 사람들이 사려는 양(수요)과 파는 사람이 내놓는 양(공급)이 같아지는 곳에서 결정됩니다.",
        "level_4": "경제학에서 수요와 공급의 법칙은 시장 가격이 정해지는 핵심 원리입니다. 상품의 가격은 사려는 양과 파는 양이 딱 맞아떨어지는 지점에서 결정되며, 이것이 자유 시장 경제가 작동하는 기본 방식입니다.",
        "level_5": "경제학에서 수요와 공급의 법칙은 시장 가격 결정의 근본적인 메커니즘이다. 재화의 가격은 수요와 공급이 균형을 이루는 지점에서 형성된다."
    }
}

# 추가 예시 병합
CONVERSION_EXAMPLES.update(ADDITIONAL_EXAMPLES)

def get_conversion_prompt(level: int, original_text: str, language: str = "Korean") -> str:
    """난이도와 언어에 맞는 프롬프트 생성"""
    
    if level == 5:
        return f"원문 그대로 출력:\n{original_text}"

    level_info = DIFFICULTY_LEVELS.get(level, DIFFICULTY_LEVELS[3])
    
    # 🌟 핵심: 프롬프트에 '경제(example_1)' 예시를 박아넣어서 AI가 따라하게 만듦
    example_data = CONVERSION_EXAMPLES["example_1"]
    example_original = example_data["original"]
    example_converted = example_data[f"level_{level}"]

    prompt = f"""
당신은 '문체 변환 전문가'입니다. 아래 [기사 원문]의 내용은 유지하되, [목표 난이도]에 맞춰 **어휘와 문체**를 변환하세요.
(내용을 요약하지 말고, 문장 하나하나를 번역하듯 바꾸세요)

# 목표 난이도: {level}단계 ({level_info['name']})
{level_info['description']}

# 💡 변환 예시 (이것과 비슷한 어휘 수준으로 바꾸세요):
--------------------------------------------------
[원문]: {example_original}
[변환 결과]: {example_converted}
--------------------------------------------------

# ⚠️ 작성 규칙:
1. **내용 유지**: 원문의 팩트(사실관계)를 절대 빠뜨리지 마세요.
2. **어휘 수준**: 위 예시를 참고하여 대상 독자가 이해할 수 있는 단어로 교체하세요.
3. **서식 금지**: **(별표), ## 등 마크다운 기호를 쓰지 마세요.
4. **언어**: {language}로 작성하세요.

[기사 원문]
{original_text}
"""
    return prompt