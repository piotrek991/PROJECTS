import json
import asyncio
import random
from email.mime.text import MIMEText

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from typing import Dict, Any
from dotenv import load_dotenv
import smtplib
from smtplib import SMTPAuthenticationError, SMTPException
import os
from email.mime.text import MIMEText

load_dotenv()
class KafkaOperations:
    conf_kafka_p = {'bootstrap_servers': 'localhost:9091'}
    conf_kafka_c = {
        'bootstrap_servers': 'localhost:9091',
        'group_id': 'my_group',
        'auto_offset_reset': 'earliest'
    }
    def __init__(self):
        self.TOPIC = 'track_allegro_t'
        self.producer = AIOKafkaProducer(**self.conf_kafka_p)
        self.consumer = AIOKafkaConsumer(self.TOPIC, **self.conf_kafka_c)
        self.smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        try:
            self.smtp_server.login(os.getenv('KAFKA_EMAIL_SENDER'), os.getenv('GMAIL_APP_PASS'))
        except SMTPAuthenticationError as e:
            print(f"error during login to smtp server: {e}")
            raise e

    async def send_message(self, message: Dict[str, Any]):
        print(f"sending message: {message}")
        await self.producer.send(self.TOPIC, json.dumps(message).encode('utf-8'))
        print(f"sended message: {message}")
        return

    async def produce_messages(self):
        cons_id = random.randint(0, 10000)

        await self.producer.start()
        t_list = list()
        for _ in range(30):
            d_data = {'id': _, 'message': f'message numer {_}', 'producer_id': cons_id}
            t_list.append(self.send_message(d_data))

        await asyncio.gather(*t_list, return_exceptions=False)
        await self.producer.stop()
        return

    async def consume_message_mail(self):
        try:
            await self.consumer.start()
            while True:
                async for msg in self.consumer:
                    msg_content = json.loads(msg.value.decode('utf-8'))
                    print(f"message consumed: {msg_content}")
                    msg_body = f"PRODUCT {{url}} ATTRIBUTE {{msg_attr}} {{add_content}} changes from: {{old}} TO {{new}}"
                    for key, val in msg_content.items():
                        if not isinstance(val, dict):
                            attr_name = list(val.keys()).pop()
                            msg_body_f = msg_body.format(msg_attr=attr_name, add_content=f"IN STORAGE {key}", old=val[attr_name]['old'], new=val[attr_name]['new'], url=val[attr_name]['product_url'])
                        else:
                            msg_body_f = msg_body.format(msg_attr=key, add_content=str(),
                                                         old=val['old'], new=val['new'], url=val['product_url'])
                        msg_mime= MIMEText(msg_body_f)
                        msg_mime['SUBJECT'] = 'PRODUCT CHANGES ALLEGRO'
                        msg_mime['FROM'] = os.getenv('KAFKA_EMAIL_SENDER')
                        msg_mime['TO'] = os.getenv('KAFKA_EMAIL_RECEIVER')

                        try:
                            self.smtp_server.send_message(msg_mime)
                        except SMTPException as e:
                            print(f"during process of sending email : {msg_body_f} error occured: {e}")
                            raise e
        except Exception as e:
            print(f"error during consuming message: {e}")
        finally:
            await self.consumer.stop()

async def main():
    kafka = KafkaOperations()
    consume = asyncio.create_task(kafka.consume_message_mail())
    await asyncio.gather(consume)

if __name__ == '__main__':
   asyncio.run(main())

