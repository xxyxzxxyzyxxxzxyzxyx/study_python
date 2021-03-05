import os
import sys
import glob
import numpy as np
import pandas as pd

sys.path.append('./')
from dukascopy import dukascopy


class Datacheck(object):
    def __init__(self, logdir):
        self.logdir = logdir
        self.latest = f'{logdir}/latest'
        self.logs = glob.glob(f'{logdir}/*.log')


    def update(self):
        try:
            latest = pd.read_csv(self.latest)
        except FileNotFoundError:
            latest = pd.DataFrame(
                columns=[
                    'request_url',
                    'year',
                    'month',
                    'day',
                    'hour',
                    'status_code',
                    'buffer_size',
                    'execute_time'
                ]
            )

        for logpath in self.logs:
            log = pd.read_csv(logpath)
            os.renames(f'{logpath}', f'{self.logdir}/__old__/{logpath.split("/").pop()}')
            latest = pd.concat([latest, log])

        latestlog = latest.sort_values(
            by=['year', 'month', 'day', 'hour', 'execute_time'],
            ascending=True
        ).drop_duplicates(
            subset=['request_url'],
            keep='last'
        ).reset_index(
            drop=True
        )

        latestlog.to_csv(f'{self.logdir}/latest', index=False)


    def check(self, pair):
        try:
            latest = pd.read_csv(self.latest)
            retry = latest[
                (latest.status_code != 200) & (latest/status_code != 404)
            ][
                ['year', 'month', 'day']
            ].drop_duplicates(
                keep = 'last'
            ).reset_index(
                drop = True
            ).to_numpy()

            for i in retry:
                target = f'{i[0]}{i[1]:02d}{i[2]:02d}'
                dukascopy(pair, target, target, self.logdir)

        except FileNotFoundError:
            print('update latest log first')
