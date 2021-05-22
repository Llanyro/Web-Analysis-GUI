from Llanylib.SimpleTools import ControlVariables, CommandsController


class MyScanner:
    # region Priv
    # Aanaliza la lista de comandos para no tener terminal injection
    @staticmethod
    def __generate_command_nmap(ip: str, ports: str = "",
                                os_ana: bool = False, script: bool = False, tcp: bool = True,
                                version: bool = False, agressive: bool = False, delay: int = -1):
        commandlist: list = []
        if ControlVariables.variableCorrecta(ip):
            commandlist.append("nmap")
            commandlist.append(ip)
            if agressive is True:
                # print("Pls no seas agresivo")
                commandlist.append("-A")
            else:
                if script is True:
                    commandlist.append("-sC")
                elif version is True:
                    commandlist.append("-sV")
                elif os_ana is True:
                    commandlist.append("-O")
            if tcp is True or tcp:
                commandlist.append("-sS")
            else:
                commandlist.append("-sU")
            if ControlVariables.variableCorrectaInt(delay) is True:
                if 0 <= delay <= 5:
                    commandlist.append(f"-T{delay}")
            if ControlVariables.variableCorrecta(ports) is True:
                if ports == "all":
                    commandlist.append("-p-")
                else:
                    commandlist.append(f"-p {ports}")
        return commandlist



    @staticmethod
    def __analizar_puerto(linea_completa: str, paramentros_de_los_puertos: int):
        dict_port: dict = {}

        linea_split: list = linea_completa.split(' ')
        ControlVariables.removeNullFromList(linea_split)
        puerto_y_protocolo = linea_split[0].split("/")

        dict_port.update({
            "port": puerto_y_protocolo[0],
            "protocolo": puerto_y_protocolo[1],
            "state": linea_split[1],
            "servicio": linea_split[2]
        })
        if paramentros_de_los_puertos == 4:
            if linea_split.__len__() == 5:
                dict_port.update({"version": linea_split[3] + " " + linea_split[4]})
            elif linea_split.__len__() == 4:
                dict_port.update({"version": linea_split[3]})
            else:
                dict_port.update({"version": "desconocido"})
        #if paramentros_de_los_puertos == linea_split.__len__():
        #    dict_port.update({"version": linea_split[3]})
        #elif paramentros_de_los_puertos > linea_split.__len__():
        #    dict_port.update({"version": "".join('a' for a in range())})
        return dict_port

    # Actualemente funciona con -sS, -O, -sU(Prob), -A, -sV
    @staticmethod
    def __analizar_nmap_results(result: list):
        dict_final: dict = {}
        if result is not None:
            lista_diccionarios_puertos: list = []
            paramentros_de_los_puertos: int = 0
            ControlVariables.removeNullFromList(result)
            for linea_a_analizar in result:
                # region startswith
                if linea_a_analizar.startswith("Not shown:"):
                    dict_final.update({"closed_ports": linea_a_analizar.split(": ")[1].split(' ')[0]})
                elif linea_a_analizar.startswith("All "):
                    dict_final.update({"closed_ports": linea_a_analizar.split(" ")[1]})
                elif linea_a_analizar.startswith("Host is up"):
                    dict_final.update({"status": "up"})
                    dict_final.update({"latencia": linea_a_analizar.split(' ')[3].replace('(', '')})
                elif linea_a_analizar.startswith("Note:"):
                    dict_final.update({"status": "down"})
                elif linea_a_analizar.startswith("Nmap done:"):
                    dict_final.update({"scanning_time": linea_a_analizar.split("scanned in ")[1].split(' ')[0]})
                elif linea_a_analizar.startswith("OS details"):
                    dict_final.update({"os": linea_a_analizar.split(": ")[1]})
                elif linea_a_analizar.startswith("OS CPE"):
                    dict_final.update({"os cpe": linea_a_analizar.split(": ")[1]})
                elif linea_a_analizar.startswith("Running (JUST GUESSING):"):
                    dict_final.update({"os pos": linea_a_analizar.split(": ")[1]})
                elif linea_a_analizar.startswith("PORT"):
                    lista = linea_a_analizar.split(' ')
                    ControlVariables.removeNullFromList(lista)
                    paramentros_de_los_puertos = lista.__len__()
                elif linea_a_analizar.startswith("Nmap scan"):
                    linea_list = linea_a_analizar.split(' ')
                    ip: str = linea_list[len(linea_list) - 1]
                    #print(ip)
                    ip = ip.replace('(', '').replace(')', '')
                    #print(ip)
                    dict_final.update({"ip": ip})
                # endregion
                elif ControlVariables.startWitnNum(linea_a_analizar):
                    if linea_a_analizar.__contains__("returning data.") is False:
                        lista_diccionarios_puertos.append(
                            MyScanner.__analizar_puerto(
                                linea_a_analizar,
                                paramentros_de_los_puertos))
                elif linea_a_analizar.startswith("SF:"):
                    print(linea_a_analizar)
                else:
                    print(linea_a_analizar)

            if lista_diccionarios_puertos.__len__() > 0:
                dict_final.update({"ports": lista_diccionarios_puertos})
        return dict_final

    # endregion
    # region Public
    def custom_command(self, ip: str, ports: str = "",
                       os_ana: bool = False, script: bool = False, tcp: bool = True,
                       version: bool = False, agressive: bool = False, delay: int = -1):
        command = self.__generate_command_nmap(ip, ports=ports, os_ana=os_ana,
                                               script=script, tcp=tcp, version=version,
                                               agressive=agressive, delay=delay)
        print(command)
        return MyScanner.__analizar_nmap_results(CommandsController.execute_command(command))

    def scan_top_ports_ip(self, ip: str):
        return self.custom_command(ip)

    # endregion

"""print(nmap3.Nmap().scan_top_ports("www.google.es"))
print(NMAPController.scan_top_ports_url("www.google.es"))
print(NMAPController.scan_ip_url("www.google.es"))
print(NMAPController.nmap_os_detection(NMAPController.scan_ip_url("www.google.es")))"""
"""print(MyScanner.get_ip_url("www.google.es"))
print(MyScanner.scan_top_ports_ip("localhost"))
print(MyScanner.scan_top_ports_ip("www.google.es"))"""
"""print(MyScanner.generate_command_nmap(ip="localhost"))
print(MyScanner.generate_and_analize(ip="localhost"))"""
# print(MyScanner().scan_top_ports_ip("8.8.8.8"))
# print(MyScanner.custom_command(ip="localhost", os_ana=True, tcp=True, agressive=True))
