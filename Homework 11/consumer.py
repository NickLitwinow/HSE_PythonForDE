import json
from collections import defaultdict
from confluent_kafka import Consumer, KafkaException, KafkaError

# Настройки консьюмера
conf = {
    'bootstrap.servers': 'localhost:9092',  # Адрес вашего Kafka брокера
    'group.id': 'my-group',                  # Группа консьюмеров
    'auto.offset.reset': 'earliest',         # Начать чтение с самого начала
    'enable.auto.commit': True               # Автоматическое подтверждение смещений
}

# Инициализация консьюмера
consumer = Consumer(conf)

# Подписка на топик
consumer.subscribe(['example_topic'])

# Словари для подсчета действий
action_counts = defaultdict(lambda: defaultdict(int))
num_events = 1000  # Укажите количество событий для обработки
processed_events = 0

try:
    while True:
        msg = consumer.poll(1.0)  # Ожидание сообщения в течение 1 секунды

        if msg is None:
            # Таймаут, продолжить ожидание
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # Конец раздела
                print(f'Достигнут конец раздела {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')
            elif msg.error():
                # Ошибка
                raise KafkaException(msg.error())
            continue

        # Обработка сообщения
        event = json.loads(msg.value().decode('utf-8'))
        user_id = event.get('user_id')
        action = event.get('action')

        if action in ['click', 'purchase']:
            action_counts[user_id][action] += 1

        processed_events += 1

        # Прерывание после обработки заданного количества событий
        if processed_events >= num_events:
            break

finally:
    # Закрытие консьюмера
    consumer.close()

# Анализ данных
# Находим пользователей с наибольшим количеством кликов и покупок
top_clicks = sorted(action_counts.items(), key=lambda x: x[1]['click'], reverse=True)[:5]
top_purchases = sorted(action_counts.items(), key=lambda x: x[1]['purchase'], reverse=True)[:5]

print("Пользователи с наибольшим количеством кликов:")
for user, actions in top_clicks:
    print(f"User ID: {user}, Clicks: {actions['click']}")

print("\nПользователи с наибольшим количеством покупок:")
for user, actions in top_purchases:
    print(f"User ID: {user}, Purchases: {actions['purchase']}")