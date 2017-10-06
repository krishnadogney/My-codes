class packet_generator:


    def __init__(self,no_of_packet, time=None, size=None, id = None , src_ip=None, dst_ip=None,
                 flow_id=0,port = None,src_port=None,dst_port=None,next_hop =None):
        self.time = time
        self.size = size
        self.id = id
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.flow_id = flow_id
        self.src_port = src_port
        self.dst_port = dst_port
        self.no_of_packet = no_of_packet
        self.next_hop = next_hop

    def packet_format(self):
      for i in range(self.no_of_packet):
        packet = {'src_ip' : self.src_ip, 'dst_ip' : self.dst_ip ,'src_port' : self.src_port,
                        'dst_port' : self.dst_port, 'packet_size': self.size, 'next_hop': self.next_hop}
        print('krishna')
        print(packet)
        return packet





pac1 = packet_generator(10)
pac1.packet_format()