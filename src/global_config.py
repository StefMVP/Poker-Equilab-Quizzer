import logging
import os
import sys
from sys import platform

localMode = False
if getattr(sys, 'frozen', False):
    currDir = ""
    localMode = False
else:
    currDir = os.path.abspath(os.path.dirname(__file__))
    currDir = os.path.join(currDir, "..//")
    localMode = True




class Config(object):
    # noinspection PyPep8Naming
    def __init__(self, LogLevel, RangePath, *args, **kwargs):
        self.LogLevel = LogLevel
        self.RangePath = RangePath
        self.validate_config()

    def validate_config(self):
        if self.LogLevel is None or self.LogLevel.strip() == "":
            self.LogLevel = logging.INFO
        elif self.LogLevel == "DEBUG":
            self.LogLevel = logging.DEBUG
        elif self.LogLevel == "INFO":
            self.LogLevel = logging.INFO
        else:
            self.LogLevel = logging.INFO


class Const(object):
    def __init__(self):
        self.GlobalConfigPath = os.path.join(currDir, 'global_config.json')
        self.NumberCards = 2
        if platform == "linux" or platform == "linux2":
            self.ClearCommand = 'clear'
        elif platform == "darwin":
            self.ClearCommand = 'clear'
        elif platform == "win32":
            self.ClearCommand = 'cls'
