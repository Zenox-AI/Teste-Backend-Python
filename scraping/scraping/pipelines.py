# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from confluent_kafka import Producer


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
        self.producer = Producer({'bootstrap.servers': self.kafka_broker})

    def close_spider(self, spider):
        self.process_all_items()
        self.producer.flush()

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def process_all_items(self):
        if self.items:
            content = json.dumps(self.items)
            self.producer.produce(self.kafka_topic, content)
