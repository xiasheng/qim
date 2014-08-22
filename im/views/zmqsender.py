
import zmq

class ZMQSender():
    instance = None
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5557")
    

    @staticmethod
    def SendMsg(msg):
        ZMQSender.socket.send_string(msg)
        res = ZMQSender.socket.recv()
        return res

def AddUser2Group(user, group):
    msg = 'ejabberdctl srg_user_add %s d-connected.com %s d-connected.com' %(user, group)
    ZMQSender.SendMsg(msg)   

if __name__ == '__main__':
    AddUser2Group('13022222222', 'test')
