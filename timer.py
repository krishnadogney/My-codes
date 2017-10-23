from threading import Timer as timer
from PyQt5.QtCore import QObject,pyqtSignal as pyqtsignal
node_thread_id=[1,2,3];
slots=[1,5,7];
class signal_slots(QObject):
    def __init__(self,trigger,count):
        self.trigger=pyqtsignal(name='trigger')
        self.count=count
    def connect_slot(self,count):
        for item,ind in enumerate(slots):
            if item==count:
                self.trigger.connect(self.handle_trigger,[node_thread_id[ind]])
                self.trigger.emit()
    def handle_trigger(self,kwargs):
        print('the trigger has been handled.',kwargs)


class channel_manager():
    def __init__(self,slot_len=10*10^-3,number_slots=1):
        self.slot_len=slot_len;
        self.number_slots=number_slots;

    def sync(self,slot_len=10*10^-3,number_slots=1):
        count=0;
        while count<=number_slots:
            obj=signal_slots();
            t=timer(slot_len,obj.connect_slot,[count])
            t.start()


if __name__=='__main__':
    cm=channel_manager()


