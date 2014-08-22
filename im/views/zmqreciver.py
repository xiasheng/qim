
import zmq, os

def RunEjabberdCmd(cmd):
    try:
        os.system(cmd)
    except:
        pass

    
if __name__ == '__main__':
    context = zmq.Context()

    # Socket to receive messages on
    receiver = context.socket(zmq.REP)
    receiver.bind("tcp://*:5557")

    # Process tasks forever
    try:
        while True:
            cmd = receiver.recv()
            print cmd
            RunEjabberdCmd(cmd)
            receiver.send("success")    
    except KeyboardInterrupt:
        exit(0)   

