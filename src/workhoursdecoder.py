import json
from datetime import timedelta, datetime
from pytz import timezone


class WorkhoursDecoder(json.JSONDecoder):
    def default(self, dct):
        brussels = timezone('Europe/Brussels')
        if 'days' in dct and 'seconds' in dct:  # to decode current json files
            return timedelta(days=dct['days'], seconds=dct['seconds'])
        if 'last_updated' in dct and 'time' in dct and 'price' in dct:

            decodedjson = {}
            decodedjson['time'] = dct['time']
            decodedjson['price'] = dct['price']
            decodedjson['last_updated'] = datetime.strptime(
                dct['last_updated'], '%d-%m-%YT%H:%M:%S%z')
            return decodedjson
            '%d-%m-%YT%H:%M:%S'
        if 'last_updated' not in dct and 'time' in dct and 'price' in dct:  # to decode new version 0.0.1 json files
            decodedjson = {}
            decodedjson['time'] = dct['time']
            decodedjson['price'] = dct['price']
            decodedjson['last_updated'] = datetime.utcnow().replace(tzinfo=brussels)

            return decodedjson
        if 'hours' in dct and 'price' in dct:  # to decode old version 0.0.1 json files
            seconds = dct['hours']*60**2
            price = dct['price']
            decodedjson = {'time': timedelta(
                seconds=seconds), 'price': price, 'last_updated': datetime.utcnow().replace(tzinfo=brussels)}
            return decodedjson
        else:
            return dct
