import os
from subprocess import check_output
from os import listdir
from os.path import isfile, join
from re import findall


class Singleton(type):
    # region Singleton
    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)

    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args, **kw)
        return cls.__instance

    # endregion


class URLController:
    # region V1
    @staticmethod
    def fixUrl(url: str):
        if URLController.urlCorrecta(url) is False:
            url = url.replace("https://", '')
            url = url.replace("http://", '')
            url = url.split('/')[0]
        return url

    # Elimina el https://www. o http://www.
    # Dejando solo google.es
    @staticmethod
    def fixURLWhoIs(url: str):
        url = URLController.fixUrl(url)
        if url.startswith("www.") is True:
            url = url[4:]
        return url

    @staticmethod
    def isWhoisURLValid(url: str):
        return None

    @staticmethod
    def urlCorrecta(url: str):
        if url.__contains__('/'):
            resultado = False
        elif url.startswith("https://"):
            resultado = False
        elif url.startswith("http://"):
            resultado = False
        else:
            resultado = True
        return resultado

    @staticmethod
    def urlCorrectaType2(url: str):
        if url.startswith("https://"):
            resultado = True
        elif url.startswith("http://"):
            resultado = True
        else:
            resultado = False
        return resultado

    # endregion
    # region V2
    @staticmethod
    def fixUrlV2(url: str):
        value = URLController.urlCorrectaV2(url)
        if value == 2:
            url = url.replace("https://", '')
        elif value == 3:
            url = url.replace("http://", '')
        elif value == 1:
            url = url.split('/')[0]
        return url, value

    @staticmethod
    def fixURLWhoIsV2(url: str):
        url, value = URLController.fixUrlV2(url)
        if url.startswith("www.") is True:
            url = url[4:]
        return url, value

    @staticmethod
    def urlCorrectaV2(url: str):
        if url.__contains__("https://"):
            resultado = 2
        elif url.__contains__("http://"):
            resultado = 3
        elif url.__contains__('/'):
            resultado = 1
        else:
            resultado = 0
        return resultado

    @staticmethod
    def urlSimpleV1(url: str):
        flag = False
        if url.__contains__("www."):
            flag = True
        url, value = URLController.fixURLWhoIsV2(url)
        pos = url.find('.')
        tempurl = url
        if value == 2:
            url = "https://"
        elif value == 3:
            url = "http://"
        else:
            url = ""
        if flag:
            url += "www."
        url += tempurl[0:pos]
        return url

    # endregion
    # region V3
    @staticmethod
    def urlDom(url: str):
        # region Primera parte
        # Destripamos por partes
        flagHttp: int = 0
        if url.startswith("https://"):
            flagHttp = 1
            url = url.replace("https://", '', 1)
        elif url.startswith("http://"):
            flagHttp = 2
            url = url.replace("http://", '', 1)

        # Si aun quitando to.do aun quedan cosas lo quitamos to.do menos lo que queremos(el root)
        if url.__contains__('/'):
            url = url.split('/')[0]
        # endregion
        # region Segunda parte
        flagWww: int = 0
        if url.startswith("www."):
            url = url.replace("www.", '', 1)
            flagWww = 1
        # endregion
        # region Tercera parte
        url = url.split('.')[0]
        urlfinal = ""
        if flagHttp == 1:
            urlfinal += "https://"
        elif flagHttp == 2:
            urlfinal += "http://"
        if flagWww == 1:
            urlfinal += "www."
        # endregion
        return urlfinal + url

    @staticmethod
    def urlDomV2(url: str):
        # region Primera parte
        # Destripamos por partes
        flagHttp: int = 0
        if url.startswith("https://"):
            flagHttp = 1
            url = url.replace("https://", '', 1)
        elif url.startswith("http://"):
            flagHttp = 2
            url = url.replace("http://", '', 1)

        # Si aun quitando to.do aun quedan cosas lo quitamos to.do menos lo que queremos(el root)
        if url.__contains__('/'):
            url = url.split('/')[0]
        # endregion
        # region Segunda parte
        flagWww: int = 0
        if url.startswith("www."):
            url = url.replace("www.", '', 1)
            flagWww = 1
        # endregion
        # region Tercera parte
        urllist = url.split('.')
        fin = ""
        url = urllist[0]
        urlfinal = ""
        if flagHttp == 1:
            urlfinal += "https://"
        elif flagHttp == 2:
            urlfinal += "http://"
        if flagWww == 1:
            urlfinal += "www."
        if urllist.__len__() > 1:
            fin = urllist[1]
        # endregion
        return urlfinal + url, fin

    @staticmethod
    def urlRoot(url: str):
        if url[url.__len__() - 1] != '/':
            url += "/"
        return url

    @staticmethod
    def urlRootDom(url: str):
        dom, fin = URLController.urlDomV2(url)
        root = URLController.urlRoot(dom + '.' + fin)
        return dom, root

    @staticmethod
    def prepararUrl(url: str, root_url: str):
        if url.startswith('//'):
            url = url[2:]
        elif url.startswith('/'):
            url = url[1:]
        return f"{root_url}{url}"

    # endregion


