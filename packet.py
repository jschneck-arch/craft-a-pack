import struct
import random


class TCPPacket:
    FLAG_OPTIONS = {
        1: 'FIN',
        2: 'SYN',
        3: 'RST',
        4: 'PSH',
        5: 'ACK',
        6: 'URG',
        7: 'ECE',
        8: 'CWR'
    }

    def __init__(self, session_id=None, destination_ips=None, source_ip=None, source_mac=None, source_port=0,
                 destination_port=0, flags=['SYN'], data=None):
        self.session_id = session_id
        self.destination_ips = destination_ips or []
        self.source_ip = source_ip or self.generate_random_ip()
        self.source_mac = source_mac or self.generate_random_mac()
        self.source_port = source_port or random.randint(1024, 65535)
        self.destination_port = destination_port or random.randint(0, 65535)
        self.flags = flags
        self.data = data
        self.ttl = random.randint(1, 128)
        self.window_size = 8192
        self.checksum = 0
        self.tcp_options = []

    def __str__(self):
        return f"TCP Packet:\nSession ID: {self.session_id}\nSource IP: {self.source_ip}\nDestination IPs: {', '.join(self.destination_ips)}\n" \
               f"Source MAC: {self.source_mac}\n" \
               f"Source Port: {self.source_port}\nDestination Port: {self.destination_port}\n" \
               f"Flags: {self.flags}\nData: {self.data}\nTTL: {self.ttl}\nWindow Size: {self.window_size}\nChecksum: {self.checksum}\nTCP Options: {self.tcp_options}"

    @staticmethod
    def generate_random_ip():
        ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        return ip

    @staticmethod
    def generate_random_mac():
        mac = ":".join("%02x" % random.randint(0, 255) for _ in range(6))
        return mac

    def print_packet(self):
        print(self)

    def print_flag_options(self):
        for index, flag in self.FLAG_OPTIONS.items():
            print(f"{index} - {flag}")

    def set_source_ip(self, source_ip):
        self.source_ip = source_ip

    def set_source_mac(self, source_mac):
        self.source_mac = source_mac

    def set_source_port(self, source_port):
        self.source_port = source_port

    def set_destination_port(self, destination_port):
        self.destination_port = destination_port

    def set_flags(self, flags):
        self.flags = flags

    def set_data(self, data):
        self.data = data

    def set_ttl(self, ttl):
        self.ttl = ttl

    def set_window_size(self, window_size):
        self.window_size = window_size

    def set_checksum(self, checksum):
        self.checksum = checksum

    def set_tcp_options(self, tcp_options):
        self.tcp_options = tcp_options

    def send_packet(self, sock):
        # Create the TCP header
        tcp_header = struct.pack('!HHLLBBHHH',
                                 self.source_port,
                                 self.destination_port,
                                 random.getrandbits(32),  # Sequence number (random)
                                 0,  # Acknowledgment number (default)
                                 self.build_flags(),
                                 self.window_size,
                                 self.checksum,
                                 0)  # Urgent pointer (default)

        # Add TCP options if available
        if self.tcp_options:
            tcp_header += self.build_tcp_options()

        # Create the complete packet
        packet = tcp_header + self.data.encode()

        # Send the packet
        sock.send(packet)

    def build_flags(self):
        flags = 0
        for flag in self.flags:
            if flag in self.FLAG_OPTIONS.values():
                flags |= 1 << (list(self.FLAG_OPTIONS.values()).index(flag))
        return flags

    def build_tcp_options(self):
        options = b''
        for tcp_option in self.tcp_options:
            if tcp_option == 'MSS':
                # Maximum Segment Size (MSS)
                mss_option = struct.pack('!BBH', 2, 4, 1460)
                options += mss_option
            elif tcp_option == 'NOP':
                # No-Operation (NOP)
                nop_option = struct.pack('!B', 1)
                options += nop_option
            elif tcp_option == 'WS':
                # Window Scale (WS)
                ws_option = struct.pack('!BBB', 3, 3, 7)
                options += ws_option
            # Add more TCP options as needed
        return options
