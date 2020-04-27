import config
import msg_pb2, build_msg
import node
import sys, subprocess, time
import selectors

#triples of (consis, request, Data)
messages = [(0, 1, "key1 ::: value1"), (0, 2, "key1")]

class Client(node.Node):

    # sid 0 means unassigned
    def __init__(self, ip = '', master_ip = '', role = 'node'):
        super().__init__(ip, role)
        self.master_ip = master_ip

    def handle_message(self, cmds):
        #test message
        recv_ip = cmds.ip
        print("Client has mail!")
        #print(str(cmds))


    def run(self): #override node run method
        self.lsock.bind((self.ip, config.PORT))
        self.lsock.listen()
        self.node_log.write('listening on' + str((self.ip, config.PORT)))
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)
        
        for message in messages:
            self.l_clock += 1
            msg = build_msg.build(self.ip, message[0], message[1], 1, message[2], self.l_clock)
            self.start_connections(self.master_ip, msg.SerializeToString())

        print('Client is running')
        
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


### TODO add acceptance of additional args to accept user input of messages
if(len(sys.argv) == 4):
    test = Client(sys.argv[1], sys.argv[2], sys.argv[3])
    test.run()
    #if len(sys.argv) > )
else:
    sys.exit(2)