class ControlVariables:
    @staticmethod
    def findAll(param: str, allstring: str):
        return findall(param, allstring)


    # region Control de variables
    @staticmethod
    def variableCorrecta(var: str):
        if var is None:
            resultado = False
        elif var.__len__() == 0:
            resultado = False
        else:
            resultado = True
        return resultado

    @staticmethod
    def variableCorrectaInt(var: int):
        if var is None:
            resultado = False
        elif var < 0:
            resultado = False
        else:
            resultado = True
        return resultado

    @staticmethod
    def variableCorrectaList(var: list):
        if var is None:
            resultado = False
        elif var.__len__() == 0:
            resultado = False
        else:
            resultado = True
            for i in var:
                resultado = ControlVariables.variableCorrecta(i)
                if resultado is False:
                    break
        return resultado

    @staticmethod
    def allTrueList(var: list):
        if var is None:
            resultado = False
        elif var.__len__() == 0:
            resultado = False
        else:
            resultado = True
            for i in var:
                resultado = i
                if resultado is False:
                    break
        return resultado

    @staticmethod
    def removeNullFromList(var: list):
        return ControlVariables.removeFromList(var, ControlVariables.variableCorrecta)

    @staticmethod
    def removeFromList(var: list, func):
        borrados: int = 0
        for i in range(0, var.__len__()):
            if type(var[i - borrados]) == str:
                if func(var[i - borrados]) is False:
                    del var[i - borrados]
                    borrados += 1
        return borrados

    @staticmethod
    def startWitnNum(var: str):
        resultado: bool = False
        if ControlVariables.variableCorrecta(var) is True:
            if var[0].isnumeric():
                resultado = True
        return resultado

    @staticmethod
    def stringIsNumeric(var: str):
        resultado: bool = False
        if ControlVariables.variableCorrecta(var) is True:
            if var.isnumeric():
                resultado = True
        return resultado

    @staticmethod
    def stringIsFloat(var: str):
        resultado: bool = False
        if ControlVariables.variableCorrecta(var) is True:
            if var.__contains__('.') is True:
                sep: list = var.split('.')
                if sep.__len__() == 2:
                    if ControlVariables.stringIsNumeric(sep[0]) and ControlVariables.stringIsNumeric(sep[1]):
                        resultado = True
        return resultado

    # Devuelve la posicion del string de la lista que esta contenido en el string
    @staticmethod
    def contains_any(string: str, list_strings: list):
        resultado: int = -1
        for i in range(0, list_strings.__len__()):
            if string.__contains__(list_strings[i]):
                resultado = i
                break
        return resultado

    # endregion


