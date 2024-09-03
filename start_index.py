from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor, KeywordExtractor, QuestionsAnsweredExtractor
from llama_index.core.ingestion import IngestionPipeline

# Подключаем нейронку
api_key = "<ваш ключ ProxyAPI>"

system_prompt = (
    "Отвечай только на Русском языке и не упускай детали."
)

llm = OpenAI(api_base="https://api.proxyapi.ru/openai/v1", model="gpt-4o-mini", api_key=api_key, max_tokens=2048, system_prompt=system_prompt)
embed_model = OpenAIEmbedding(api_base="https://api.proxyapi.ru/openai/v1", model="text-embedding-3-large", api_key=api_key)

# Ставим по умолчанию
Settings.llm = llm
Settings.embed_model = embed_model

# Загружаем доки и парсим, разбиваем на ноды
reader = SimpleDirectoryReader(input_dir='./docs/')
docs = reader.load_data()

print(f'Загружено {len(docs)} документов')

# SentenceSplitter парсер
parser = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=20,
)
nodes = parser.get_nodes_from_documents(docs)
index = VectorStoreIndex(nodes)

# Pipeline Index
# pipeline = IngestionPipeline(transformations = [
#     SentenceSplitter(chunk_size=512, chunk_overlap=20),
#     TitleExtractor(nodes=5),
#     KeywordExtractor(keywords=10),
#     QuestionsAnsweredExtractor(questions=3)
# ])

# nodes = pipeline.run(documents=docs)
# index = VectorStoreIndex(nodes)

# Сохраняем индекс
index.storage_context.persist(persist_dir="./storage")