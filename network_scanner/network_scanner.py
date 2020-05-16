#!/usr/bin/env python
# Provee la funcion que manda el broadcast pa tener la mac
import scapy.all as scapy
import optparse

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target to send arp message")
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("[-] Please especify target, use --help for more info")
    return options.target

def scan_result(ip):

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
    client_list = []
    for element in answered_list:
        # Cada element es una lista de las respuestas (packet sent, answered) por
        # Ello se procede a solo imprimir el elemento de respuesta [1] aunque imprimira objetos
        # los cuales no tienen sentido por ello se procede a ir al metodo show
        # Igual se puede ir al metodo psr para imprimir la ip address del objetivo
        # Con hwsrc se imprime la MAC address del objetivo
        client_dict= {"ip": element[1].psrc, "MAC": element[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_result(result_list):
    print("IP\t\t\t       MAC Address\n-----------------------------------------------")
    for client in result_list:
        print(client["ip"]+"\t\t\t"+client["MAC"])


# La funcion scapy.arping puede bsucar dentro de un rango
options = get_args()
scan_result = scan_result(options)
print_result(scan_result)