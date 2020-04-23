import config
import msg_pb2, build_msg
import node
import sys, subprocess, time
import selectors



class Master(node.Node):
    # sid 0 means unassigned
    def __init__(self, ip = '', role = 'master'):
        super().__init__(ip, role)
        self.currentRID = 0
        self.registry = {}
        self.replicaRoster = [config.REPLICA1_IP, config.REPLICA2_IP, config.REPLICA3_IP]

    def handle_message(self, cmds):
        #test message
        recv_ip = cmds.ip

        #TODO handle all possible incoming messages
        #TODO update l_clocks?

        ### Handle Client message
        if recv_ip not in self.replicaRoster :
            pass
            self.currentRID += 1
            self.registry[self.currentRID] = cmds.ip

            #Message to send to replica
            toReplica = build_msg.build(self.ip, cmds.consis, cmds.request, 
            cmds.ack, cmds.data, cmds.l_Clock, self.currentRID)

            self.node_log.write('\n Data outbound: \n')
            self.node_log.write(str(toReplica))

            #TODO send to random? replica. 
            self.start_connections(self.replicaRoster[0], config.PORT, 1, toReplica.SerializeToString())

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

                self.node_log.write('\n Data outbound: \n')
                self.node_log.write(str(toClient))
                client = self.registry[cmds.rID]
                del self.registry[cmds.rID]
                self.start_connections(client, config.PORT, 1, toClient.SerializeToString())

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
            self.node_log.write(str(self))
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