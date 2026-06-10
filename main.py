import os
from rasp_download import YandexStationRasp
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')


def main():
    downloader = YandexStationRasp(api_key, 'ru_RU', 'json')
    downloader.json_save()

if __name__ == '__main__':
    main()