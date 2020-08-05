from multiprocessing import Process
import zmq, time

class Base(Process):
    def __init__(self, address):
        super().__init__()
        self.address = address

class Updater(Base):
    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.bind(self.address)
        msg = socket.recv_json()
        print(msg)
        return msg
       
