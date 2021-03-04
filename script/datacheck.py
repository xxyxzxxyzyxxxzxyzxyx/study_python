import os
import glob
import pandas as pd


class Datacheck(object):
    def __init__(self, logdir):
        self.logdir = logdir
        self.latest = f'{logdir}/latest'
        self.logs = glob.glob(f'{logdir}/*.log')


    def latestlogupdate(self):
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

        for logpath in logs:
            log = pd.read_csv(logpath)
            os.renames(f'{i}', f'{self.logdir}/__old__/{logpath.split("/").pop()}')
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


    def latestlogcheck(self):
        try:
            latest = pd.read_csv(self.latest)
        except FileNotFoundError:
            print('update latest log first')

    
    def 