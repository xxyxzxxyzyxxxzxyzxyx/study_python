import csv
import time
import requests
import struct
import pandas as pd
from datetime import date, datetime, timedelta
from io import BytesIO, DEFAULT_BUFFER_SIZE
from lzma import LZMADecompressor, LZMAError, FORMAT_AUTO


def get_requests(pair, year, month, day, fileplace, exectime):
    attempts = 5
    request_day = BytesIO()

    for hour in range(0, 24):
        url = f'https://www.dukascopy.com/datafeed/{pair}/{year}/{month-1:02d}/{day:02d}/{hour:02d}h_ticks.bi5'

        request_hour = BytesIO()
        check_request = 0
        check_buffer = 0

        for attempt in range(attempts):
            try:
                request = requests.get(url)
                check_request = request.status_code
                break
            except Exception as e:
                time.sleep(1*attempt)

        if check_request == 200:
            for request_buffer in request.iter_content(DEFAULT_BUFFER_SIZE):
                request_hour.write(request_buffer)

            buffer_hour = request_hour.getbuffer()
            check_buffer = len(buffer_hour)

            if 0 < check_buffer:
                request_day.write(buffer_hour)

            else:
                pass

        else:
            pass
    
        with open(f'{fileplace}/{exectime}.log', 'a') as f:
            writer = csv.writer(f)
            writer.writerow((url, year, month, day, hour, check_request, check_buffer))


    return request_day.getbuffer()


def decomp_buffer(buffer):
    results = []
    while True:
        decomp = LZMADecompressor(FORMAT_AUTO, None, None)
        result = decomp.decompress(buffer)
        results.append(result)
        buffer = decomp.unused_data
        if not buffer:
            break
    

    return b''.join(results)



def write_ticks(pair, year, month, day, fileplace, tokens):
    ticks = []
    tokensize = 20
    elapsed = 0
    dt = datetime(year, month, day)
    for i in range(0, int(len(tokens)/tokensize)):
        token = struct.unpack('!IIIff', tokens[i*tokensize:(i+1)*tokensize])
        et = token[0]
        if et < elapsed:
            dt += timedelta(hours=1)
        else:
            pass
        tick = (dt+timedelta(milliseconds=et), token[1], token[2], token[3], token[4])
        ticks.append(tick)
        elapsed = et
    
    with open(f'{fileplace}/{pair}{year}{month:02d}{day:02d}.csv'.lower(), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(('time', 'ask', 'bid', 'ask_amount', 'bid_amount'))
        writer.writerows(ticks)


def generate_date(date_begin, date_end):
    begin = datetime.strptime(f'{date_begin}', '%Y%m%d')
    end = datetime.strptime(f'{date_end}', '%Y%m%d')

    for n in range((end - begin).days+1):
        yield begin + timedelta(n)


def dukascopy(pair, date_begin, date_end, fileplace):
    exectime = datetime.now().strftime('%Y%m%d%H%M%S')
    with open(f'{fileplace}/{exectime}.log'.lower(), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(('request_url', 'year', 'month', 'day', 'hour', 'status_code', 'buffer_size'))

    for yyyymmdd in generate_date(date_begin, date_end):
        year = yyyymmdd.year
        month = yyyymmdd.month
        day = yyyymmdd.day

        buffer_day = get_requests(pair, year, month, day, fileplace, exectime)

        if 0 < len(buffer_day):
            tokens_day = decomp_buffer(buffer_day)
            write_ticks(pair, year, month, day, fileplace, tokens_day)
        else:
            pass


