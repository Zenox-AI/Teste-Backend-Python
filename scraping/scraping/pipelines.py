import json
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from confluent_kafka import Producer
import logging

logger = logging.getLogger('MyPipelineLogger')

class DataProcessingPipeline:

    def process_item(self, item, spider):
        if not item.get('populationCountry') or not item.get('areaCountry'):
            raise DropItem("Item faltando campos necessários")

        try:
            item['populationCountry'] = int(item['populationCountry'])
            item['areaCountry'] = float(item['areaCountry'])
        except ValueError:
            raise DropItem("Não foi possível converter os dados")
        return item


class KafkaPipeline:

    def __init__(self, kafka_broker, kafka_topic):
        self.kafka_broker = kafka_broker
        self.kafka_topic = kafka_topic
        self.items = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            kafka_broker=crawler.settings.get('KAFKA_BROKER'),
            kafka_topic=crawler.settings.get('KAFKA_TOPIC')
        )

    def open_spider(self, spider):

        self.file = open("items.jsonl", "w")
        self.file.write("ab re")
        self.producer = Producer({'bootstrap.servers': self.kafka_broker})

    def close_spider(self, spider):
        self.file.close()
        self.process_all_items()
        self.producer.flush()

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def process_all_items(self):
        try:
            if self.items:
                content = json.dumps(self.items)
                teste = self.producer.produce(self.kafka_topic, content)
                logger.info(teste)
                logger.info(f"Enviando dados para o Kafka: {content}")
                self.file.write("Envio para o Kafka")
        except Exception as e:
            self.file.write(str(e))
            logger.error(f"Erro ao enviar dados para o Kafka: {e}")
