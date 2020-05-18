#!/etc/bin/env python
import scapy.all as scapy


def sniff(interface):
    # iface interface a snifear, store es donde guardar los packetes en memoria
    # prn especifica una callback function es decir ejecutar una funcion cada que e mande el paquete
    scapy.sniff(iface=interface, store=False, prn=procces_sniffed_packet)

def procces_sniffed_packet(packet):
    print(packet)

sniff("eth0")