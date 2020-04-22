

import msg_pb2

def build(ip, consis, request, ack, data, num_chunks = 1):
    message = msg_pb2.Message()
    message.ip = ip
    message.consis = consis
    message.request = request
    message.ack = ack
    message.data = data
    message.num_chunks = num_chunks
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