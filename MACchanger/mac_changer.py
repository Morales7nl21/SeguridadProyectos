#!/usr/bin/env python
import subprocess
import optparse

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    # creamos dos objetos a los cuales le asignamos a lo que devuelva parser.parse_args()
    # options tendra la interface y mac  y los argumentos seran --interface y --mac
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Por favor especifica interface, use --help para mas info")
    elif not options.new_mac:
        parser.error("[-] Por favor especifica nueva mac, use --help para mas info")

    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC adress for " + interface + " to " + new_mac)
    # Con subprocess.call("comando a ejecutar en string", shell=True)
    # No es seguro debido a que el comando lo metemos como una cadena y podemos colgar mas comandos

    # subprocess.call("ifconfig " + interface + " down", shell=True)
    # subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
    # subprocess.call("ifconfig " + interface + " up", shell=True)

    # Es mas seguro usar subprocess.call(["comando", "argumentos"]) dentro de una lista
    # Asi solo ejecuta el comando y lo demas lo toma como argumentos no puede ejecutar otro comando
    # Cada elemnto es una palabra donde el primero es el comando a ejecutar
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

options = get_args()

# change_mac(options.interface, options.new_mac)
ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
print(ifconfig_result)