import os
import glob
import pandas as pd


class Datacheck(object):
    def __init__(self, logdir):
        self.logdir = logdir
        self.latest = f'{logdir}/latest'
        self.logs = glob.glob(f'{logdir}/*.log')

    def logsummary(self):
        try:
            latest = pd.read_csv(self.latest)
        except FileNotFoundError:
            latest = pd.DataFrame(columns=['request_url', 'year', 'month', 'day', 'hour', 'status_code', 'buffer_size'])

        for logpath in logs:
            log = pd.read_csv(logpath)
            os.renames(f'{i}', f'{self.logdir}/old/{logpath.split("/").pop()}')
            latest = pd.concat([latest, log])
