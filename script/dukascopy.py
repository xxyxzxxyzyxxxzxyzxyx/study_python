import csv
import requests
import struct
import pandas as pd
from datetime import date, datetime, timedelta
from io import BytesIO, DEFAULT_BUFFER_SIZE
from lzma import LZMADecompressor, LZMAError, FORMAT_AUTO


class Dukascopy(object):
    def __init__(self, pair, year, month, day):
        self.pair = pair
        self.year = year
        self.month = month
        self.day = day
        self.urls = [
            f'https://www.dukascopy.com/datafeed'
            f'/{pair}/{year}/{month:02d}/{day:02d}/{hour:02d}'
            f'h_ticks.bi5'
            for hour in range(0, 24)
        ]


    def get_requests(self):
        request_day = BytesIO()
        check = []

        for url in self.urls:
            request_hour = BytesIO()
            request = requests.get(url)
            check_request = request.status_code
            check_buffer = 0

            if check_request == 200:
                for request_buffer in request.iter_content(DEFAULT_BUFFER_SIZE):
                    request_hour.write(request_buffer)

                buffer_hour = request_buffer.getbuffer()
                check_buffer = len(buffer_hour)

                if 0 < check_buffer:
                    request_day.write(buffer_hour)
                else:
                    pass

            else:
                pass

            check.append((url, check_request, check_buffer))