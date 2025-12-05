from rag_system import EconomicTermRAG
from news_converter import NewsConverter
import sys

# ==========================================
# 🔑 API 키 입력
MY_API_KEY = "API 키"
# ==========================================

def get_user_input_article():
    print("\n📰 변환할 기사 내용을 붙여넣고 [Enter]를 두 번 치세요 (종료: Ctrl+C):")
    lines = []
    while True:
        try:
            line = input()
        except EOFError: break
        if not line: break
        lines.append(line)
    return "\n".join(lines)

def main():
    if not MY_API_KEY or "여기에" in MY_API_KEY:
        print("❌ 오류: API 키를 입력해주세요!")
        return

    try:
        rag = EconomicTermRAG(MY_API_KEY)
        converter = NewsConverter(MY_API_KEY, model_name='gemini-2.5-flash')
    except Exception as e:
        print(f"❌ 초기화 오류: {e}")
        return

    while True:
        print("\n" + "="*50)
        print("   📰 Easy News : 5단계 문체 변환기")
        print("="*50)

        article = get_user_input_article()
        if len(article.strip()) < 5: continue

        while True:
            print("\n⚙️  난이도를 선택하세요 (1~5):")
            print("   [1] 동화책 수준 (초등 저)")
            print("   [2] 초등 고학년 수준")
            print("   [3] 중학생 수준 (표준)")
            print("   [4] 고등/성인 수준 (고급)")
            print("   [5] 원문 유지")
            
            try:
                level_choice = input("👉 선택: ").strip()
                if level_choice in ['1', '2', '3', '4', '5']:
                    target_level = int(level_choice)
                else:
                    print("⚠️ 기본값(3)으로 설정합니다.")
                    target_level = 3

                lang_input = input("👉 언어 선택 (엔터치면 한국어): ").strip()
                target_lang = lang_input if lang_input else "Korean"
            except:
                break

            print("\n" + "-"*50)
            print(f"🤖 [ {target_level}단계 ] 로 문체를 변환합니다...") 
            
            result = converter.convert(article, target_level, target_lang)
            print("-" * 20 + " [변환 결과] " + "-" * 20)
            print(result)
            print("-" * 50)

            while True:
                print("\n🤔 추가 작업:")
                print("   [1] ❓ 용어 질문하기")
                print("   [2] 🔄 난이도 바꿔서 다시 보기")
                print("   [3] 🆕 새로운 기사 입력")
                print("   [4] 👋 종료")
                
                action = input("👉 선택: ").strip()

                if action == '1':
                    term = input("🔎 궁금한 용어: ")
                    found_terms = rag.search_terms(term, k=3)
                    
                    if found_terms:
                        print(f"\n[📖 전문 용어 사전 결과]")
                        for info in found_terms:
                            print(f"  • {info}")
                    else:
                        print(f"\n[🤖 AI 자동 설명]")
                        print(converter.explain_term(term))
                    
                elif action == '2': break
                elif action == '3': break 
                elif action == '4': sys.exit()
            
            if action == '3': break

if __name__ == "__main__":
    main()