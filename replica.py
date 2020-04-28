import config
import msg_pb2, build_msg
import node
import sys
import selectors
import os


class Replica(node.Node):
    # sid 0 means unassigned
    def __init__(self, ip = '', master_ip = '', role = 'replica_unnamed'):
        super().__init__(ip, role)
        self.master_ip = master_ip
        self.registry = {}
        self.replicaRoster = [config.REPLICA1_IP, config.REPLICA2_IP, config.REPLICA3_IP]


        self.allConsisDB = {}

        # *** Linearized Consistency Attributes ***
        # TODO
        self.linearDB = {}
        # *** Sequential Consistency Attributes ***
        # TODO
        self.sequentialDB = {}        
        # *** Causal Consistency Attributes ***
        # TODO
        self.causalDB = {}
        # *** Eventual Consistency Attributes ***
        # TODO but might not be necessary
        self.eventualDB = {}

    def handle_message(self, cmds):
        #TODO handle all possible messages from master
        consistency = cmds.consis
        if(consistency == 1):
            # *** Linearized Consistency Requests ***
            # TODO
            pass
        elif(consistency == 2):
            # *** Sequential Consistency Requests ***
            # TODO
            pass
        elif(consistency == 3):
            # *** Causal Consistency Requests ***
            # TODO
            pass
        elif(consistency == 4):
            # *** Eventual Consistency Requests ***
            # TODO
            pass
            self.eventual(cmds)
        else:
            # incorrect consistency type
            pass
            self.eventual(cmds)

    ### No consistency maintained...? Or is this eventual... 
    #   TODO send set request to other replicas
    def eventual(self, cmds):
        pass
        toMaster = msg_pb2.Message()
        if cmds.rID in self.requests.keys() :
            # Do nothing if replica has already seen request
            pass
        else :
            # Handle set request 
            if cmds.request == 1:
                newKV = cmds.data.split(" ::: ")
                if len(newKV) == 2 :

                    self.allConsisDB[newKV[0]] = newKV[1]
                    self.eventualDB[newKV[0]] = newKV[1]

                    # If msg from master, 
                    # then it is the first replica to see it, and we should send a response    
                    if cmds.ip == config.MASTER_IP :
                        toMaster = build_msg.build(self.ip, cmds.consis, cmds.request, 
                        cmds.ack, cmds.data, cmds.l_Clock, cmds.rID)

                    # Send to other replicas if 
                    for ip in self.replicaRoster : 
                        if ip == self.ip :
                            pass
                        else : 
                            toReplica = build_msg.build(self.ip, cmds.consis, cmds.request, 
                            cmds.ack, cmds.data, cmds.l_Clock, cmds.rID)
                            self.start_connections(ip, toReplica.SerializeToString())

                    # Add the request to the requests dictionary
                    self.requests[cmds.rID] = cmds.ip
                            
                else :
                    toMaster = build_msg.build(self.ip, cmds.consis, cmds.request, 
                    0, cmds.data, cmds.l_Clock, cmds.rID)

            # Handle get request
            elif cmds.request == 2:
                if cmds.data in self.allConsisDB:
                    pass
                    toMaster = build_msg.build(self.ip, cmds.consis, cmds.request, 
                    1, self.allConsisDB[cmds.data], cmds.l_Clock, cmds.rID)
                else :
                    toMaster = build_msg.build(self.ip, cmds.consis, cmds.request, 
                    0, cmds.data, cmds.l_Clock, cmds.rID)

            # Send off to master
            self.start_connections(self.master_ip, toMaster.SerializeToString())

    def run(self): #override node run method
        self.lsock.bind((self.ip, config.PORT))
        self.lsock.listen()
        self.node_log.write('listening on' + str((self.ip, config.PORT)))
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)
        #msg = msg_pb2.Message()
        msg = build_msg.build(self.ip, 0, 0, 0, 'hey there Im up', self.l_clock)
        self.node_log.write('\n Data outbound: \n')
        self.node_log.write(str(msg))
        self.start_connections(self.master_ip, msg.SerializeToString())
        print('im running!')
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
            self.node_log.write('Logical clock:' + str(self.l_clock)) 
            self.node_log.write('outstanding requests:' + '\n' + str(self.requests)) 
            self.node_log.write('processed requests:' + '\n' + str(self.processed_reqs)) 
            self.node_log.write("\nAll consistencies DB : " + str(self.allConsisDB))
            self.node_log.write("Linearized consistency DB : " + str(self.linearDB))
            self.node_log.write("Sequential consistency DB : " + str(self.sequentialDB))
            self.node_log.write("Causal consistency DB : " + str(self.causalDB))
            self.node_log.write("Eventual consistency DB : " + str(self.eventualDB))
            self.node_log.output_log()
        finally:
            self.sel.close()

        

print('boot replica')

if(len(sys.argv) > 3):
    test = Replica(sys.argv[1], sys.argv[2], sys.argv[3])
    test.run()
else:
    test = Replica('127.0.0.21', '127.0.0.11', 'replica1')
    test.run()
