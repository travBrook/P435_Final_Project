

import msg_pb2

def build(ip, consis, request, ack, data, l_Clock, rID = 0):
    message = msg_pb2.Message()
    message.ip = ip
    message.consis = consis
    message.request = request
    message.ack = ack
    message.data = data
    message.l_Clock = l_Clock
    message.rID = rID
    return message

"""
msg = build('fds', 1,1,1,'testee')
print(msg)
serial = msg.SerializeToString()
print(serial)
test = msg_pb2.Message()
test.ParseFromString(serial)
print(test)
"""