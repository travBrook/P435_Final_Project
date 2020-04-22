# file name: logger.py
# author: Dexter Volz
# description: Quality of life file to assist in creating log files
# 

import config



class Logger():
    contents = 'This is the first line of the log'

    def __init__(self, filename = 'log.txt', pid = '', role = ''):
        self.filename = filename
        self.pid = pid
        self.role = role
        self.filepath = config.log_path + pid + role + filename 

    def output_log(self):
        f = open(self.filepath, 'w')
        f.write(self.contents)
        f.close()

    def write(self, str):
        self.contents += '\n' + str

    
#test = Logger('log.txt', '123','master')
#test.write('I am the master logger')
#test.output_log()