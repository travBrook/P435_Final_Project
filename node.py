# file name: node.py
# author: Dexter Volz
# description: general node worker class. the meat and potatoes of this program/library
# 

import config, logger, build_msg, msg_pb2
import socket, os, signal, subprocess, selectors, types, sys, time
import ast


#takes a string and builds a sort list of tuples. keys are the individual words and the values
# indicate the frequency. All pairs will have a value of 1 after being output by this func

class Node():
    # sid 0 means unassigned
    def __init__(self, ip = '', role = 'node'):
        self.pid = os.getpid()
        self.ip = ip
        self.role = role
        self.data = ''
        self.l_clock = 0

        #socket stuffs
        self.sel = selectors.DefaultSelector()
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.events = selectors.EVENT_READ | selectors.EVENT_WRITE


        #kick off log
        self.node_log = logger.Logger('log.txt', '', self.role)
        self.node_log.write('Im Alive \n')

    def kill(self):
        #final msg to master
        #death_letter = msg_pb2.Slave()
        #death_letter = build_msg.build_slave(self.sid, self.master_ip, self.ip, self.pid, 4, 'goodnight master', 0)
        # send death letter and kill self
        #self.start_connections(self.master_ip, config.PORT, 1, death_letter.SerializeToString())
        self.node_log.write('and now I sleep')
        self.node_log.output_log()
        os.kill(self.pid, 0)
    
    def transmit_data(self, ip, consis, request, ack, data): #data should be string
        data_in =  data
        self.node_log.write('\nsplit input data: \n' + str(data_in))
        data_out = list()
        tmp = ''
        i = 0
        for word in data_in:
            tmp += str(word)
            i += 1
            if(i % config.item_max == 0): #different from master
                data_out.append(tmp)
                tmp = ''
        data_out.append(tmp)
        self.node_log.write('\nOutbound data: \n' + str(data_out))
        print(str(data_out))
        self.node_log.write('\nNum Chunks: \n' + str(len(data_out)))
        for chunk in data_out:
            outb_msg = msg_pb2.Message()
            outb_msg = build_msg.build(ip, consis, request, ack, str(chunk), len(data_out))
            self.start_connections(ip, config.PORT, 1, outb_msg.SerializeToString())

        #TODO **** Update with new proto

        return 1

    # this method is meant to be overridden
    def handle_message(self, cmds):
        raise NotImplementedError('Error: Subclass has not implemented handle_message method')


    # *** SERVER Defs ***

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        self.connected_ip = addr[0] # store ip of machine we are connected to
        #self.node_log.write('accepted connection from' + str(addr))
        conn.setblocking(False)
        data = types.SimpleNamespace(connid = conn, addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        #self.node_log.write('\nService connection invoked')
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                


                #who is the msg coming from?
                #self.node_log.write('\nConnected ip:' + self.connected_ip)
                cmds = msg_pb2.Message() 
                try:
                    cmds.ParseFromString(recv_data)
                    self.node_log.write(str(cmds))
                except:
                    self.node_log.write("\nerror cmds: " + repr(cmds))
                    self.node_log.write('\nmessage error: either not a proto buffer or incorrect type')

                #TODO do stuff with commands (cmds)
                self.handle_message(cmds)



            else:
                self.node_log.write('closing connection to' + str(data.addr))
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                #self.node_log.write('[Server] sending' + repr(data.outb) + 'to' + str(data.addr))
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]

    def start_connections(self, host, open_msg): # open_msg has to be in bytes
        server_addr = (host, config.PORT)
        for i in range(0, 1):
            connid = i + 1
            self.node_log.write('starting connection' + str(connid) + 'to' + str(server_addr))
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            sock.connect_ex(server_addr)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            data = types.SimpleNamespace(connid = connid, addr=server_addr, inb=b'', outb=b'')
            data.outb += open_msg
            self.sel.register(sock, events, data=data)

    def run(self):
        self.lsock.bind((self.ip, config.PORT))
        self.lsock.listen()
        self.node_log.write('listening on' + str((self.ip, config.PORT)))
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

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

#if(len(sys.argv) > 2):
#    test = Node(sys.argv[1], sys.argv[2])
#    test.run()

#test = Node('127.0.0.21', 'replica1')
#test.run()


'''
output = wc_map('hey boy you there you dingus boy you')
print(output)
red_output = wc_reduce(output)
print(red_output)
'''    

