from logging.config import dictConfig
import logging
import os
from datetime import datetime

tmp = datetime.now().strftime('%Y-%m-%d %H_%M_%S')
dir_path = os.path.dirname(os.path.realpath(__file__))
loggerPath = f'{dir_path}/../../../logs'  # project root directory

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': f'{loggerPath}/debug_{datetime.now().strftime(tmp)}.log',
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file']
    }
})


def writeLog(msg):
    logging.debug(msg)


writeLog('log started: ' + datetime.now().strftime(tmp))
