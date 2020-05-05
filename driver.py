import config
import sys, subprocess, time



def run():

    #Spawn controller and replicas
    proc_id = subprocess.Popen([sys.executable, './master.py', config.MASTER_IP, 'Master Control'])

    time.sleep(2)           
    print("\nMoving to clientel\n")

    #Spawn Client
    #proc_id = subprocess.Popen([sys.executable, './causalClient.py', config.CLIENT1_IP, config.MASTER_IP,'CausalClient1', 'causal1'])
    #proc_id = subprocess.Popen([sys.executable, './causalClient.py', config.CLIENT6_IP, config.MASTER_IP,'CausalClient2',  'causal2'])
    #time.sleep(0.13)
    #proc_id = subprocess.Popen([sys.executable, './client.py', config.CLIENT2_IP, config.MASTER_IP,'LinearClient1',  'linear1'])
    #proc_id = subprocess.Popen([sys.executable, './client.py', config.CLIENT4_IP, config.MASTER_IP,'LinearClient2',  'linear2'])
    #proc_id = subprocess.Popen([sys.executable, './client.py', config.CLIENT8_IP, config.MASTER_IP,'SeqClient1',  'seq1'])    
   # proc_id = subprocess.Popen([sys.executable, './client.py', config.CLIENT3_IP, config.MASTER_IP,'SeqClient2',  'seq2'])

    proc_id = subprocess.Popen([sys.executable, './client.py', config.CLIENT5_IP, config.MASTER_IP,'EventualClient1',  'event1'])
    proc_id = subprocess.Popen([sys.executable, './client.py', config.CLIENT7_IP, config.MASTER_IP,'EventualClient2',  'event2'])

    
   # time.sleep(0.13)
    '''
    proc_id = subprocess.Popen([sys.executable, './client.py', config.CLIENT3_IP, config.MASTER_IP,'Client3',  '4, 1, key1 ::: value?!', '1, 2, key1', '1, 1, key1 ::: overwrite1', '1, 1, key3 ::: value1'])
    time.sleep(0.13)
    proc_id = subprocess.Popen([sys.executable, './client.py', config.CLIENT4_IP, config.MASTER_IP,'Client4',  '4, 1, key1 ::: value?!', '1, 2, key1', '1, 1, key1 ::: overwrite1', '1, 1, key3 ::: value1'])
'''
    # keep running to listen for kill command
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('keyboard interrupt, exiting...')



#main
run()