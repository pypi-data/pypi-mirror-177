'''Module providing time functions.'''
import time
import sys
import signal
import json
from .const import MAC_INFO_MAP
from datetime import datetime
from pylibpcap.base import Sniff


class Payload():
    '''Stores parsed payload data. Such as mac and ip addresses of involved devices.'''

    def __init__(self, payload_bytes, mac_notation=False):
        payload_array = bytearray(payload_bytes)

        self.payload_bytes = payload_bytes

        if mac_notation:
            self.src_mac = (f'{payload_array[0]  :02x}:'
                            f'{payload_array[1]  :02x}:'
                            f'{payload_array[2]  :02x}:'
                            f'{payload_array[3]  :02x}:'
                            f'{payload_array[4]  :02x}:'
                            f'{payload_array[5]  :02x}')
            self.dst_mac = (f'{payload_array[6]  :02x}:'
                            f'{payload_array[7]  :02x}:'
                            f'{payload_array[8]  :02x}:'
                            f'{payload_array[9]  :02x}:'
                            f'{payload_array[10] :02x}:'
                            f'{payload_array[11] :02x}')
        else:
            self.src_mac = (f'{payload_array[0]  :02x}'
                            f'{payload_array[1]  :02x}'
                            f'{payload_array[2]  :02x}'
                            f'{payload_array[3]  :02x}'
                            f'{payload_array[4]  :02x}'
                            f'{payload_array[5]  :02x}')
            self.dst_mac = (f'{payload_array[6]  :02x}'
                            f'{payload_array[7]  :02x}'
                            f'{payload_array[8]  :02x}'
                            f'{payload_array[9]  :02x}'
                            f'{payload_array[10] :02x}'
                            f'{payload_array[11] :02x}')

        self.src_ip =  (f'{payload_array[26]}.'
                        f'{payload_array[27]}.'
                        f'{payload_array[28]}.'
                        f'{payload_array[29]}')
        self.dst_ip =  (f'{payload_array[30]}.'
                        f'{payload_array[31]}.'
                        f'{payload_array[32]}.'
                        f'{payload_array[33]}')


class IoTSniffer():
    '''Sniff a specific interface and port, and store devices data,
    such as number of packets transmited and total packets size.'''

    def __init__(self, interface, port, packets_limit=None, time_limit=None, output_file=None):

        self.sniffobj = Sniff(
            interface,
            filters="port "+str(port),
            count=-1,
            promisc=1,
            out_file="pcap.pcap")

        self.packets_count  = 0
        self.init_timestamp = 0
        self.packets_limit  = None
        self.time_limit     = None
        self.collected_data = {}
        self.metadata = {
            'interface': interface,
            'port': port
        }

        if packets_limit:
            if packets_limit>0:
                self.packets_limit = packets_limit
            else:
                raise ValueError("packets_limit must be greater than zero.")

        if time_limit:
            if time_limit>0:
                self.time_limit = time_limit
            else:
                raise ValueError("time_limit must be grater than zero.")
        
        if output_file is None:
            self.output_file = interface+'_'+str(port)+'.json'
        else:
            self.output_file = output_file

        signal.signal(signal.SIGINT, self.exit)


    def sniff(self):
        '''Starts the sniffing process.'''

        self.init_timestamp = int(time.time())
        self.metadata['start_time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        for packet_length, _, packet_payload in self.sniffobj.capture():

            self.packets_count += 1

            print('Packets sniffed:', self.packets_count)

            parsed_payload = Payload(packet_payload)
            src_mac = parsed_payload.src_mac

            if src_mac not in self.collected_data:
                self.collected_data[src_mac] = dict({'packets_sent': 1,
                                                     'total_size': packet_length})
                if src_mac in MAC_INFO_MAP:
                    self.collected_data[src_mac]['name'] = MAC_INFO_MAP[src_mac]['name']
            else:
                self.collected_data[src_mac]['packets_sent'] += 1
                self.collected_data[src_mac]['total_size'] += packet_length

            if self.packets_limit and self.packets_count == self.packets_limit:
                print("Sniff terminated reaching packets limit.")
                print("Packets captured:", self.packets_count)
                break

            elapsed_time = (int(time.time())-self.init_timestamp)

            if self.time_limit and elapsed_time > self.time_limit:
                print("Sniff terminated reaching time limit.")
                print("Elapsed time:", elapsed_time)
                break

        self.finish()


    def finish(self):
        '''Executed when the program is finished.'''

        self.metadata['end_time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        stats = self.sniffobj.stats()

        print(stats.capture_cnt, " packets captured")
        print(stats.ps_recv, " packets received by filter")
        print(stats.ps_drop, "  packets dropped by kernel")
        print(stats.ps_ifdrop, "  packets dropped by iface")

        print("Collected Data:")
        print(self.collected_data)

        sniff_results = {
            'metadata': self.metadata,
            'data': self.collected_data
        }

        with open(self.output_file, 'w') as output_file:
            json.dump(sniff_results, output_file, indent=4)


    def exit(self, _, __):
        '''Executed when the program is terminated by SIGINT signal.'''

        print("")
        print("Sniff terminated by SIGINT.")
        self.finish()
        sys.exit(0)
