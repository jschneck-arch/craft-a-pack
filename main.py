import argparse
import time
import socket
import pickle
from packet import TCPPacket


CACHE_FILE = 'packet_cache.pkl'


def load_packet_sessions():
    try:
        with open(CACHE_FILE, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}


def save_packet_sessions(packet_sessions):
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(packet_sessions, f)


packet_sessions = load_packet_sessions()  # Dictionary to store packet sessions


def create_session(session_id, target_ips):
    packet = TCPPacket(session_id=session_id, destination_ips=target_ips)
    packet.print_packet()
    packet_sessions[session_id] = packet  # Add packet session to dictionary
    save_packet_sessions(packet_sessions)
    return packet


def modify_packet(packet):
    print("\nWhat would you like to modify?")
    print("1 - Source IP")
    print("2 - Source MAC")
    print("3 - Source Port")
    print("4 - Destination Port")
    print("5 - Flags")
    print("6 - Data")
    print("7 - TTL")
    print("8 - Window Size")
    print("9 - Checksum")
    print("10 - TCP Options")
    print("11 - Exit")

    while True:
        choice = input("Enter your choice: ")

        if choice == "1":
            source_ip = input("Enter the new source IP: ")
            packet.set_source_ip(source_ip)
            packet.print_packet()

        elif choice == "2":
            source_mac = input("Enter the new source MAC: ")
            packet.set_source_mac(source_mac)
            packet.print_packet()

        elif choice == "3":
            source_port = int(input("Enter the new source port: "))
            packet.set_source_port(source_port)
            packet.print_packet()

        elif choice == "4":
            destination_port = int(input("Enter the new destination port: "))
            packet.set_destination_port(destination_port)
            packet.print_packet()

        elif choice == "5":
            print("Available flags:")
            packet.print_flag_options()
            new_flags = input("Enter the new flags (separated by space): ").split()
            packet.set_flags(new_flags)
            packet.print_packet()

        elif choice == "6":
            new_data = input("Enter the new data: ")
            packet.set_data(new_data)
            packet.print_packet()

        elif choice == "7":
            ttl = int(input("Enter the new TTL value: "))
            packet.set_ttl(ttl)
            packet.print_packet()

        elif choice == "8":
            window_size = int(input("Enter the new window size: "))
            packet.set_window_size(window_size)
            packet.print_packet()

        elif choice == "9":
            checksum = int(input("Enter the new checksum: "))
            packet.set_checksum(checksum)
            packet.print_packet()

        elif choice == "10":
            tcp_options = input("Enter the new TCP options (separated by space): ").split()
            packet.set_tcp_options(tcp_options)
            packet.print_packet()

        elif choice == "11":
            break

        else:
            print("Invalid choice. Please try again.")


def send_packets(packet, num_packets, delay):
    print(f"\nSending {num_packets} packets:")
    for i in range(num_packets):
        packet.print_packet()
        time.sleep(delay)

    print("\nPackets sent successfully!")


def create_connection(packet):
    print("\nCreating a connection...")
    # Get the first destination IP
    target_ip = packet.destination_ips[0]
    # Create a socket and connect to the target IP and port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, packet.destination_port))

    # Send the packet
    packet.send_packet(sock)

    # Receive the response
    response = sock.recv(1024)
    print(f"\nReceived response from {target_ip}:\n{response.decode()}")

    # Close the socket
    sock.close()

    print("\nConnection established!")


def test_packets(packet, num_packets, delay):
    print(f"\nTesting {num_packets} packets:")
    for i in range(num_packets):
        packet.print_packet()
        # Implement your tests here
        time.sleep(delay)

    print("\nTesting completed!")


def main():
    parser = argparse.ArgumentParser(description='TCP Packet Configuration Script')
    subparsers = parser.add_subparsers(dest='command', help='Command')

    # Create sub-command
    create_parser = subparsers.add_parser('create', help='Create a packet session')
    create_parser.add_argument('session_id', type=int, help='Session ID')
    create_parser.add_argument('target_ips', nargs='+', help='Target IPs')

    # Modify sub-command
    modify_parser = subparsers.add_parser('modify', help='Modify a packet session')
    modify_parser.add_argument('session_id', type=int, help='Session ID')

    # Send sub-command
    send_parser = subparsers.add_parser('send', help='Send packets')
    send_parser.add_argument('session_id', type=int, help='Session ID')
    send_parser.add_argument('--num-packets', type=int, default=1, help='Number of packets to send')
    send_parser.add_argument('--delay', type=float, default=1.0, help='Delay between packets (in seconds)')

    # Connect sub-command
    connect_parser = subparsers.add_parser('connect', help='Create a connection')
    connect_parser.add_argument('session_id', type=int, help='Session ID')

    # Test sub-command
    test_parser = subparsers.add_parser('test', help='Test packets')
    test_parser.add_argument('session_id', type=int, help='Session ID')
    test_parser.add_argument('--num-packets', type=int, default=1, help='Number of packets to test')
    test_parser.add_argument('--delay', type=float, default=1.0, help='Delay between packets (in seconds)')

    args = parser.parse_args()

    if args.command == 'create':
        packet = create_session(args.session_id, args.target_ips)

    elif args.command == 'modify':
        if args.session_id in packet_sessions:
            packet = packet_sessions[args.session_id]
            modify_packet(packet)
        else:
            print(f"Session {args.session_id} does not exist.")

    elif args.command == 'send':
        if args.session_id in packet_sessions:
            packet = packet_sessions[args.session_id]
            send_packets(packet, args.num_packets, args.delay)
        else:
            print(f"Session {args.session_id} does not exist.")

    elif args.command == 'connect':
        if args.session_id in packet_sessions:
            packet = packet_sessions[args.session_id]
            create_connection(packet)
        else:
            print(f"Session {args.session_id} does not exist.")

    elif args.command == 'test':
        if args.session_id in packet_sessions:
            packet = packet_sessions[args.session_id]
            test_packets(packet, args.num_packets, args.delay)
        else:
            print(f"Session {args.session_id} does not exist.")

    save_packet_sessions(packet_sessions)


if __name__ == '__main__':
    main()
