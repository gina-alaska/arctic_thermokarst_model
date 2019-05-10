"""
Logger
------
logger.py

simple logger class
"""
from datetime import datetime
from collections import namedtuple
import sys


## LogEntry named tuple
LogEntry = namedtuple(
    'LogEntry',
    ['datetime', 'level', 'message', 'file', 'location', 'line']
)

## Types of log messages
LEVELS = ['info', 'warn', 'error', 'fatal']

class LoggingError (Exception):
    """Raised if error in adding a log message"""

class Logger(object):
    """Logger class
    """
    def __init__ (self, file, also_print=False, exit_on_error=True):
        """Logger class that can be used to track, print, and save logging 
        messages

        Parameters
        ----------
        file: path or None
            default path to save log results to. Can be set to None if there
        is no desired default save location.
        also_print: bool, Default False
        exit_on_error: bool, Default True

        Attributes
        ----------
        log: list of LogEntry 
            the log 
        file: path or None
            default path to save log results to. Can be set to None if there
        is no desired default save location. Can be overridden in save function.
        also_print: bool
            If true, log messages are printed as they are generated.
        exit_on_error: bool
            If true, program will exit on 'error' messages. program 
        will alawas exit on 'fatal messages 
        """
        self.log = []
        self.also_print = also_print
        self.exit_on_error = exit_on_error
        self.file = file
        self.add("Print log entries? " + str(self.also_print))
        self.add("Exit on error? " + str(self.exit_on_error))

    def reset (self):
        """Reset Log 
        """
        self.log = []   

    def add(self, message, level = 'info', in_file=None, at = None, line=None):
        """Add entry to log.
       
        Parameters
        ----------
        message: str
        level: str, default 'info'
            one of the strings in LEVELS
        in_file: str, or None. Default None
            file error generated by
        at: str, or None. Default None
            location (function, class) in file
        line: int, or None. Default None
            line # in file
        

        Raises
        ------
        LoggingError
            if level is not valid 
        """
        if not level.lower() in LEVELS:
            raise LoggingError(
                'Bad level provided: ' + level + '. Use one of ' + str(LEVELS))

        self.log.append(
            LogEntry(
                datetime.now(), 
                level.upper(), 
                str(message), 
                in_file,
                at,
                line
            )
        )
        exit_error = self.exit_on_error and level.lower() == 'error'
        if (exit_error) or level.lower() == 'fatal':
            print('Exiting Due To Error')
            print(self.pretty_log_str(-1, '. '))
            self.save()
            print("Log file saved to", self.file)
            sys.exit(1)


        if self.also_print:
            print(self.pretty_log_str(-1, '. '))

    def pretty_log_str(self, index, sep = ',', write_loc_info=False):
        """convert an entry in log to string.

        Parameters
        ----------
        index: int
            index in to log
        sep: str, default ','
            seperator used in string

        Returns
        -------
        str
            The string for the log item
        """
        entry = self.log[index]
        s = ''
        s += datetime.strftime(entry.datetime, "%Y-%m-%d %H:%M:%S") + sep
        s += entry.level + sep + entry.message + sep
        if write_loc_info:
            s += "File: "
            s += str(entry.file) if not entry.file is None else 'N/A'
            s += sep
            s += "In: "
            s += str(entry.location) if not entry.location is None else 'N/A'
            s += sep
            s += "At line: "
            s += str(entry.line) if not entry.line is None else 'N/A'
        
        return s

    def save(self, filename = None,write_loc_info =True ):
        """save the log to a file

        Parameters
        ----------
        filename: path or None
            override path to save log to.
        
        Returns
        -------
        bool:
            true if a file is saved, false other wise.
        """
        if filename is None:
            filename = self.file

        if filename is None:
            self.add(
                "Logger not configured to save", "warn", "logger.py", "save"
            )
            return False

        with open(filename, 'w') as output:
            for line_no in range(len(self.log)):
                output.write(
                    self.pretty_log_str(line_no, write_loc_info=write_loc_info) +'\n'
                )
        
        return True




def test():
    """
    do some tests
    """
    from inspect import currentframe, getframeinfo
    logger = Logger('logger_test.csv', True, False)
    logger.add("a test info")
    logger.add("next test info", 'info')
    frameinfo = getframeinfo(currentframe())
    logger.add("test warn with loc info", 'warn',  
        frameinfo.filename, frameinfo.function, frameinfo.lineno)
    logger.add("test error", "error")
    logger.add("test fatal", 'fatal')

