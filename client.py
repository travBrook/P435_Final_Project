import config
import msg_pb2, build_msg
import node
import sys, subprocess, time
import selectors

class Client(node.Node):

    # sid 0 means unassigned
    def __init__(self, ip = '', master_ip = '', role = 'node'):
        super().__init__(ip, role)
        self.master_ip = master_ip

    def handle_message(self, cmds):
        #test message
        recv_ip = cmds.ip
        msg = build_msg.build(self.ip, 0, 0, 0, 'I hear ya',1)
        self.node_log.write('\n Data outbound: \n')
        self.node_log.write(str(msg))
        self.start_connections(recv_ip, config.PORT, 1, msg.SerializeToString())

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


if(len(sys.argv) == 4):
    test = Client(sys.argv[1], sys.argv[2], sys.argv[3])
    test.run()
else:
    sys.exit(2)