# Si devulve None el objeto no es una clase
class ClassAnalyzer:
    # region Analyzer
    @staticmethod
    def getClassNameString(class_object):
        return str(class_object.__class__).split("'")[1]

    @staticmethod
    def dictGeneratorClassVersion(class_object):
        class_name = ClassAnalyzer.getClassNameString(class_object)
        resultado = None
        if class_name is not None:
            var_list = vars(class_object)
            #print(var_list)
            dict_list: dict = {}
            for k in var_list:
                # temp
                class_and_var = k.split("__")
                # Claves y valores de la clase
                sub_class_name = class_and_var[0].replace("_", '')
                variable: str = class_and_var[1]
                value = var_list[k]
                if dict_list.__contains__(sub_class_name):
                    dict_list[sub_class_name].update({variable: value})
                else:
                    dict_list.update({sub_class_name: {variable: value}})
            if dict_list.__len__() == 1:
                for k in dict_list:
                    resultado = dict_list[k]
            else:
                resultado = dict_list
        return resultado

    @staticmethod
    def dictGeneratorClassVersionFull(class_object):
        class_name = ClassAnalyzer.getClassNameString(class_object)
        if class_name is not None:
            resultado = {class_name: ClassAnalyzer.dictGeneratorClassVersion(class_object)}
        else:
            resultado = None
        return resultado

    @staticmethod
    def findAndFixIntNegativeClassVersion(class_object):
        class_name = ClassAnalyzer.getClassNameString(class_object)
        resultado = None
        if class_name is not None:
            var_list = vars(class_object)
            #print(var_list)
            dict_list: dict = {}
            for k in var_list:
                print(k)
                # temp
                class_and_var = k.split("__")
                add: bool = False
                # Claves y valores de la clase
                sub_class_name = class_and_var[0].replace("_", '')
                variable: str = class_and_var[1]
                value = var_list[k]
                if type(value) == int:
                    if int(value) < 0:
                        add = True
                        exec("class_object." + variable + " = 0")
                elif type(value) == float:
                    if float(value) < 0.0:
                        add = True
                        exec("class_object." + variable + " = 0.0")
                elif isinstance(value, type):
                    instanceres = ClassAnalyzer.findAndFixIntNegativeClassVersion(value)
                    if instanceres is not None:
                        dict_list[sub_class_name].update({variable: instanceres})
                if add:
                    if dict_list.__contains__(sub_class_name):
                        dict_list[sub_class_name].update({variable: value})
                    else:
                        dict_list.update({sub_class_name: {variable: value}})
            if dict_list.__len__() == 1:
                for k in dict_list:
                    resultado = dict_list[k]
            else:
                resultado = dict_list
        return resultado

    @staticmethod
    def findAndFixIntNegativeClassVersionFull(class_object):
        class_name = ClassAnalyzer.getClassNameString(class_object)
        if class_name is not None:
            resultado = {class_name: ClassAnalyzer.findAndFixIntNegativeClassVersion(class_object)}
        else:
            resultado = None
        return resultado

    # endregion


class LlanyClass:
    def findAndFixIntNegative(self):
        return ClassAnalyzer.findAndFixIntNegativeClassVersion(self)

    def findAndFixIntNegativeFull(self):
        return ClassAnalyzer.findAndFixIntNegativeClassVersionFull(self)

    def getFullDict(self):
        return ClassAnalyzer.dictGeneratorClassVersionFull(self)

    def getDict(self):
        return ClassAnalyzer.dictGeneratorClassVersion(self)

    def __repr__(self):
        return str(self.getDict())


