import os
import logging
import json
import random
from dotenv import load_dotenv
from pymilvus import MilvusClient
from pymilvus import model

# 1. 环境与日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()  # 加载 .env 环境变量

# 2. 初始化 OpenAI API
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# 3. 嵌入函数初始化
def init_embedding():
    return model.dense.OpenAIEmbeddingFunction(
        model_name='text-embedding-3-large',
    )

# 4. Milvus 客户端连接
MILVUS_DB = os.getenv("MILVUS_DB_PATH", "text2sql_milvus_sakila.db")
client = MilvusClient(MILVUS_DB)

# 5. 嵌入函数实例化
embedding_fn = init_embedding()

# 6. 评估函数
def evaluate_recall_precision(questions: list, expected_sqls: list):
    correct_count = 0
    total_count = len(questions)

    for question, expected_sql in zip(questions, expected_sqls):
        # 用户提问嵌入
        q_emb = embedding_fn([question])[0]
        logging.info(f"[评估] 问题嵌入完成: {question}")

        # RAG 检索：示例对
        q2sql_hits = retrieve("q2sql_knowledge", q_emb.tolist(), top_k=3, fields=["question","sql_text"])
        retrieved_sqls = [hit.get("entity",{}).get("sql_text","") for hit in q2sql_hits]

        logging.info(f"[评估] 检索结果: {retrieved_sqls}")
        # 检查是否有正确的 SQL 被检索到
        if expected_sql in retrieved_sqls:
            correct_count += 1

    recall = correct_count / total_count if total_count > 0 else 0
    precision = correct_count / len(retrieved_sqls) if retrieved_sqls else 0

    logging.info(f"[评估] 召回率: {recall:.2f}, 精确率: {precision:.2f}")
    return recall, precision

# 7. 检索函数
def retrieve(collection: str, query_emb: list, top_k: int = 3, fields: list = None):
    results = client.search(
        collection_name=collection,
        data=[query_emb],
        limit=top_k,
        output_fields=fields
    )
    logging.info(f"[检索] {collection} 检索结果: {results[0]}")
    return results[0]  # 返回第一个查询的结果列表

# 8. 从 JSON 文件中随机获取数据
def load_random_questions(file_path: str, num_samples: int = 20):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    samples = random.sample(data, num_samples)
    questions = [item['question'] for item in samples]
    sqls = [item['sql'] for item in samples]
    return questions, sqls

# 9. 程序入口
if __name__ == "__main__":
    # 从 JSON 文件中加载随机问题和 SQL
    questions, expected_sqls = load_random_questions("90-文档-Data/sakila/q2sql_pairs.json", num_samples=20)

    # 评估召回率和精确率
    evaluate_recall_precision(questions, expected_sqls)
