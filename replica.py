import config
import msg_pb2, build_msg
import node
import sys
import selectors
import os
from queue import PriorityQueue


class Replica(node.Node):
    # sid 0 means unassigned
    def __init__(self, ip = '', master_ip = '', role = 'replica_unnamed'):
        super().__init__(ip, role)
        self.master_ip = master_ip
        self.replicaRoster = [config.REPLICA1_IP, config.REPLICA2_IP, config.REPLICA3_IP]

        self.linearPQ = PriorityQueue() # (original_l_clock, rID)
        self.seqPQ = PriorityQueue() # (original_l_clock, rID)


        # merged database.. should be wild
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
            self.linear(cmds)
        elif(consistency == 2):
            # *** Sequential Consistency Requests ***
            # TODO
            self.sequential(cmds)
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
                if cmds.data in self.eventualDB:
                    pass
                    toMaster = build_msg.build(self.ip, cmds.consis, cmds.request, 
                    1, self.eventualDB[cmds.data], self.l_clock, cmds.rID)
                else :
                    toMaster = build_msg.build(self.ip, cmds.consis, cmds.request, 
                    0, 'Get Failure', self.l_clock, cmds.rID)

            # Send off to master
            self.start_connections(self.master_ip, toMaster.SerializeToString())

    def linear(self, cmds):
        self.tob(cmds)
        return 0

    def sequential(self, cmds):
        if(cmds.request == 1):
            self.tob(cmds)
        else:
            #TODO local get
            pass

        return 0

    #totally ordered broadcast yo
    def tob(self, cmds):
        msgQ = PriorityQueue()
        outb = msg_pb2.Message()

        #check if request is in the dict
        if(cmds.rID in self.requests.keys()):
            # this is an acknowledgement message
            #add to request's msgQ
            msgQ = self.requests[cmds.rID]
            msgQ.put((msgQ.queue[0][0] + cmds.l_Clock, cmds))
            #update requests dict
            self.requests[cmds.rID] = msgQ

        else:
            #this is a command message
            #update local requests dict
            if(cmds.ip == self.master_ip):
                outb = build_msg.build(self.ip, cmds.consis, cmds.request, 1, cmds.data, self.l_clock, cmds.rID)
                msgQ.put((self.l_clock, outb))
                self.requests[cmds.rID] = msgQ
                
                if(cmds.consis == 1):
                    # add to linearPQ
                    self.linearPQ.put((self.l_clock, cmds.rID))
                else:
                    # add to seq
                    self.seqPQ.put((self.l_clock, cmds.rID))
            else:
                msgQ.put((cmds.l_Clock, cmds))
                self.requests[cmds.rID] = msgQ

                if(cmds.consis == 1):
                    # add to linearPQ
                    self.linearPQ.put((cmds.l_Clock, cmds.rID))
                else:
                    # add to seq
                    self.seqPQ.put((cmds.l_Clock, cmds.rID))
        self.broadcast(cmds)
    
    #tob helper
    def broadcast(self,cmds):
        # Check the queues if we have any broadcasting to do        
        # if linear
        

        if(cmds.consis == 1):
            #prevent empty queue
            if(len(self.linearPQ.queue) == 0):
                return 0
            rID = self.linearPQ.queue[0][1]
            msgQ = self.requests[rID]
            top_msg = msgQ.queue[0][1]
            # are we the originator of the next queued message
            if(top_msg.ip == self.ip):
                # all acks are in
                if(len(msgQ.queue) == len(self.replicaRoster)):
                    #remove first element
                    self.linearPQ.get()
                    #if set perform operation
                    if(top_msg.request == 1):
                        newKV = top_msg.data.split(" ::: ")
                        if(len(newKV) == 2):
                            self.allConsisDB[newKV[0]] = newKV[1]
                            self.linearDB[newKV[0]] = newKV[1]
                            outb = build_msg.build(self.ip, 1, 1, 1, 'Set successful', self.l_clock, rID)
                        else:
                            outb = build_msg.build(self.ip, 1, 1, 0, 'Set failure', self.l_clock, rID)
                        
                    else:
                        # perform get
                        if (top_msg.data in self.linearDB):
                            outb = build_msg.build(self.ip, top_msg.consis, top_msg.request, 
                            1, self.linearDB[cmds.data], self.l_clock, top_msg.rID)
                        else:
                            outb = build_msg.build(self.ip, cmds.consis, cmds.request, 
                            0, 'Get Failure', self.l_clock, top_msg.rID)
                    self.start_connections(self.master_ip, outb.SerializeToString())
                    self.broadcast(cmds)
                elif(len(msgQ.queue) == 1):
                    # Broadcast to all
                    for ip in self.replicaRoster : 
                        if ip == self.ip :
                            pass
                        else : 
                            outb = build_msg.build(self.ip, top_msg.consis, top_msg.request, 
                            top_msg.ack, top_msg.data, top_msg.l_Clock, top_msg.rID)
                            self.start_connections(ip, outb.SerializeToString())
            else:
                #check if we need to broadcast ack
                if(len(msgQ.queue) == 1):
                    # Broadcast to all
                    for ip in self.replicaRoster : 
                        if ip == self.ip :
                            pass
                        else : 
                            outb = build_msg.build(self.ip, top_msg.consis, top_msg.request, 
                            top_msg.ack, top_msg.data, self.l_clock, top_msg.rID)
                            self.start_connections(ip, outb.SerializeToString())
                elif(len(msgQ.queue) == 2):
                    #perform operation and remove if we have all acks
                    #remove first element
                    self.linearPQ.get()
                    if(top_msg.request == 1):
                        newKV = top_msg.data.split(" ::: ")
                        if(len(newKV) == 2):
                            self.allConsisDB[newKV[0]] = newKV[1]
                            self.linearDB[newKV[0]] = newKV[1]
                    self.broadcast(cmds)
                    #dont care about gets

        else:
            #sequential
            pass





        # checks if I am the originator
#        if(self.requests[cmds.rID].queue[0][1].ip == self.ip):
            # and we haven't received any acks
 #           if(len(self.requests[cmds.rID])) == 1):
                #broadcast




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

            self.node_log.write('Outstanding requests:' + '\n') 
            for req in self.requests:
                if(isinstance(self.requests[req], PriorityQueue)):
                    self.node_log.write('\n' + str(req) + ': ' + str(self.requests[req].queue)) 
                else:
                    self.node_log.write('\n' + str(req) + ': ' + str(self.requests[req])) 
            self.node_log.write('processed requests:' + '\n') 
            for req in self.processed_reqs:
                if(isinstance(self.processed_reqs[req], PriorityQueue)):
                    self.node_log.write('\n' + str(req) + ': ' + str(self.processed_reqs[req].queue))
                else: 
                    self.node_log.write('\n' + str(req) + ': ' + str(self.processed_reqs[req].queue)) 

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
