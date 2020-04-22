import config
import sys, subprocess, time

#Spawn controller and replicas

#master = master.Master(config.MASTER_IP)
#master.run()
def run():
    proc_id = subprocess.Popen([sys.executable, './master.py', config.MASTER_IP, 'Master Control'])
    time.sleep(2)
    print("\nMoving to clientel\n")


    #Spawn Client

    #client = client.Client(config.CLIENT_IP)
    #client.run()

    proc_id = subprocess.Popen([sys.executable, './client.py', config.CLIENT_IP, 'Client1'])



#main
run()