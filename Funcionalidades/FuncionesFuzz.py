import requests
from Llanylib.StringIterator import StringIterator
from Llanylib.SimpleTools import LlanyClass, FilesController


class FuzzAnalyzer(LlanyClass):
    __resultados: list

    def __init__(self, string: str, root: str, dict_names: list):
        self.__resultados = []
        iterator = StringIterator(string, self.make_request)
        iterator.dicts_values_dicts = FilesController().openListsEasy(root, ".dict", dict_names)
        iterator.procesarString()

    def make_request(self, url: str):
        resultado = requests.get(url=url)
        self.__resultados.append({
            "url": url,
            "response_code": resultado.status_code,
            "content_lenght": resultado.content.__len__()
        })

    def getResults(self):
        return self.__resultados

#f = FuzzAnalyzer("https://www.google.es/{{dict_1}}/{{dict_1}}/{{dict_2}}", "./dict/", ["dict_1", "dict_2"])
#f = FuzzAnalyzer("https://www.google.es/{{dict_1}}", "./dict/", ["dict_1"])
#print(f)

"""class Test2(LlanyClass):
    def func(self, function):
        function(1)


class Test(LlanyClass):
    __l: list
    __t: Test2

    def __init__(self):
        self.__l = []
        self.__t = Test2()

    def func(self, val):
        self.__l.append(val)

    def llamar(self):
        self.__t.func(self.func)


t = Test()
t.llamar()
t.llamar()
t.llamar()
print(t)"""

