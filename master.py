import config
import msg_pb2, build_msg
import node
import sys, subprocess, time
import selectors

class Master(node.Node):
    # sid 0 means unassigned
    def __init__(self, ip = '', role = 'master'):
        super().__init__(ip, role)

    def handle_message(self, cmds):
        #test message
        recv_ip = cmds.ip
        msg = build_msg.build(self.ip, 0, 0, 0, 'I hear ya',1)
        self.node_log.write('\n Data outbound: \n')
        self.node_log.write(str(msg))
        self.start_connections(recv_ip, config.PORT, 1, msg.SerializeToString())

        #TODO handle all possible incoming messages

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