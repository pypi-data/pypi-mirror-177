# -*- coding: utf-8 -*-
from datetime import datetime

class Log():

    def __init__(self, show=0, gui_log_information=None):
        """ init """
        self.switch(show)
        if gui_log_information:
            self.gui_log_information = gui_log_information

    def _log_noshow(self, *args, **kwargs):
        pass

    def switch(self, show):
        if show == None:
            self.log_debug = self._log_noshow
            self.log_info = self._log_noshow
        elif show == "INFO":
            self.log_debug = self._log_noshow
            self.log_info = print
        else:
            # DEBUG
            self.log_debug = print
            self.log_info = print

    def gui_log_information(self, title, info, tag):
        """ 默认的gui日志函数 """
        pass

    def log_info_format(self, title, info):
        self.log_info("@NOW | @45031{0:^25} | {1}".cformat(title, info))
        self.gui_log_information(title, info, 'blueviolet')

    def log_info_format_err(self, title, info):
        self.log_info("@NOW | @680{0:^25} | {1}".cformat(title, info))
        self.gui_log_information(title, info, 'crimson')

    def log_info_warning_format(self, title, info):
        self.log_info("@NOW | @2448{0:^25} | {1}".cformat(title, info))
        self.gui_log_information(title, info, 'gold')

    def log_debug_format(self, title, info):
        self.log_debug("@NOW | @45031{0:^25} | {1}".cformat(title, info))
        # self.gui_log_information(title, info, 'blueviolet')

    def log_debug_format_err(self, title, info):
        self.log_debug("@NOW | @680{0:^25} | {1}".cformat(title, info))
        # self.gui_log_information(title, info, 'crimson')
