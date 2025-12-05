import google.generativeai as genai
from difficulty_levels import get_conversion_prompt

class NewsConverter:
    def __init__(self, api_key, model_name='gemini-2.5-flash'):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def convert(self, article, level, language):
        prompt = get_conversion_prompt(level, article, language)
        response = self.model.generate_content(prompt)
        
        # 출력 깔끔하게 다듬기
        clean_text = response.text.replace("**", "").replace("##", "").strip()
        return clean_text

    def explain_term(self, term):
        prompt = f"경제 용어 '{term}'의 뜻을 1~2문장으로 아주 쉽게 설명해줘."
        response = self.model.generate_content(prompt)
        return response.text