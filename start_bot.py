from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import StorageContext, Settings, load_index_from_storage
from flask import Flask, request, jsonify

# Создаем Flask App
app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers'
    return response

@app.route('/api', methods=['POST', 'GET'])
def handle_post():
    # Получаем JSON данные из POST запроса
    data = request.get_json()

    # Задаем вопрос сетке
    response = engine.query(data.get('query'))
    
    # Обрабатываем данные
    response_data = {
        "status": "success",
        "response": str(response)
    }
    
    # Возвращаем JSON ответ
    return jsonify(response_data)

if __name__ == '__main__':
    # Подключаем нейронку
    api_key = "<ваш ключ ProxyAPI>"

    system_prompt = (
        "Ты - помощник для менеджеров компании Хатико. Отвечай только на Русском языке."
        "\nОтвечай подробно, используя документы из контекста и не упускай детали."
        "\nОтветь на вопрос. Если не можешь ответить - НЕ ПРИДУМЫВАЙ ОТВЕТ."
    )

    llm = OpenAI(api_base="https://api.proxyapi.ru/openai/v1", model="gpt-4o-mini", api_key=api_key, max_tokens=2048, system_prompt=system_prompt)
    embed_model = OpenAIEmbedding(api_base="https://api.proxyapi.ru/openai/v1", model="text-embedding-3-large", api_key=api_key)

    # Ставим по умолчанию
    Settings.llm = llm
    Settings.embed_model = embed_model

    # Создаем индекс, ноды, движок запросов
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)

    # Инициализируем движок
    engine = index.as_query_engine(similarity_top_k=4)

    # Запускаем приложение
    app.run(host='0.0.0.0', port=5000)
