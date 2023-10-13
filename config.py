import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class GeneralConfig:
    KAFKA_TOPIC: str = os.getenv('KAFKA_TOPIC')
    KAFKA_BROKER: str = os.getenv('KAFKA_BROKER')


def get_config() -> GeneralConfig:
    return GeneralConfig()
