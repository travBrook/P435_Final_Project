# settings to be used with final project: KV Store


#default paths
log_path = './log/'

# Network CONSTANTS:
CLIENT1_IP = '127.0.0.1' # + sid will be the assigned ip
CLIENT2_IP = '127.0.0.2'
MASTER_IP = '127.0.0.11'
REPLICA1_IP = '127.0.0.21'
REPLICA2_IP = '127.0.0.22'
REPLICA3_IP = '127.0.0.23'
PORT = 65432 





#data transmission **may not be useful for final project
word_max = 45   #max words sent per message
item_max = int(word_max/3) # max mapped items