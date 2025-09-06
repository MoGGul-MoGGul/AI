# AI/app/langchain_pipe.py

import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import OpenAIEmbeddings

from app.ai_utils import summarize_and_tag

load_dotenv()

def run_langchain_pipeline(raw_text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents([raw_text])

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    conn = os.getenv("PGVECTOR_CONNECTION_STRING") or os.getenv("DB_URL")
    
    PGVector.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="tip_data",
        connection_string=conn
    )

    summary = ""
    tag_list = []
    title = ""
    try:
        summary_and_tags = summarize_and_tag(raw_text)
        summary = summary_and_tags["summary"]
        title = summary_and_tags["title"]
        tag_list = summary_and_tags["tags"]

    except Exception as e:
        print(f"[AI 요약/태그 생성 중 오류] {e}")


    return {
        "chunks": len(docs),
        "title": title,
        "summary": summary,
        "tags": tag_list
    }