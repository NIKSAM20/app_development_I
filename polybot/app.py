import telebot
from loguru import logger
import os
import requests
from collections import Counter

import time

# from werkzeug.utils import secure_filename
from pymongo import MongoClient, DESCENDING

class Bot:

    def __init__(self, token):
        self.bot = telebot.TeleBot(token, threaded=False)
        self.bot.set_update_listener(self._bot_internal_handler)

        self.current_msg = None

    def _bot_internal_handler(self, messages):
        """Bot internal messages handler"""
        for message in messages:
            self.current_msg = message
            self.handle_message(message)

    def start(self):
        """Start polling msgs from users, this function never returns"""
        logger.info(f'{self.__class__.__name__} is up and listening to new messages....')
        logger.info(f'Telegram Bot information\n\n{self.bot.get_me()}')

        self.bot.infinity_polling()

    def send_text(self, text):
        self.bot.send_message(self.current_msg.chat.id, text)

    def send_text_with_quote(self, text, message_id):
        self.bot.send_message(self.current_msg.chat.id, text, reply_to_message_id=message_id)

    def is_current_msg_photo(self):
        return self.current_msg.content_type == 'photo'

    def download_user_photo(self, quality=2):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :param quality: integer representing the file quality. Allowed values are [0, 1, 2]
        :return:
        """
        if not self.is_current_msg_photo():
            raise RuntimeError(
                f'Message content of type \'photo\' expected, but got {self.current_msg.content_type}')

        file_info = self.bot.get_file(self.current_msg.photo[quality].file_id)
        data = self.bot.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def handle_message(self, message):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {message}')
        self.send_text(f'Your original message: {message.text}')


class QuoteBot(Bot):
    def handle_message(self, message):
        logger.info(f'Incoming message: {message}')

        if message.text != 'Please don\'t quote me':
            self.send_text_with_quote(message.text, message_id=message.message_id)


# ObjectDetectionBot class, inherits from Bot
class ObjectDetectionBot(Bot):

    def detect(self, photo_file):
        # file = request.files['file']
        # filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # p = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        p = photo_file

        logger.info(f'request detect service with {p}')

        logger.info(f'YOLO_URL: {YOLO_URL}')

        # file = open(p, 'rb')

        res = requests.post(f'{YOLO_URL}/predict', files={
            'file': (p, open(p, 'rb'), 'image/png')
        })

        detections = res.json()
        logger.info(f'response from detect service with {detections}')

        # calc summary
        element_counts = Counter([l['class'] for l in detections])
        summary = ''
        for element, count in element_counts.items():
            summary += f"{element}: {count}\n"

        self.send_text(f'{summary}')

        # write result to mongo
        logger.info('writing results to db')
        document = {
            'client_ip': self.current_msg.chat.id,
            'detections': detections,
            'filename': photo_file,
            'summary': summary,
            'time': time.time()
        }

        inserted_document = client['objectDetection']['predictions'].insert_one(document)
        logger.info(f'inserted document id {inserted_document.inserted_id}')


    def handle_message(self, message):
        # logger.info(f'Incoming message: {message}')

        # if message.text != 'Please don\'t quote me':
        #     self.send_text_with_quote(message.text, message_id=message.message_id)

        if self.is_current_msg_photo():
            self.send_text('Got your photo, analyzing it now...')

            # Download the photo
            photo_path = self.download_user_photo()
            logger.info(f'photo_path: {photo_path}')

            # Upload the photo to the object detection service
            self.detect(photo_path)

        else:
            self.send_text('Please send me a photo')


if __name__ == '__main__':
    # TODO - in the 'polyBot' dir, create a file called .telegramToken and store your bot token there.
    #  ADD THE .telegramToken FILE TO .gitignore, NEVER COMMIT IT!!!
    with open('.telegramToken') as f:
        _token = f.read()

    YOLO_URL = 'http://yolo5:8081'

    logger.info(f'Initializing MongoDB connection')

    # We can set MONGO_HOST to be the name of the mongo service in docker-compose.yml (here it's 'mongodb')
    MONGO_HOST = os.getenv('MONGO_HOST', "mongodb")
    
    MONGO_USERNAME = os.getenv('MONGO_USERNAME', "")
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', "")

    # MONGO_URL = 'mongodb://localhost:27017'
    MONGO_URL = f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:27017/'
    
    # client = MongoClient(MONGO_URL, username=f'{MONGO_USERNAME}',password=f'{MONGO_PASSWORD}')
    client = MongoClient(MONGO_URL)

    # Start the bot
    # my_bot = Bot(_token)
    # my_bot = QuoteBot(_token)
    my_bot = ObjectDetectionBot(_token)

    my_bot.start()