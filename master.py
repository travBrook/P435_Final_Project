import config
import msg_pb2, build_msg
import node
import sys, subprocess, time
import selectors
import random



class Master(node.Node):
    # sid 0 means unassigned
    def __init__(self, ip = '', role = 'master'):
        super().__init__(ip, role)
        self.currentRID = 0
        self.replicaRoster = [config.REPLICA1_IP, config.REPLICA2_IP, config.REPLICA3_IP]

    def handle_message(self, cmds):
        #test message
        recv_ip = cmds.ip

        #TODO handle all possible incoming messages

        ### Handle Client message
        if recv_ip not in self.replicaRoster :
            pass
            self.currentRID += 1
            # (rID, [orig_Message, timestamp recv, timestamp processed, total time elapsed])
            self.requests[self.currentRID] = (cmds, time.time(), 0, 0) 

            #Message to send to replica
            toReplica = build_msg.build(self.ip, cmds.consis, cmds.request, 
            cmds.ack, cmds.data, self.l_clock, self.currentRID)

            #TODO send to random? replica. 

            self.start_connections(self.replicaRoster[random.randrange(0, len(self.replicaRoster))], toReplica.SerializeToString())

        ### Handle Replica message
        else : 
        
            if cmds.rID != 0 :
                if cmds.ack == 1:
                    #Answer a successful request to client
                    toClient = build_msg.build(self.ip, cmds.consis, cmds.request, 
                    cmds.ack, cmds.data, cmds.l_Clock, cmds.rID)
                
                elif cmds.ack == 0:
                    #Answer failure of Request to client 
                    pass
                    toClient = build_msg.build(self.ip, cmds.consis, cmds.request,
                    cmds.ack, 'REQUEST FAILURE', self.l_clock, cmds.rID)

                client = self.requests[cmds.rID][0].ip
                self.processed_reqs[cmds.rID] = self.requests.pop(cmds.rID)
                # calculate current time stats
                curr_req = self.processed_reqs[cmds.rID]
                curr_time = time.time()
                proc_time = curr_time - curr_req[1]
                #update processed_reqs
                self.processed_reqs[cmds.rID] = (curr_req[0], curr_req[1], curr_time, proc_time)

                #finalize request by sending to client
                self.start_connections(client, toClient.SerializeToString())

    def run(self): # override from standard node
        self.lsock.bind((self.ip, config.PORT))
        self.lsock.listen()
        self.node_log.write('listening on' + str((self.ip, config.PORT)))
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

        #spawn rep 1
        proc_id = subprocess.Popen([sys.executable, './replica.py', config.REPLICA1_IP, self.ip, 'replica1'])
        self.node_log.write('\n' + 'replica1 spawned')
        #time.sleep(1)

        #spawn rep 2
        proc_id = subprocess.Popen([sys.executable, './replica.py', config.REPLICA2_IP, self.ip, 'replica2'])
        self.node_log.write('\n' + 'replica2 spawned')
        #time.sleep(1)

        #spawn rep 3
        proc_id = subprocess.Popen([sys.executable, './replica.py', config.REPLICA3_IP, self.ip, 'replica3'])
        self.node_log.write('\n' + 'replica3 spawned')

        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            print("caught keyboard interrupt, node exiting")
            # log current and processed requests
            self.node_log.write('Logical clock:' + str(self.l_clock)) 
            self.node_log.write('outstanding requests:') 
            for req in self.requests:
                self.node_log.write('\n' + str(req) + ': ' + str(self.requests[req])) 
            self.node_log.write('processed requests:' + '\n') 
            for req in self.processed_reqs:
                self.node_log.write('\n' + str(req) + ': ' + str(self.processed_reqs[req])) 

            self.node_log.output_log()
        finally:
            self.sel.close()


if(len(sys.argv) == 3):
    print('boot master')
    test = Master(sys.argv[1], sys.argv[2])
    #test = Master(config.MASTER_IP)
    test.run()
else: 
    sys.exit(1)