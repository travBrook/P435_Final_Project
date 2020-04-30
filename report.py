# file: report.py
# author: Dexter Volz
# Takes a dictionary of master requests and outputs into a viewable format.

import logger, msg_pb2

class Report():
    def __init__(self, contents):
        self.log = logger.Logger('report_stats.txt')
        self.log.write('KV Consistency Data Report \n\n')
        #headers
        self.log.write('Request # --- Request Type ----- Request Consistency ------ Request Time(secs)')
        self.log.write('__________________________________________________________________________________')
        
        msg = msg_pb2.Message()
        request_types = {1 : 'Get', 2 : 'Set'}
        consis_types = {1 : 'LINEAR', 2 : 'SEQUENT', 3 : 'CAUSAL', 4 : 'EVENTUAL'}


        for req in contents:
            msg = contents[req][0]
            self.log.write(str(req) + '.                ' + str(request_types[msg.request]) + '                  ' + 
            str(consis_types[msg.consis]) + '              ' + str(contents[req][3]))
            self.log.write('__________________________________________________________________________________')
        self.log.output_log()

