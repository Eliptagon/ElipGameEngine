import datetime, sys
import os
import pathlib
from Engine.utils.misc import getTraceback

import colorama
from colorama import Fore, Style
colorama.init()


class logger:
    def __init__(self):
        trans_table = str.maketrans({':':'_', '-':'_', ' ':'_'})
        self.logFileName = 'logs/' + str(datetime.datetime.now()).translate(trans_table).split('.')[0] + '.log'

    def log(self, message: str, severity:str = "FATAL", exception = Exception, exit_code = 0) -> None: #logs and prints out log, can exit with optional exit code if severity = FATAL
        colour_table = {'FATAL': Fore.RED,
                        'ERROR': Fore.CYAN,
                        'WARNING': Fore.GREEN,
                        'INFO': Fore.WHITE}
        if not pathlib.Path('logs/').exists():
            os.mkdir('logs/')
        if severity != 'INFO' and severity != 'WARNING':
            traceback = f'\nSalvaged {getTraceback(exception)}'
        else:
            traceback = ''

        msg = f'\n{colour_table.get(severity, Fore.MAGENTA)}[{str(datetime.datetime.now()).split('.')[0]}] [{severity}] {message}{traceback}, {Style.RESET_ALL}' #single line that formats teh output message
        print(msg, end='')
        logFile = open(self.logFileName, 'a')
        logFile.write(msg)
        logFile.close()
        if severity == 'FATAL':
            sys.exit()


