import config
import sys, subprocess, time



def run():

    #Spawn controller and replicas
    proc_id = subprocess.Popen([sys.executable, './master.py', config.MASTER_IP, 'Master Control'])

    time.sleep(2)
    print("\nMoving to clientel\n")

    #Spawn Client
    proc_id = subprocess.Popen([sys.executable, './client.py', config.CLIENT_IP, config.MASTER_IP,'Client1'])

    # keep running to listen for kill command
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('keyboard interrupt, exiting...')



#main
run()