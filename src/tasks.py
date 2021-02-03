from parser import parse_pages

from celery import Celery, bootsteps
from kombu import Consumer, Exchange, Queue

news_hash_queue = Queue("news_hash", Exchange("news_hash"), "news_hash")
fresh_news_queue = Queue("fresh_news", Exchange("fresh_news"), "fresh_news")


app = Celery("parser", broker="amqp://rabbitmq:rabbitmq@rabbitmq:5672")


class NewsConsumerStep(bootsteps.ConsumerStep):
    def get_consumers(self, channel):
        return [
            Consumer(
                channel,
                queues=[news_hash_queue],
                callbacks=[self.handler],
                accept=["json"],
            )
        ]

    def handler(self, body, message):
        send_fresh_news.delay(body.get("hash"))
        message.ack()


app.steps["consumer"].add(NewsConsumerStep)


@app.task
def send_fresh_news(last_news=None, producer=None):
    news = parse_pages(last_news)

    if not news:
        return

    with app.producer_or_acquire(producer) as producer:
        for obj in news:
            producer.publish(
                {obj.get("header"): obj},
                serializer="json",
                exchange=fresh_news_queue.exchange,
                routing_key="fresh_news",
                declare=[fresh_news_queue],
                retry=True,
            )
