# Features of the testing framework

Note: In folder framework_tests you can find a reference usage of all provided features.

## Asserts
All asserts defined in unittest.TestCase can be used.

Also the following asserts are available. Message is always the message for the assert.

* assertAllReachable(message): Check if each host can reach each other using ping
* assertReachable(h1, h2, message): Check if h1 and h2 can reach each other
* assertPacketIn(message, host=None): Check if there was a packet on a host. Caution: This is only available when running 
analyze_packets(host, test_function) before!
* assertReceivedPacket(packet, message, host=None): Check if there was a packet on host matching the given packet (See section matching Packet).
Caution: This is only available when running analyze_packets(host, test_function) before!
* assertNotReceivedPacket(packet, message, host=None): Check if there was NOT a packet on host matching the given packet (See section matching Packet).
Caution: This is only available when running analyze_packets(host, test_function) before!

## Helper functions

* self.execCmd(host, cmd): Execute the cmd on given host. Will return the output of the command
* self.analyze_packets(host, test_function): Capture the packets on given host, when running the given test_function.
* self.get_all_packets(packet, host=None): Returns all captured packets for a specific host.
Caution: This is only available when running analyze_packets(host, test_function) before!
This method can be used e.g. to check timing of packets, because each packet has a "time_stamp" attribute.
* self.send_ip4_packet(host, dst, ip_proto, content): This method sends an ipv4 packet from host to IP destination dst.
ip_proto should contain the protocol type for ip header (e.g. dpkt.ip.IP_PROTO_ICMP) and content
is the content of the created packet.

### Capturing packets

You can write pcap files capturing all traffic on an host. First you need to import testing.tcpdump.Packetcapture
Then you can instantiate a capture object using: capture = PacketCapture(self.net)
To start capturing use: capture.start_capture("h1"), where h1 is the name of your host (defined in your mininet-network).
After that you can do what ever you want (sending packets around). To stop capturing use capture.stop_capture().
You can get the path to the file by using capture.get_file_name()

### Analyzing packets

There is also an easier way to analyze packets arrived on an given host. Just specify the host and give a test_function
for which the packets should be analyzed. After that you can use the provided asserts.

self.analyze_packets("h1", lambda: self.net.pingAll())
self.assertPacketIn("Host 1 received a packet")

or

self.analyze_packets("h1", lambda: self.net.pingAll())
packet = Packet()
packet.eth_src = "cc:cc:cc:cc:cc:01"
packet.eth_dst = "cc:cc:cc:cc:cc:02"
self.assertReceivedPacket(packet, "Received eth packet")

Additionally you can analyze packets on more than one host. Use therefore a lists of hosts to analyze:
self.analyze_packets(["h1","h2"], lambda: self.net.pingAll())
every assert has an additional host parameter to specify on which host this assert should be checked:
self.assertReceivedPacket(packet, "Received eth packet", "h1")

### Matching packets

To check if a host received (or not received) a packet, you need to define a packet, that is used for matching. Every
defined attribute of this packet is used for matching. See testcases/test_packets.py as an example.
Possible attributes can be found in testing/tcpdump/packet.py Every not set attribute is ignored.

## Sending own test packets
You also can send packets in your test. See test_send_packets.py to get an idea how this could work. You can send
every packet that you can create, using dpkt.

## Using IPerf
The test-framework supports running IPerf in the test environment. First you need to import IPerf support:
from testing.iperf.IPerfTest import IPerfTest
Then you can setup a IPerfTest by using
iperf_test = IPerfTest(self.net)
iperf_test.start_test("h1", ["h2", "h3"], server_parameter = "", client_parameter = [])
where in this case h1 is the server and h2 and h3 the clients. You can specify a list of multiple clients.
Additionally you can specify parameters that are handed over to the IPerf call. After running the test you can use
get_transfer(index) and get_bandwidth(index) to get the results. With the index you need to identify the client,
for which you want to get the results. This order is corresponding to the list, provided in the start_test call.

See testcases/test_iperf.py as an example.