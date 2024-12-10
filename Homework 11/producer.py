import json
import random
from datetime import datetime, timedelta
from confluent_kafka import Producer
import time

# Определение доступных действий
actions = ['login', 'logout', 'purchase', 'click']
num_users = 100
num_events = 1000

# Функция генерации события
def generate_event(user_id):
    action = random.choice(actions)
    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 60))
    event = {
        "user_id": user_id,
        "action": action,
        "timestamp": timestamp.isoformat()
    }
    return event

# Генерация данных
data = [generate_event(random.randint(1, num_users)) for _ in range(num_events)]

# Пример первых 5 событий
for event in data[:5]:
    print(json.dumps(event))

# Настройки продюсера
conf = {
    'bootstrap.servers': 'localhost:9092',  # Адрес вашего Kafka брокера
    'client.id': 'python-producer'
}

# Инициализация продюсера
producer = Producer(**conf)

# Функция обратного вызова для обработки результатов отправки
def delivery_report(err, msg):
    if err is not None:
        print(f'Сообщение не доставлено: {err}')
    else:
        print(f'Сообщение доставлено в {msg.topic()} [{msg.partition()}]')

# Отправка данных
for event in data:
    producer.produce(
        'example_topic',  # Название топика
        value=json.dumps(event).encode('utf-8'),
        callback=delivery_report
    )
    # Асинхронная отправка сообщений
    # Можно добавить задержку, если необходимо
    # time.sleep(0.01)

# Ожидание завершения отправки всех сообщений
producer.flush()
print("Данные успешно загружены в топик example_topic.")