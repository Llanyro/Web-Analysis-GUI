from Llanylib.SimpleTools import LlanyClass, ControlVariables


class StringIterator(LlanyClass):
    # region Variables
    __string: str
    __dicts_values: list
    __dicts_values_dicts: list
    __funcion = None

    # endregion
    # region Constructores
    def __init__(self, string: str, function=None):
        self.__string = string
        self.__dicts_values = []
        self.__dicts_values_dicts = []
        self.__funcion = function
        self.__prepare()

    # endregion
    # region Private
    def __prepare(self):
        primer: list = self.__string.split("{{")
        segundo: list = []
        for i in primer:
            if i.__contains__("}}"):
                segundo.append(i.split("}}"))
            else:
                segundo.append(i)
        for i in range(0, segundo.__len__()):
            temp = segundo[i]
            if type(temp) == list:
                if self.__dicts_values.__contains__(temp[0]) is False:
                    self.__dicts_values.append(temp[0])

    def __save_or_restart(self, string_process: str):
        pos: int = ControlVariables.contains_any(string_process, self.__dicts_values)
        if pos == -1:
            if self.__funcion is not None:
                self.__funcion(string_process)
            else:
                print(string_process)
        else:
            self.__procesarString(string_process, pos)

    def __procesarString(self, string_process: str, pos_dict: int):
        for i in self.__dicts_values_dicts[pos_dict]:
            if i.__len__() > 0:
                nueva_string: str = string_process.replace('{{' + self.__dicts_values[pos_dict] + '}}', i, 1)
                self.__save_or_restart(nueva_string)

    def __sepuedeAdd(self):
        return self.__dicts_values.__len__() > self.__dicts_values_dicts.__len__()

    # endregion
    # region Getters
    @property
    def string(self):
        return self.__string

    @property
    def dicts_values(self):
        return self.__dicts_values

    @property
    def dicts_values_dicts(self):
        return self.__dicts_values_dicts

    @property
    def funcion(self):
        return self.__funcion

    # endregion
    # region Setters
    @funcion.setter
    def funcion(self, value):
        self.__funcion = value

    @dicts_values_dicts.setter
    def dicts_values_dicts(self, value: list):
        if value.__len__() == self.__dicts_values.__len__():
            self.__dicts_values_dicts = value
        else:
            print("Introduce una lista con tantos diccionarios como variables diferentes quieres iterar")

    # endregion
    # region Public
    def addDictlist(self, dict_list: list):
        resultado: bool = False
        if self.__sepuedeAdd():
            resultado = True
            self.__dicts_values_dicts.append(dict_list)
        return resultado

    def removeDictList(self, pos: int):
        del self.__dicts_values_dicts[pos]

    def procesarString(self) -> bool:
        resultado: bool = False
        if self.__sepuedeAdd() is False:
            resultado = True
            self.__save_or_restart(self.__string)
        else:
            print("Hay que poner tantos diccionadios como variables diferentes")
        return resultado

    # endregion


s = StringIterator("https://www.google.es/{{dict_1}}/{{dict_2}}/{{dict_2}}", None)
s.dicts_values_dicts = [["a"], ["b"]]
s.procesarString()
