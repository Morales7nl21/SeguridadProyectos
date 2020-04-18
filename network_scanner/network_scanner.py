#!/usr/bin/env python
import scapy.all as scapy

def scan (ip):
    #Devuelve la mac usando el protocolo ARP se envia un mensaje de tipo broadcast con la ip
    #Para acceder y esta conesta devolviendo la mac.
    scapy.arping(ip)

#La funcion scapy.arping puede bsucar dentro de un rango
scan("10.0.2.2/24")
