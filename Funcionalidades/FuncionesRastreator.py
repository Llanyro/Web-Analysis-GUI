import cloudscraper
from sys import exit
from datetime import datetime
from re import findall
from enum import Enum
from requests import Response, Session
from Llanylib.SimpleTools import LlanyClass, FilesController, URLController


# region Enums
class SpiderModes(Enum):
    SIMPLE = 0
    FULL = 1


class SpiderEvade(Enum):
    NONE = 0
    CLOUDFLARE = 1


# endregion

class Spider(LlanyClass):
    # region Variables
    # Ej: https://www.google.es/  | https://jsonlint.com
    __url_original: str  # Url que se recibe   -> https://www.google.es/  | https://jsonlint.com
    __url_dom: str       # Url de tipo dominio -> https://www.google     | https://jsonlint
    __root_url: str      # Url para concat     -> https://www.google.es/  | https://jsonlint.com/

    __mode: SpiderModes
    __rastreatorEvade: SpiderEvade
    __petitionObject = None
    __cookies: dict
    __url_list: list
    __urlFind: list
    __results: list
    __filename: str
    __root: str
    __extension_busqueda: list
    __objetos_busqueda: list  # Lista de objetos que matchean la busqueda especifica

    # endregion
    # region Funciones
    def __init__(self, url: str, mode: SpiderModes = SpiderModes.SIMPLE,
                 evademode: SpiderEvade = SpiderEvade.NONE, cookies=None):
        if cookies is None:
            cookies = {}

        # Inicializacion de variables
        self.__url_original = url
        self.__url_dom, self.__root_url = URLController.urlRootDom(url)
        self.__url_list = [url]
        self.__filename = datetime.now().__str__()
        self.__root = "./Spider/"
        self.__extension_busqueda = []
        self.__objetos_busqueda = []
        self.__urlFind = []
        self.__results = []
        self.__mode = mode
        self.__rastreatorEvade = evademode
        self.__cookies = cookies

        # Funciones
        FilesController().comprobarExisteYCrear(self.__root)
        self.__generatePetitionsObject()

    def __generatePetitionsObject(self):
        if self.__rastreatorEvade == SpiderEvade.NONE:
            self.__petitionObject = Session()
        elif self.__rastreatorEvade == SpiderEvade.CLOUDFLARE:
            self.__petitionObject = cloudscraper.create_scraper()
        else:
            print("Has introducido un Evade fuera del rango")
            exit()
        for i in self.__cookies:
            self.__petitionObject.cookies.set(i, self.__cookies[i])

    def __saveUrlList(self, url: str):
        if self.__mode == SpiderModes.FULL:
            if self.__url_list.__contains__(url) is False:
                self.__url_list.append(url)
        self.__urlFind.append(url)

    def __saveList(self, content: list):
        for i in content:
            if URLController.urlCorrectaType2(i):
                self.__saveUrlList(i)
            else:
                self.__saveUrlList(URLController.prepararUrl(i, self.__root_url))

    def __analizarContenido(self, contenido: str):
        self.__saveList(findall("src=\"(.+?)\"", contenido))
        self.__saveList(findall("href=\"(.+?)\"", contenido))

    def __guardarResultadoRequest(self, resultado: Response, pos: int):
        contenido = resultado.text
        FilesController().writeAppendEasy(
            f"{self.__root}{self.__filename}/", ".txt", self.__filename + f"({pos})", contenido)
        self.__analizarContenido(contenido)

    def __getSpider(self, pos: int):
        resultado = self.__petitionObject.get(self.__url_list[pos])
        print(f"Pos: {pos}, StatusCode: {resultado.status_code}, Url: {self.__url_list[pos]}")
        self.__results.append({
            "status_code": resultado.status_code,
            "url": self.__url_list[pos],
            "bytes": resultado.content.__len__()
        })
        if self.__url_list[pos].startswith(self.__url_dom):
            self.__guardarResultadoRequest(resultado, pos)

    def start(self):
        pos: int = 0
        while pos < self.__url_list.__len__():
            self.__getSpider(pos)
            pos += 1
        print(f"Fin! Pos: {pos}")

    # endregion
    # region Busquedas especificas
    def __contineneParametroDeBusqueda(self, string: str):
        resultado: bool = False
        for i in self.__extension_busqueda:
            if string.__contains__(i):
                resultado = True
                break
        return resultado

    def __comprobarParametroYAgregar(self, i: str):
        if self.__contineneParametroDeBusqueda(i):
            if self.__objetos_busqueda.__contains__(i) is False:
                self.__objetos_busqueda.append(i)

    # endregion


"""# s = Spider("https://9gag.com/gag/a7WBdOA", [".jpg"])
s = Spider(url="https://9gag.com/gag/a7WBdOA", evademode=SpiderEvade.CLOUDFLARE)
# s = Spider("https://9gag.com/gag/a7WBdOA", SpiderModes.SIMPLE)
# s = Spider("https://jsonlint.com/", [])
# s = Spider("http://www.google.es", [], SpiderModes.SIMPLE)
# s = Spider("https://www.virustotal.com/gui/home/url.", [], SpiderModes.SIMPLE)
s.start()
print(s)"""