class FilesController:
    # region Easy
    @staticmethod
    def fileExistEasy(root: str, extension: str, filename: str):
        return os.path.isfile(root+filename+extension)

    def writeAppendEasy(self, root: str, extension: str, filename: str, content: str):
        self.comprobarExisteYCrear(root)
        if ControlVariables.variableCorrecta(extension) is False:
            f = open(root + filename, "a")
        else:
            f = open(root + filename + extension, "a")
        f.write(content)

    def writeAppendBytesEasy(self, root: str, extension: str, filename: str, contentbytes: bytes):
        self.comprobarExisteYCrear(root)
        if ControlVariables.variableCorrecta(extension) is False:
            f = open(root + filename, "ab")
        else:
            f = open(root + filename + extension, "ab")
        f.write(contentbytes)

    @staticmethod
    def openEasy(root: str, extension: str, filename: str):
        if ControlVariables.variableCorrecta(extension) is False:
            f = open(root + filename, "r")
        else:
            f = open(root + filename + extension, "r")
        return f.read()

    def openListEasy(self, root: str, extension: str, filename: str):
        return self.openEasy(root, extension, filename).split('\n')

    def openListsEasy(self, root: str, extension: str, filenames: list):
        lista: list = []
        for i in filenames:
            if type(i) == str:
                lista.append(self.openListEasy(root, extension, i))
        return lista

    def clearFileEasy(self, root: str, extension: str, filename: str):
        resultado: bool = False
        if self.fileExist(filename):
            CommandsController().execute_command(["rm", root + filename + extension])
            resultado = True
        return resultado

    def writeEasy(self, root: str, filename: str,  extension: str, content: str):
        fileall = f"{root}{filename}{extension}"
        f = open(fileall, "w")
        f.write(content)

    def writeEasy2(self, root: str, filename: str, content: str):
        fileall = f"{root}{filename}"
        f = open(fileall, "w")
        f.write(content)

    # endregion
    # region Normal
    @staticmethod
    def getFilesNames(dirname: str):
        return [f for f in listdir(dirname) if isfile(join(dirname, f))]

    @staticmethod
    def fileExist(filename: str):
        return os.path.isfile(filename)

    def writeAppend(self, filename: str, content: str):
        f = open(filename, "a")
        f.write(content)

    def writeAppendBytes(self, filename: str, contentbytes: bytes):
        f = open(filename, "ab")
        f.write(contentbytes)

    def open(self, filename: str):
        if self.fileExist(filename):
            f = open(filename, "r")
            contenido = f.read()
        else:
            contenido = None
        return contenido

    def openList(self, filename: str):
        return self.open(filename).split('\n')

    def openLists(self, filenames: list):
        lista: list = []
        for i in filenames:
            if type(i) == str:
                lista.append(self.openList(i))
        return lista

    def clearFile(self, filename: str):
        resultado: bool = False
        if self.fileExist(filename):
            CommandsController().execute_command(["rm", filename])
            resultado = True
        return resultado

    def write(self, filename: str, content: str):
        f = open(filename, "w")
        f.write(content)

    def getFiles(self, root: str, extension: list):
        var = ControlVariables()
        resultado: list = []
        if var.variableCorrectaList(extension) and var.variableCorrecta(root):
            for dp, dn, filenames in os.walk(root):
                for f in filenames:
                    if os.path.splitext(f)[1] in extension:
                        resultado.append({
                            "filename": f,
                            "path": f"{dp}{f}"
                        })
        else:
            print("WTF")
        return resultado

    # endregion
    # region Other
    @staticmethod
    def comprobarExisteYCrear(root: str):
        if os.path.exists(root) is False:
            os.mkdir(root)

    # endregion


class CommandsController:
    @staticmethod
    def __commandlistAnalizer(commandlist: list):
        return commandlist

    @staticmethod
    def execute_command(commandlist: list):
        newCommand = CommandsController.__commandlistAnalizer(commandlist)
        if newCommand is not None:
            try:
                resultado = check_output(commandlist).decode("utf-8").split("\n")
            except:
                resultado = None
        else:
            resultado = None
        return resultado


#print(FilesController().getFilesNames("../dict/"))
"""print(URLController.urlRoot("https://www.google.es/"))
print(URLController.urlRoot("https://jsonlint.com"))
print(URLController.urlRoot("https://9gag.com/gag/a7WBdOA"))

print(URLController.urlDom("https://www.google.es/"))
print(URLController.urlDom("https://jsonlint.com"))"""
# print(URLController.urlRootDom("https://9gag.com/gag/a7WBdOA"))

# print(URLController().urlCorrectaType2("https://jsonlint.com"))
