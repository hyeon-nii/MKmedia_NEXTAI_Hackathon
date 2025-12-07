# 📰 Newfit: AI 기반 맞춤형 뉴스 변환 서비스

> **"뉴스가 어려운 MZ세대를 위해, 기사의 문체와 난이도를 실시간으로 변환해주는 서비스"**
<br>
<br>

## 📖 프로젝트 개요
**Newfit**는 사용자의 문해력 수준에 맞춰 뉴스 기사의 **어휘와 문체**를 5단계로 변환해주는 AI 서비스입니다. 
단순 요약이 아니라, **Few-shot Prompting** 기술을 활용해 특정 페르소나(동화책, 블로그, 전문가 등)로 기사를 재작성(Rewriting)하며, **RAG(검색 증강 생성)** 기술을 통해 어려운 경제 용어를 정확하게 설명해줍니다.
<br>
<br>

## 🚀 핵심 기능 (Key Features)

### 1. 5단계 맞춤형 뉴스 변환 (Style Transfer)
사용자가 선택한 난이도에 따라 기사의 문체와 어휘 수준을 실시간으로 변환합니다.
- **Level 1 (초등 저학년):** 순우리말 사용, 짧은 문장, 친근한 말투 (~해요체)
- **Level 2 (초등 고학년):** 쉬운 일상 어휘, 명확한 표현
- **Level 3 (중학생/표준):** 대중적인 뉴스 표준 문체
- **Level 4 (고등/성인):** 전문 용어 사용, 복합 문장 허용
- **Level 5 (원문):** 변환 없음

### 2. 하이브리드 용어 검색 (Hybrid Term Search)
기사를 읽다가 모르는 용어가 나오면 **RAG 기술**을 활용해 정확한 뜻을 알려줍니다.
- **1단계 (DB 검색):** 기획재정부 시사경제용어 등 3,000+개의 공인된 데이터베이스(Vector DB)를 먼저 검색하여 정확성 확보.
- **2단계 (AI 설명):** DB에 없는 신조어나 일반 용어는 Gemini AI가 문맥에 맞춰 알기 쉽게 설명.
<br>

## 🛠️ 기술 스택 (Tech Stack)

| 구분 | 상세 내용 | 비고 |
| :--- | :--- | :--- |
| **LLM Model** | **Gemini 2.5 Flash** | 고속 텍스트 생성 및 변환 |
| **Embedding** | **text-embedding-004** | 고성능 벡터 변환 모델 |
| **Vector DB** | **FAISS (CPU)** | 로컬 기반 고속 유사도 검색 |
| **Framework** | **LangChain, Python** | RAG 파이프라인 구축 |
| **Data** | 기획재정부 시사경제용어 등 | 신뢰성 있는 공공 데이터 활용 |
<br>

## 📂 파일 및 아키텍처 구조 (Architecture Structure)

본 프로젝트는 모듈성 및 유지보수성을 위해 기능별로 분리되어 있습니다.

```text
EasyNews/
├── data/                   # 엑셀 원본 데이터 (DB 구축을 위한 소스)
├── main.py                 # [실행 진입점]: 사용자 입력 및 전체 루프 관리
├── rag_system.py           # [RAG 엔진]: 엑셀 로딩, FAISS 캐싱, 용어 검색/필터링
├── news_converter.py       # [LLM 엔진]: Gemini 호출, 변환/설명 요청, 후처리
├── difficulty_levels.py    # [PROMPT/FEW-SHOT 데이터]: 5단계 난이도 정의
└── requirements.txt        # 필수 라이브러리 목록
```
<br>

## ⚙️ 설치 및 실행 방법 (Installation)

1. **레포지토리 클론 (Clone)**
   ```bash
   git clone [https://github.com/your-username/EasyNews.git](https://github.com/your-username/EasyNews.git)
   cd EasyNews
   ```

2. **필수 라이브러리 설치**
   ```bash
   pip install -r requirements.txt 
   ```

3. **API 키 설정**
- main.py 파일을 열고 MY_API_KEY 변수에 본인의 Google Gemini API 키를 입력하세요.

4. **실행**
   ```bash
   python main.py
   ```
