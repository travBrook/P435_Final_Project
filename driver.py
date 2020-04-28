import config
import sys, subprocess, time



def run():

    #Spawn controller and replicas
    proc_id = subprocess.Popen([sys.executable, './master.py', config.MASTER_IP, 'Master Control'])

    time.sleep(2)
    print("\nMoving to clientel\n")

    #Spawn Client
    proc_id = subprocess.Popen([sys.executable, './client.py', config.CLIENT1_IP, config.MASTER_IP,'Client1', '4, 1, key2 ::: value2', '4, 2, key1'])
    proc_id = subprocess.Popen([sys.executable, './client.py', config.CLIENT2_IP, config.MASTER_IP,'Client2',  '4, 1, key1 ::: value?!', '4, 2, key1', '0, 1, key1 ::: overwrite1', '0, 1, key3 ::: value1'])


    # keep running to listen for kill command
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('keyboard interrupt, exiting...')



#main
run()