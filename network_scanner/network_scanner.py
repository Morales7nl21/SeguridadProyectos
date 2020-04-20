#!/usr/bin/env python
# Provee la funcion que manda el broadcast pa tener la mac
import scapy.all as scapy


def scan (ip):

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
    # (packet sent, answer) y el segundo de la lista son los paquetes sin responder.

    answered, unanswered = scapy.srp(arp_request_broadcast,timeout = 1)

    # Imprimimos lo que nos dio de la variable combinada el metodo summary.
    print(answered.summary())
    # arp_request_broadcast.show()



    # !! El metodo ls lista los metodos que oueden ser modificados, como ip destino para hacer el broadcast, mac, etc.
    # scapy.ls(scapy.ARP())
    # scapy.ls(scapy.Ether())

#La funcion scapy.arping puede bsucar dentro de un rango
scan("10.0.2.2/24")
