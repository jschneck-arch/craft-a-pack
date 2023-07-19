# craft-a-pack
packet crafing

TCP Packet Configuration Tool - README

This program allows you to create, modify, send, connect, and test TCP packets with customizable parameters.

Requirements:
- Python 3.x
- Dependencies:
  - click (install with `pip install click`)
  - argparse (already included in Python standard library)

Usage:
1. Run the program with the following command: `python main.py [command] [options]`

Commands:
- create: Create a new packet session
- modify: Modify an existing packet session
- send: Send packets
- connect: Create a TCP connection
- test: Test packets

Options:
- create:
  - session_id: Unique ID for the packet session
  - target_ips: Space-separated list of target IP addresses

- modify:
  - session_id: ID of the packet session to modify

- send:
  - session_id: ID of the packet session to send
  - num_packets: Number of packets to send (default: 1)
  - delay: Delay between packets in seconds (default: 1.0)

- connect:
  - session_id: ID of the packet session to connect

- test:
  - session_id: ID of the packet session to test
  - num_packets: Number of packets to test (default: 1)
  - delay: Delay between packets in seconds (default: 1.0)

Examples:
1. Creating a packet session:
   `python main.py create 1 192.168.0.1 192.168.0.2`

2. Modifying a packet session:
   `python main.py modify 1`

3. Sending packets:
   `python main.py send 1 --num-packets 10 --delay 0.5`

4. Creating a connection:
   `python main.py connect 1`

5. Testing packets:
   `python main.py test 1 --num-packets 5 --delay 1.0`

Note:
- The program will cache the created and modified packet sessions, allowing you to reuse them in subsequent program executions.
- The packet sessions are stored in the `packet_cache.pkl` file.

Feel free to explore the program and customize the packet parameters as needed.

For additional help or inquiries, please contact.

Enjoy using the TCP Packet Configuration Tool!
