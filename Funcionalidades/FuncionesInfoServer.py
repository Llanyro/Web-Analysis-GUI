import whois
import socket
import geoip2.database
import requests
from Llanylib.SimpleTools import ControlVariables, URLController, CommandsController
from virus_total_apis import PublicApi


class InfoServer:
    __data_dict_response = "data_dict_response"
    __publicApi = "9937e4389b47e585c379961a9c932e29cd99486ca7fe739c56e2ca9b7c62afeb"

    def locate(self, ip: str):
        result: dict = {"data_dict_response": True}
        if ControlVariables.variableCorrecta(ip) is True:
            try:
                with geoip2.database.Reader('./Funcionalidades/geolite2_city.mmdb') as gi:
                    rec = gi.city(ip)
                    result.update({
                        "pais": rec.country.name,
                        "ciudad": rec.city.name,
                        "region": rec.subdivisions.most_specific.name,
                        "latitud": rec.location.latitude,
                        "longitud": rec.location.longitude
                          })
            except:
                result[self.__data_dict_response] = False
        else:
            result[self.__data_dict_response] = False
        return result

    def getwhois(self, url: str):
        result: dict = {"data_dict_response": True}
        if ControlVariables.variableCorrecta(url) is True:
            url = URLController.fixURLWhoIs(url)
            try:
                result.update(whois.query(url).__dict__)
            except:
                result[self.__data_dict_response] = False
        else:
            result[self.__data_dict_response] = False
        return result

    def getIPfromURL(self, url: str):
        if URLController.urlCorrecta(url) is False:
            url = URLController.fixUrl(url)
        try:
            resultado = socket.gethostbyname(url)
        except:
            resultado = None
        return resultado

    def getInfoVirusTotal(self, url: str):
        return PublicApi(self.__publicApi).get_url_report(url)

    def getWAFwithWAFW00F(self, url: str):
        all_list: list = CommandsController.execute_command(["wafw00f", url])
        del all_list[all_list.__len__() - 1]
        continuar: bool = True
        while continuar:
            if all_list[0].startswith('['):
                continuar = False
            else:
                del all_list[0]
        if len(all_list) > 10:
            all_list[1] = all_list[1].replace("\x1b[1;94m", '')
            all_list[1] = all_list[1].replace("\x1b[0m", '')
            all_list[1] = all_list[1].replace("\x1b[1;96m", '')
            all_list[1] = all_list[1].replace("\x1b[0m", '')
        for i in range(all_list.__len__()):
            all_list[i] = all_list[i][4:]
        return {self.__data_dict_response: all_list}

    def getIPVv4InfoName(self, name: str):
        result = requests.get(f"https://www.ipv4info.com/?act=check&ip={name}")

    def getIPVv4InfoIP(self, ip: str):
        result = requests.get(f"https://www.ipv4info.com/?act=check&ip={ip}")


"MTUyNjIwMTc2MTgtWkc5dWRDQmlaU0JsZG1scy0xNjA0MjgwNzk2LjU4Nw=="

"""print(InfoServer().getwhois("google.com"))
print(InfoServer().getwhois("https://google.com"))
print(InfoServer().getwhois("https://www.google.com"))
print(InfoServer().getwhois("google.es"))
print(InfoServer().getwhois("https://google.es"))
print(InfoServer().getwhois("https://www.google.es"))"""
# print(InfoServer().locate(InfoServer().getIPfromURL("https://www.google.es")))
# print(InfoServer().locate("83.43.119.73"))
# print(InfoServer().getIPfromURL("https://www.google.es"))

# InfoServer().getInfoVirusTotal("https://www.google.es")
# print(InfoServer().getWAFwithWAFW00F("https://www.9gag.com"))
# print(InfoServer().getWAFwithWAFW00F("https://www.google.es"))
# print(InfoServer().getWAFwithWAFW00F("asddf"))
# print(InfoServer().getWAFwithWAFW00F("https://www.google.es"))
