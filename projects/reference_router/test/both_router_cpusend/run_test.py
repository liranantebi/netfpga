#!/bin/env python

from NFTestLib import *
from NFTestHeader import reg_defines, scapy

from RegressRouterLib import *

interfaces = ("nf2c0", "nf2c1", "nf2c2", "nf2c3", "eth1", "eth2")

nftest_init(interfaces, 'conn')
nftest_start()

nftest_barrier()

if isHW():
    NUM_PKTS = 20
else:
    NUM_PKTS = 10

routerMAC0 = "00:ca:fe:00:00:01"
routerMAC1 = "00:ca:fe:00:00:02"
routerMAC2 = "00:ca:fe:00:00:03"
routerMAC3 = "00:ca:fe:00:00:04"

routerIP0 = "192.168.0.40"
routerIP1 = "192.168.1.40"
routerIP2 = "192.168.2.40"
routerIP3 = "192.168.3.40"

ALLSPFRouters = "224.0.0.5"

# Write the mac and IP addresses
nftest_add_dst_ip_filter_entry ('nf2c0', 0, routerIP0)
nftest_add_dst_ip_filter_entry ('nf2c1', 1, routerIP1)
nftest_add_dst_ip_filter_entry ('nf2c2', 2, routerIP2)
nftest_add_dst_ip_filter_entry ('nf2c3', 3, routerIP3)
nftest_add_dst_ip_filter_entry ('nf2c0', 4, ALLSPFRouters)

nftest_set_router_MAC ('nf2c0', routerMAC0)
nftest_set_router_MAC ('nf2c1', routerMAC1)
nftest_set_router_MAC ('nf2c2', routerMAC2)
nftest_set_router_MAC ('nf2c3', routerMAC3)

if isHW():
    nftest_regread_expect(reg_defines.MDIO_PHY_0_CONTROL_REG(), 0x1140)
    nftest_regread_expect(reg_defines.MDIO_PHY_1_CONTROL_REG(), 0x1140)
    nftest_regread_expect(reg_defines.MDIO_PHY_2_CONTROL_REG(), 0x5140)
    nftest_regread_expect(reg_defines.MDIO_PHY_3_CONTROL_REG(), 0x5140)

DA = routerMAC0
SA = "aa:bb:cc:dd:ee:ff"
TTL = 64
DST_IP = "192.168.1.1"
SRC_IP = "192.168.0.1"
nextHopMAC = "dd:55:dd:66:dd:77"

precreated0 = scapy.rdpcap('precreated0.pcap')
precreated1 = scapy.rdpcap('precreated1.pcap')
precreated2 = scapy.rdpcap('precreated2.pcap')
precreated3 = scapy.rdpcap('precreated3.pcap')

# reset counters
nftest_regwrite(reg_defines.MAC_GRP_0_RX_QUEUE_NUM_PKTS_STORED_REG(), 0)
nftest_regwrite(reg_defines.MAC_GRP_0_TX_QUEUE_NUM_PKTS_SENT_REG(), 0)
nftest_regwrite(reg_defines.MAC_GRP_0_RX_QUEUE_NUM_BYTES_PUSHED_REG(), 0)
nftest_regwrite(reg_defines.MAC_GRP_0_TX_QUEUE_NUM_BYTES_PUSHED_REG(), 0)

nftest_regwrite(reg_defines.MAC_GRP_1_RX_QUEUE_NUM_PKTS_STORED_REG(), 0)
nftest_regwrite(reg_defines.MAC_GRP_1_TX_QUEUE_NUM_PKTS_SENT_REG(), 0)
nftest_regwrite(reg_defines.MAC_GRP_1_RX_QUEUE_NUM_BYTES_PUSHED_REG(), 0)
nftest_regwrite(reg_defines.MAC_GRP_1_TX_QUEUE_NUM_BYTES_PUSHED_REG(), 0)

