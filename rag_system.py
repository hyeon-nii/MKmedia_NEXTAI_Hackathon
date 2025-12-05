import pandas as pd
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import os
import time

class EconomicTermRAG:
    def __init__(self, google_api_key):
        clean_key = google_api_key.strip()
        os.environ["GOOGLE_API_KEY"] = clean_key
        
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        self.vector_db = None
        self.DB_PATH = "faiss_db_cache"

        if os.path.exists(self.DB_PATH):
            self._load_from_disk()
        else:
            self._build_from_excel()

    def _load_from_disk(self):
        print("💾 저장된 데이터베이스를 불러오는 중...")
        self.vector_db = FAISS.load_local(
            self.DB_PATH, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )

    def _build_from_excel(self):
        print("📚 엑셀 데이터를 읽어오는 중입니다...")
        documents = []

        try:
            # 파일명은 서현님의 실제 파일명과 일치해야 합니다
            df1 = pd.read_excel("data/20251205_시사경제용어사전.xlsx")
            for _, row in df1.iterrows():
                term = str(row['용어'])
                desc = str(row['설명'])
                if term != 'nan' and desc != 'nan':
                    content = f"용어: {term}\n설명: {desc}"
                    documents.append(Document(page_content=content, metadata={"term": term}))
        except Exception as e:
            print(f"⚠️ 엑셀 로드 실패: {e}")

        try:
            df2 = pd.read_excel("data/기획재정부_경제용어_20240905.xlsx")
            for _, row in df2.iterrows():
                term = str(row['경제용어'])
                desc = str(row['용어설명'])
                if term != 'nan' and desc != 'nan':
                    content = f"용어: {term}\n설명: {desc}"
                    documents.append(Document(page_content=content, metadata={"term": term}))
        except:
            pass

        if documents:
            print(f"🧠 총 {len(documents)}개의 용어 학습 시작 (서버 보호 모드)")
            batch_size = 50
            self.vector_db = FAISS.from_documents(documents[:batch_size], self.embeddings)
            time.sleep(1)

            for i in range(batch_size, len(documents), batch_size):
                batch = documents[i : i + batch_size]
                # print(f"   🚀 학습 중... ({i}/{len(documents)})")
                for attempt in range(3):
                    try:
                        self.vector_db.add_documents(batch)
                        time.sleep(1.5)
                        break
                    except:
                        time.sleep(5)
            
            self.vector_db.save_local(self.DB_PATH)
            print("✅ 학습 및 저장 완료!")
        else:
            print("❌ 데이터가 없습니다.")

    def search_terms(self, query_text, k=3):
        """
        유사도 점수(Score)를 확인하여 엉뚱한 결과 필터링
        """
        if not self.vector_db:
            return []
        
        # 점수와 함께 검색 (낮을수록 정확함, 0.5 이상이면 엉뚱한 것)
        results_with_scores = self.vector_db.similarity_search_with_score(query_text, k=k)
        
        terms_info = []
        # 기준점 (이 점수보다 높으면 버림)
        THRESHOLD = 0.48 
        
        print(f"\n   [검색 디버깅] '{query_text}' 결과:")
        for doc, score in results_with_scores:
            if score < THRESHOLD:
                print(f"      ✅ 채택 (점수: {score:.3f}) - {doc.metadata.get('term')}")
                terms_info.append(doc.page_content)
            else:
                print(f"      🗑️ 탈락 (점수: {score:.3f} - 너무 다름) - {doc.metadata.get('term')}")
        
        return terms_info