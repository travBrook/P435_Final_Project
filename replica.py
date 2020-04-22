import config
import msg_pb2, build_msg
import node
import sys
import selectors


class Replica(node.Node):
    # sid 0 means unassigned
    def __init__(self, ip = '', master_ip = '', role = 'replica_unnamed'):
        super().__init__(ip, role)
        self.master_ip = master_ip

        # *** Linearized Consistency Attributes ***
        # TODO

        # *** Sequential Consistency Attributes ***
        # TODO
        
        # *** Causal Consistency Attributes ***
        # TODO
        
        # *** Eventual Consistency Attributes ***
        # TODO but might not be necessary


    def handle_message(self, cmds):
        #TODO handle all possible messages from master
        consistency = cmds.consis
        if(consistency == 0):
            # *** Linearized Consistency Requests ***
            # TODO
            pass
        elif(consistency == 1):
            # *** Sequential Consistency Requests ***
            # TODO
            pass
        elif(consistency == 2):
            # *** Causal Consistency Requests ***
            # TODO
            pass
        elif(consistency == 3):
            # *** Eventual Consistency Requests ***
            # TODO
            pass
        else:
            #incorrect consistency type
            pass
        



    def run(self): #override node run method
        self.lsock.bind((self.ip, config.PORT))
        self.lsock.listen()
        self.node_log.write('listening on' + str((self.ip, config.PORT)))
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)
        #msg = msg_pb2.Message()
        msg = build_msg.build(self.ip, 0, 0, 0, 'hey there Im up',1)
        self.node_log.write('\n Data outbound: \n')
        self.node_log.write(str(msg))
        self.start_connections(self.master_ip, config.PORT, 1, msg.SerializeToString())
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
            self.node_log.write(str(self))
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