nftest_regwrite(reg_defines.MAC_GRP_2_RX_QUEUE_NUM_PKTS_STORED_REG(), 0)
nftest_regwrite(reg_defines.MAC_GRP_2_TX_QUEUE_NUM_PKTS_SENT_REG(), 0)
nftest_regwrite(reg_defines.MAC_GRP_2_RX_QUEUE_NUM_BYTES_PUSHED_REG(), 0)
nftest_regwrite(reg_defines.MAC_GRP_2_TX_QUEUE_NUM_BYTES_PUSHED_REG(), 0)

nftest_regwrite(reg_defines.MAC_GRP_3_RX_QUEUE_NUM_PKTS_STORED_REG(), 0)
nftest_regwrite(reg_defines.MAC_GRP_3_TX_QUEUE_NUM_PKTS_SENT_REG(), 0)
nftest_regwrite(reg_defines.MAC_GRP_3_RX_QUEUE_NUM_BYTES_PUSHED_REG(), 0)
nftest_regwrite(reg_defines.MAC_GRP_3_TX_QUEUE_NUM_BYTES_PUSHED_REG(), 0)

print "Sending now:"
pkt = None
totalPktLengths = [0,0,0,0]
for i in range(NUM_PKTS):
    pkt = precreated0[i]
    totalPktLengths[0] += len(pkt)
    nftest_send('nf2c0', pkt)
    nftest_expect('eth1', pkt)

    pkt = precreated1[i]
    totalPktLengths[1] += len(pkt)
    nftest_send('nf2c1', pkt)
    nftest_expect('eth2', pkt)

    pkt = precreated2[i]
    totalPktLengths[2] += len(pkt)
    nftest_send('nf2c2', pkt)
    nftest_expect('nf2c2', pkt)

    pkt = precreated3[i]
    totalPktLengths[3] += len(pkt)
    nftest_send('nf2c3', pkt)
    nftest_expect('nf2c3', pkt)

nftest_barrier()

nftest_regread_expect(reg_defines.MAC_GRP_0_TX_QUEUE_NUM_PKTS_SENT_REG(), NUM_PKTS)
nftest_regread_expect(reg_defines.MAC_GRP_0_TX_QUEUE_NUM_BYTES_PUSHED_REG(), totalPktLengths[0])

nftest_regread_expect(reg_defines.MAC_GRP_1_TX_QUEUE_NUM_PKTS_SENT_REG(), NUM_PKTS)
nftest_regread_expect(reg_defines.MAC_GRP_1_TX_QUEUE_NUM_BYTES_PUSHED_REG(), totalPktLengths[1])

nftest_regread_expect(reg_defines.MAC_GRP_2_TX_QUEUE_NUM_PKTS_SENT_REG(), NUM_PKTS)
nftest_regread_expect(reg_defines.MAC_GRP_2_TX_QUEUE_NUM_BYTES_PUSHED_REG(), totalPktLengths[2])
if isHW():
    nftest_regread_expect(reg_defines.MAC_GRP_2_RX_QUEUE_NUM_BYTES_PUSHED_REG(), totalPktLengths[2])
    nftest_regread_expect(reg_defines.MAC_GRP_2_RX_QUEUE_NUM_PKTS_STORED_REG(), NUM_PKTS)

nftest_regread_expect(reg_defines.MAC_GRP_3_TX_QUEUE_NUM_PKTS_SENT_REG(), NUM_PKTS)
nftest_regread_expect(reg_defines.MAC_GRP_3_TX_QUEUE_NUM_BYTES_PUSHED_REG(), totalPktLengths[3])
if isHW():
    nftest_regread_expect(reg_defines.MAC_GRP_3_RX_QUEUE_NUM_BYTES_PUSHED_REG(), totalPktLengths[3])
    nftest_regread_expect(reg_defines.MAC_GRP_3_RX_QUEUE_NUM_PKTS_STORED_REG(), NUM_PKTS)

nftest_regread_expect(reg_defines.ROUTER_OP_LUT_NUM_CPU_PKTS_SENT_REG(), 4*NUM_PKTS)

nftest_barrier()

total_errors = nftest_finish()

if total_errors == 0:
    print 'SUCCESS!'
    sys.exit(0)
else:
    print 'FAIL: ' + str(total_errors) + ' errors'
    sys.exit(1)
