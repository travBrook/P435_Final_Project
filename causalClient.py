import config
import msg_pb2, build_msg
import node
import sys, subprocess, time
import selectors

#triples of (consis, request, Data)
messages = []#(4, 1, "key1 ::: value1"), (4, 2, "key1")]

class causalClient(node.Node):

    # sid 0 means unassigned
    def __init__(self, ip = '', master_ip = '', role = 'node'):
        super().__init__(ip, role)
        self.master_ip = master_ip
        self.read_time = 0 # max read time
        self.writes = {} # writes and associated times this client has preformed
    def handle_message(self, cmds):
        #test message
        recv_ip = cmds.ip
        if cmds.request == 1: # write
            newKV = cmds.data.split(" ::: ")
            self.writes[newKV[0]] = cmds.l_Clock
        if cmds.request == 2: # read
            self.read_time = max(self.l_clock, cmds.l_Clock)
        print(self.role + " has mail!")
       #print(str(cmds))


    def run(self): #override node run method
        self.lsock.bind((self.ip, config.PORT))
        self.lsock.listen()
        self.node_log.write('listening on' + str((self.ip, config.PORT)))
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)
        for message in messages:
            
            # if read message, calculate minimum acceptable timestamp
            if message[1] == 2:
                if message[2] in self.writes:
                    wt = self.writes[message[2]]
                else:
                    wt = 0
                ma_Timestamp = max(wt, self.read_time)
                msg = build_msg.build(self.ip, 3, message[1], 1, message[2], self.l_clock, ma_Timestamp =  ma_Timestamp)
            else:    
                msg = build_msg.build(self.ip, 3, message[1], 1, message[2], self.l_clock)
            self.start_connections(self.master_ip, msg.SerializeToString())
            #time.sleep(0.1)

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
            self.node_log.write('Logical clock:' + str(self.l_clock)) 
            self.node_log.output_log()
        finally:
            self.sel.close()

if(len(sys.argv) >= 4):
    test = causalClient(sys.argv[1], sys.argv[2], sys.argv[3])
    #file interpretation
    try:
        f = open(config.input_path + sys.argv[4], 'r')
        for line in f:
            line = line.strip()
            msgList = line.split(', ')
            if len(msgList) == 3 : 
                newMsg = (int(msgList[0]), int(msgList[1]), msgList[2])
                messages.append(newMsg)
            else: 
                raise Exception
        
    except:
        for i in range(4, len(sys.argv)):
            try :
                pass
                msg = sys.argv[i] 
                msgList = msg.split(", ")
                if len(msgList) == 3 : 
                    newMsg = (int(msgList[0]), int(msgList[1]), msgList[2])
                    messages.append(newMsg)
                else : 
                    raise Exception                
            except : 
                pass
                print("Incorrect format for message : " + sys.argv[i])

    test.run()
else:
    sys.exit(2)