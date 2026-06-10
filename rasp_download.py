import json
import os
import requests
import pandas as pd
from logger import get_logger

class YandexStationRasp():
    '''
    lang = ru_RU, ru_UA, uk_RU or uk_UA, 
    format = json or xml
    '''
   
    def __init__(self, api_key, lang, format):
        self.logger = get_logger(__name__)
        try:
            headers = {'Authorization': api_key}
            url = f'https://api.rasp.yandex-net.ru/v3.0/stations_list/?lang={lang}&format={format}'
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            if response.status_code == 200:
                self.response = response
                self.logger.info(response)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            self.response = None
        
    def json_save(self):
        try:
            data = self.response.json()
            station_info =[]
            for country in data['countries']:
                for region in country.get('regions', []):    
                    for settlement in region.get('settlements', []):
                        for station in settlement.get('stations', []):
                            station_info.append({
                                'country_nm': country.get('title'),
                                'settlement_nm':settlement.get('title'),
                                'station_nm': station.get('title'),
                                'direction': station.get('direction'),
                                'yandex_cd': station.get('codes', {}).get('yandex_code'),
                                'station_type': station.get('station_type'),
                                'transport_type': station.get('transport_type'),
                                'long': '' if station.get('longitude') == '' else round(float(station.get('longitude')),3),
                                'lat': '' if station.get('latitude') == '' else round(float(station.get('latitude')),3)
                                # округление используется тк в тз показана таблица, где координаты округлены до 3х знаков
                            })
            df = pd.DataFrame(station_info)
            df.to_csv('stations_info.csv', index=False, encoding="utf-8-sig")
            self.logger.info(f'stations_info download, total = {len(df)} rows')
        except Exception as e:
            self.logger.error(f'Error: {e}')
        