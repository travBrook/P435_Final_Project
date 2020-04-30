# file: report.py
# author: Dexter Volz
# Takes a dictionary of master requests and outputs into a viewable format.

import logger, msg_pb2

class Report():
    def __init__(self, contents):
        self.log = logger.Logger('report_stats.txt')
        self.log.write('KV Consistency Data Report \n\n')
        self.log.write('Request # --- Request Type ----- Request Consistency ------ Request Time')
        for req in contents:
            self.log.write(str(req) + ' ' + str(contents[req][0].request) + ' ' + str(contents[req][0].consis) + str(contents[req][3]))
        self.log.output_log()

