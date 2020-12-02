import webbrowser
from tkinter import messagebox
from GUI.guiclass import GeneralTab, GeneralButton, GeneralNotebook, GeneralVentana, GeneralMenuBar, GeneralMenu, \
    GeneralDivTab, GeneralTextAreaScrollTab, GeneralEntradaTexto, GeneralCombox, GeneralCheckBox
from Llanylib.SimpleTools import ControlVariables, URLController, FilesController
from Funcionalidades.FuncionesRastreator import Rastreator, RastreatorModes, RastreatorEvade
from Funcionalidades.FuncionesNmap import MyScanner
from Funcionalidades.FuncionesInfoServer import InfoServer
from Funcionalidades.FuncionesFuzz import FuzzAnalyzer

info: InfoServer = InfoServer()
varcontroller: ControlVariables = ControlVariables()
urlcontroller: URLController = URLController()
scanner: MyScanner = MyScanner()
files = FilesController()


# region Menu
class MainMenuHelp(GeneralMenu):
    def __init__(self, parent: GeneralMenuBar):
        super().__init__("Help", parent)
        self.nucleo.add_command(label="Help", command=self.__help)
        self.nucleo.add_command(label="Not help", command=self.__openNever)
        self.nucleo.add_separator()
        self.nucleo.add_command(label="Acerca de...", command=self.__opengit)

    def __help(self):
        if messagebox.askyesno("Help", "¿Necesitas ayuda?"):
            messagebox.showinfo("Help", "Entonces busca en google")

    def __openNever(self):
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO", new=2)

    def __opengit(self):
        if messagebox.askyesno("Acerca de ..", "Seguro que quiere abrir el enlace?"):
            webbrowser.open("https://github.com/Llanyro", new=2)


class MainMenu(GeneralMenuBar):
    def __init__(self, parent: GeneralVentana):
        super().__init__("Main menu", parent)
        MainMenuHelp(self)


# endregion
# region Tabs
# region InfoServer
# region URLtoIP
class MainURLtoIPDivTab(GeneralDivTab):
    def __init__(self, parent: GeneralTab):
        super().__init__("Div", parent)
        GeneralButton("URL to IP", self, 0, 0, command=self.urltoip)
        GeneralButton("Clear text!", self, 0, 1, command=self.clear)
        GeneralEntradaTexto("IP", self, 0, 2)
        GeneralButton("Enviar a NMAP", self, 0, 3, command=self.send)

    def getip(self):
        urltext = self.parent.parent.parent.get("URL")
        ip = None
        if urltext is None or varcontroller.variableCorrecta(urltext.getText()) is False:
            messagebox.showinfo("Aviso", "La url no puede estar vacia!")
        else:
            url = urltext.getText()
            if varcontroller.variableCorrecta(url):
                ip = info.getIPfromURL(url)
            else:
                messagebox.showinfo("WAT", "URL invalida\nIntroduce una url tipo:\nhttps://www.google.com")
        return ip

    def urltoip(self):
        ip = self.getip()
        if ip is not None:
            text = self.get("IP")
            if text is None:
                messagebox.showerror("Error", "Texto no encontrado!")
            else:
                text.setText(ip)

    def clear(self):
        text = self.get("IP")

        if text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            text.setText("")

    def send(self):
        ip = self.getip()
        if ip is not None:
            mainnmap = self.parent.parent.parent.parent.parent.get("Nmap")
            if mainnmap is None:
                messagebox.showinfo("Alert", "No se ha podido enviar la ip a NMAP")
            else:
                nmap = mainnmap.get("Div")
                if nmap is None:
                    messagebox.showinfo("Alert", "No se ha podido enviar la ip a NMAP div")
                else:
                    text = nmap.get("IP")
                    if text is None:
                        messagebox.showinfo("Alert", "No se ha podido enviar la ip a NMAP Text")
                    else:
                        text.setText(ip)


class MainURLtoIPTab(GeneralTab):
    def __init__(self, parent: GeneralNotebook):
        super().__init__("URL to IP", parent)
        MainURLtoIPDivTab(self)


# endregion
# region Locate
class MainLocateDivTab(GeneralDivTab):
    def __init__(self, parent: GeneralTab):
        super().__init__("Div", parent)
        GeneralButton("Locate", self, 0, 0, command=self.locate)
        GeneralButton("Clear text!", self, 0, 1, command=self.clear)
        GeneralTextAreaScrollTab("Ultimo resultado", self, 1, 0, 7)

    def printlocate(self, dic: dict):
        if dic['data_dict_response'] is True:
            text = self.get("Ultimo resultado")
            text.setText("")

            pais = dic.get('pais')
            ciudad = dic.get('ciudad')
            region = dic.get('region')
            latitud = dic.get('latitud')
            longitud = dic.get('longitud')

            if pais is not None:
                text.appendText(f"Pais: {pais}\n")
            if ciudad is not None:
                text.appendText(f"Ciudad: {ciudad}\n")
            if region is not None:
                text.appendText(f"Region: {region}\n")
            if latitud is not None:
                text.appendText(f"Latitud: {latitud}\n")
            if longitud is not None:
                text.appendText(f"Longitud: {longitud}\n")

    def locate(self):
        urltext = self.parent.parent.parent.get("URL")
        text = self.get("Ultimo resultado")

        if urltext is None or varcontroller.variableCorrecta(urltext.getText()) is False:
            messagebox.showinfo("Aviso", "La url no puede estar vacia!")
        elif text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            url = urltext.getText()
            if varcontroller.variableCorrecta(url):
                ip = info.getIPfromURL(url)
                dic = info.locate(ip)
                self.printlocate(dic)
            else:
                messagebox.showinfo("WAT", "URL invalida\nIntroduce una url tipo:\nhttps://www.google.com")

    def clear(self):
        text = self.get("Ultimo resultado")

        if text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            text.setText("")


class MainLocateTab(GeneralTab):
    def __init__(self, parent: GeneralNotebook):
        super().__init__("Locate", parent)
        MainLocateDivTab(self)


# endregion
# region Whois
class MainWhoIsDivTab(GeneralDivTab):
    def __init__(self, parent: GeneralTab):
        super().__init__("Div", parent)
        GeneralButton("Scan!", self, 0, 0, command=self.scan)
        GeneralButton("Clear text!", self, 0, 1, command=self.clear)
        GeneralTextAreaScrollTab("Ultimo resultado", self, 1, 0, 7)

    def printscan(self, dic_full: dict):
        text = self.get("Ultimo resultado")
        text.setText("")
        resultado = dic_full['data_dict_response']
        if resultado is False:
            text.appendText(f"No hay datos para la URL indicada\n")
        else:
            name = dic_full.get("name")
            registrar = dic_full.get("registrar")
            creation_date = dic_full.get("creation_date")
            expiration_date = dic_full.get("expiration_date")
            last_updated = dic_full.get("last_updated")
            status = dic_full.get("status")
            name_servers = dic_full.get("name_servers")

            if name is not None:
                text.appendText(f"Nombre: {name}\n")
            if registrar is not None:
                text.appendText(f"Registrador: {registrar}\n")
            if creation_date is not None:
                text.appendText(f"Fecha de creacion: {creation_date}\n")
            if last_updated is not None:
                text.appendText(f"Ultima acualizacion: {last_updated}\n")
            if status is not None:
                text.appendText(f"Estado: {status}\n")
            if name_servers is not None:
                text.appendText("Servidores:\n")
                for i in name_servers:
                    text.appendText(f"\t{i}\n")

    def scan(self):
        urltext = self.parent.parent.parent.get("URL")
        text = self.get("Ultimo resultado")

        if urltext is None or varcontroller.variableCorrecta(urltext.getText()) is False:
            messagebox.showinfo("Aviso", "La url no puede estar vacia!")
        elif text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            url = urltext.getText()
            if varcontroller.variableCorrecta(url):
                dic = info.getwhois(url)
                self.printscan(dic)
            else:
                messagebox.showinfo("WAT", "URL invalida\nIntroduce una url tipo:\nhttps://www.google.com")

    def clear(self):
        text = self.get("Ultimo resultado")

        if text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            text.setText("")


class MainWhoIsTab(GeneralTab):
    def __init__(self, parent: GeneralNotebook):
        super().__init__("WhoIs", parent)
        MainWhoIsDivTab(self)


# endregion
# region InfoVirusTotal
class MainInfoVirusTotalDivTab(GeneralDivTab):
    def __init__(self, parent: GeneralTab):
        super().__init__("Div", parent)
        GeneralButton("Scan!", self, 0, 0, command=self.scan)
        GeneralButton("Scan simple!", self, 0, 1, command=self.scansimple)
        GeneralButton("Clear text!", self, 0, 2, command=self.clear)
        GeneralTextAreaScrollTab("Ultimo resultado", self, 1, 0, 7)

    def printscan(self, dic_full: dict, completo: bool):
        text = self.get("Ultimo resultado")
        text.setText("")
        dic = dic_full.get('results')
        response_code_1 = dic_full.get('response_code')

        url = dic.get("url")
        response_code_2 = dic.get("response_code")
        positives = dic.get("positives")
        total = dic.get("total")
        scan_id = None
        resource = None
        scan_date = None
        permalink = None
        scans = None
        if completo:
            scan_id = dic.get("scan_id")
            resource = dic.get("resource")
            scan_date = dic.get("scan_date")
            permalink = dic.get("permalink")
            # verbose_msg = dic.get("verbose_msg")
            # filescan_id = dic.get("filescan_id")
            scans = dic.get("scans")

        if url is not None:
            text.appendText(f"Url: {url}\n")
        if resource is not None:
            text.appendText(f"Url original: {resource}\n")
        if scan_id is not None:
            text.appendText(f"ID del escaneo: {scan_id}\n")

        if positives is not None and total is not None:
            text.appendText(f"Resultados: {positives} / {total}\n")
        elif positives is not None:
            text.appendText(f"Resultados: {positives} / ???\n")
        elif total is not None:
            text.appendText(f"Resultados: ??? / {total}\n")

        if response_code_1 is not None and response_code_2 is not None:
            text.appendText(f"Response codes: {response_code_1}, {response_code_2}\n")
        elif response_code_1 is not None:
            text.appendText(f"Response codes: {response_code_1}, ???\n")
        elif response_code_2 is not None:
            text.appendText(f"Response codes: ???, {response_code_2}\n")

        if scan_date is not None:
            text.appendText(f"Fecha de escaneo: {scan_date}\n")
        if permalink is not None:
            text.appendText(f"Link permanente a Virustotal: {permalink}\n")
        if scans is not None:
            self.printscansdictlist(scans)

    def printscansdictlist(self, scans: dict):
        text = self.get("Ultimo resultado")
        text.appendText("Analizador\t\t\t\t\tResultado\t\t\tMensaje\n")
        for k in scans:
            linea = scans[k]
            if linea is not None:
                text.appendText(f"{k}")
            detectado = linea.get('detected')
            mens = linea.get('result')
            if detectado is not None:
                text.appendText(f"\t\t\t\t\t{detectado}")
            else:
                text.appendText("\t\t\t\t\t")
            if mens is not None:
                text.appendText(f"\t\t\t{mens}")
            else:
                text.appendText("\t\t\t")
            text.appendText("\n")

    def scan(self):
        urltext = self.parent.parent.parent.get("URL")
        text = self.get("Ultimo resultado")

        if urltext is None or varcontroller.variableCorrecta(urltext.getText()) is False:
            messagebox.showinfo("Aviso", "La url no puede estar vacia!")
        elif text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            url = urltext.getText()
            if urlcontroller.urlCorrectaType2(url):
                dic = info.getInfoVirusTotal(url)
                self.printscan(dic, True)
            else:
                messagebox.showinfo("WAT", "URL invalida\nIntroduce una url tipo:\nhttps://www.google.com")

    def scansimple(self):
        urltext = self.parent.parent.parent.get("URL")
        text = self.get("Ultimo resultado")

        if urltext is None or varcontroller.variableCorrecta(urltext.getText()) is False:
            messagebox.showinfo("Aviso", "La url no puede estar vacia!")
        elif text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            url = urltext.getText()
            if urlcontroller.urlCorrectaType2(url):
                dic = info.getInfoVirusTotal(url)
                self.printscan(dic, False)
            else:
                messagebox.showinfo("WAT", "URL invalida\nIntroduce una url tipo:\nhttps://www.google.com")

    def clear(self):
        text = self.get("Ultimo resultado")

        if text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            text.setText("")


class MainInfoVirusTotalTab(GeneralTab):
    def __init__(self, parent: GeneralNotebook):
        super().__init__("InfoVirusTotal", parent)
        MainInfoVirusTotalDivTab(self)


# endregion
# region WAFW00F
class MainWAFW00FDivTab(GeneralDivTab):
    def __init__(self, parent: GeneralTab):
        super().__init__("Div", parent)
        GeneralButton("Scan WAF!", self, 0, 0, command=self.waf)
        GeneralButton("Clear text!", self, 0, 1, command=self.clear)
        GeneralTextAreaScrollTab("Ultimo resultado", self, 1, 0, 7)

    def waf(self):
        urltext = self.parent.parent.parent.get("URL")
        text = self.get("Ultimo resultado")

        if urltext is None or varcontroller.variableCorrecta(urltext.getText()) is False:
            messagebox.showinfo("Aviso", "La url no puede estar vacia!")
        elif text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            url = urltext.getText()
            if urlcontroller.urlCorrectaType2(url):
                dic = info.getWAFwithWAFW00F(url)['data_dict_response']
                text.setText("")
                for i in dic:
                    text.appendText(f"{i}\n")
            else:
                messagebox.showinfo("WAT", "URL invalida\nIntroduce una url tipo:\nhttps://www.google.com")

    def clear(self):
        text = self.get("Ultimo resultado")

        if text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            text.setText("")


class MainWAFW00FTab(GeneralTab):
    def __init__(self, parent: GeneralNotebook):
        super().__init__("WAFW00F", parent)
        MainWAFW00FDivTab(self)


# endregion
class MainInfoServerNotebook(GeneralNotebook):
    def __init__(self, parent, row: int, column: int):
        super().__init__("FuzzNotebook", parent, row, column)
        MainLocateTab(self)
        MainWhoIsTab(self)
        MainInfoVirusTotalTab(self)
        MainWAFW00FTab(self)
        MainURLtoIPTab(self)


class MainInfoServerDivTab(GeneralDivTab):
    def __init__(self, parent: GeneralTab):
        super().__init__("Div", parent)
        GeneralEntradaTexto("URL", self, 0, 0)
        MainInfoServerNotebook(self, 1, 0)


class MainInfoServerTab(GeneralTab):
    def __init__(self, parent: GeneralNotebook):
        super().__init__("Info", parent)
        MainInfoServerDivTab(self)


# endregion
# region Fuzzers
# region Fuzzing
class MainFuzzingDivTab(GeneralDivTab):
    __dicts: list

    def __init__(self, parent: GeneralTab):
        super().__init__("Div", parent)
        self.__dicts = files.getFilesNames("./dict/")
        GeneralEntradaTexto("URL", self, 0, 0, columnspan=5)
        GeneralCombox("Diccionarios", self, 0, 5, self.__dicts)
        GeneralButton("Fuzz!", self, 1, 0, command=self.fuzz)
        GeneralButton("Clear text!", self, 1, 1, command=self.clear)
        GeneralButton("Example", self, 1, 2, command=self.example)
        GeneralTextAreaScrollTab("Ultimo resultado", self, 2, 0, 7)

    def example(self):
        text = self.get("URL")
        if text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            text.setText("https://www.google.es/{{dict_1}}/{{dict_2}}")

    def fuzz(self):
        urltext = self.get("URL")
        text = self.get("Ultimo resultado")

        if urltext is None or varcontroller.variableCorrecta(urltext.getText()) is False:
            messagebox.showinfo("Aviso", "La url no puede estar vacia!")
        elif text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            url = urltext.getText()
            if varcontroller.variableCorrecta(url):
                dicts_usados = varcontroller.findAll("{{(.+?)}}", url)
                fuzzer = FuzzAnalyzer(url, "./dict/", dicts_usados)
                resultados = fuzzer.getResults()
                self.printFuzz(resultados)
            else:
                messagebox.showinfo("WAT", "URL invalida\nIntroduce una url tipo:\nhttps://www.google.com")

    def printFuzz(self, li: list):
        text = self.get("Ultimo resultado")
        for i in li:
            text.appendText(f"Url: {i['url']}\n")
            text.appendText(f"\tResponse code: {i['response_code']}\n")
            text.appendText(f"\tContent length: {i['content_lenght']}\n")

    def clear(self):
        text = self.get("Ultimo resultado")

        if text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            text.setText("")


class MainFuzzingTab(GeneralTab):
    def __init__(self, parent: GeneralNotebook):
        super().__init__("Fuzzing", parent)
        MainFuzzingDivTab(self)


# endregion
# region Crawling
class MainCrawlingDivTab(GeneralDivTab):
    def __init__(self, parent: GeneralTab):
        super().__init__("Div", parent)
        GeneralEntradaTexto("URL", self, 0, 0)
        GeneralCombox("Diccionarios", self, 0, 1, files.getFilesNames("./dict/"))
        GeneralButton("Crawl", self, 1, 0, command=self.crawl)
        GeneralButton("Clear text!", self, 1, 1, command=self.clear)
        GeneralTextAreaScrollTab("Ultimo resultado", self, 2, 0, 7)

    def crawl(self):
        urltext = self.get("URL")
        text = self.get("Ultimo resultado")
        dictobj = self.get("Diccionarios")

        if urltext is None or varcontroller.variableCorrecta(urltext.getText()) is False:
            messagebox.showinfo("Aviso", "La url no puede estar vacia!")
        elif text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        elif dictobj is None or varcontroller.variableCorrecta(dictobj.getCurrentText()) is False:
            messagebox.showinfo("Aviso", "La url no puede estar vacia!")
        else:
            url = urltext.getText()
            dictname = dictobj.getCurrentText()
            if varcontroller.variableCorrecta(url) and varcontroller.variableCorrecta(dictname) and \
                    urlcontroller.urlCorrectaType2(url):
                dictname = dictname.split(".")[0]
                if url[:-1] == '/':
                    fuzzer = FuzzAnalyzer(f"{url}{{{{{dictname}}}}}", "./dict/", [dictname])
                else:
                    fuzzer = FuzzAnalyzer(f"{url}/{{{{{dictname}}}}}", "./dict/", [dictname])
                resultados = fuzzer.getResults()
                self.printCrawl(resultados)
            else:
                messagebox.showinfo("WAT", "URL invalida\nIntroduce una url tipo:\nhttps://www.google.com")

    def printCrawl(self, li: list):
        text = self.get("Ultimo resultado")
        for i in li:
            text.appendText(f"Url: {i['url']}\n")
            text.appendText(f"\tResponse code: {i['response_code']}\n")
            text.appendText(f"\tContent length: {i['content_lenght']}\n")

    def clear(self):
        text = self.get("Ultimo resultado")

        if text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            text.setText("")


class MainCrawlingTab(GeneralTab):
    def __init__(self, parent: GeneralNotebook):
        super().__init__("Crawling", parent)
        MainCrawlingDivTab(self)


# endregion
class MainFuzzersNotebook(GeneralNotebook):
    def __init__(self, parent, row: int, column: int):
        super().__init__("FuzzNotebook", parent, row, column)
        MainFuzzingTab(self)
        MainCrawlingTab(self)


class MainFuzzersDivTab(GeneralDivTab):
    def __init__(self, parent: GeneralTab):
        super().__init__("Div", parent)
        MainFuzzersNotebook(self, 0, 0)


class MainFuzzersTab(GeneralTab):
    def __init__(self, parent: GeneralNotebook):
        super().__init__("Fuzzers", parent)
        MainFuzzersDivTab(self)


# endregion
# region Nmap
class MainNMAPDivTab(GeneralDivTab):
    def __init__(self, parent: GeneralTab):
        super().__init__("Div", parent)
        # Basic
        GeneralEntradaTexto("IP", self, 0, 0)

        # Ports
        GeneralEntradaTexto("Ports", self, 1, 0)
        GeneralCombox("Ports Options", self, 1, 1, ["Top ports", "Custom ports"])

        # Options
        GeneralCheckBox("OS Scan", self, 2, 0)
        GeneralCheckBox("Scripts", self, 2, 1)
        GeneralCombox("TCP or UDP", self, 2, 2, ["TCP", "UDP"])
        GeneralCheckBox("Get service version", self, 2, 3)
        GeneralCheckBox("Agressive", self, 2, 4)

        # GeneralEntradaTexto("DelayText", self, 3, 0)
        GeneralCombox("BoxDelay", self, 3, 0, [0, 1, 2, 3, 4, 5])
        GeneralCheckBox("Delay?", self, 3, 1)

        # Resultados
        GeneralButton("Scan!", self, 4, 0, command=self.runNMAP)
        GeneralButton("Clear text!", self, 4, 1, command=self.clear)
        GeneralTextAreaScrollTab("Ultimo resultado", self, 5, 0, 7)

    def printResults(self, result: dict):
        status = result.get("status")
        text = self.get("Ultimo resultado")

        ip = result.get("ip")
        closed_ports = result.get("closed_ports")
        latencia = result.get("latencia")
        scanning_time = result.get("scanning_time")
        os_ = result.get("os")
        os_cpe = result.get("os cpe")
        os_pos = result.get("os pos")
        ports = result.get("ports")

        if varcontroller.variableCorrecta(ip) is False:
            messagebox.showinfo("Error", "Ip Desconocida???")
        else:
            text.setText(f"Ip: {ip}\n")
            text.setText(f"Estado: {status}\n")
            if varcontroller.variableCorrecta(closed_ports) is True:
                text.appendText(f"Puertos cerrados: {closed_ports}\n")
            if varcontroller.variableCorrecta(latencia) is True:
                text.appendText(f"Latencia: {latencia}\n")
            if varcontroller.variableCorrecta(scanning_time) is True:
                text.appendText(f"Tiempo de escaneo: {scanning_time}\n")
            if varcontroller.variableCorrecta(os_) is True:
                text.appendText(f"Sistema operativo: {os_}\n")
            if varcontroller.variableCorrecta(os_cpe) is True:
                text.appendText(f"OS CPE: {os_cpe}\n")
            if varcontroller.variableCorrecta(os_pos) is True:
                text.appendText(f"Posibles sistemas operativos: {os_pos}\n")
            if ports is not None and ports.__len__() > 0:
                for i in ports:
                    text.appendText(f"\nPuerto: {i['port']}\n")
                    text.appendText(f"\tProtocolo: {i['protocolo']}\n")
                    text.appendText(f"\tEstado: {i['state']}\n")
                    text.appendText(f"\tServicio: {i['servicio']}\n")

    def runNMAP(self):
        # nmap options
        ip_str: str = ""
        ports: str = ""
        delayval: int = -1
        os_scan_param: bool = False
        scripts_param: bool = False
        tcp_param: bool = False
        version_param: bool = False
        agressive_param: bool = False

        # Parametros
        ip = self.get("IP")
        portsoptions = self.get("Ports Options")

        os_scan = self.get("OS Scan")
        scripts = self.get("Scripts")
        tcp = self.get("TCP or UDP")
        version = self.get("Get service version")
        agressive = self.get("Agressive")
        delay = self.get("Delay?")
        text = self.get("Ultimo resultado")

        if ip is None or varcontroller.variableCorrecta(ip.getText()) is False:
            messagebox.showinfo("Aviso", "Ip no valida o null!")
        elif portsoptions is None or varcontroller.variableCorrectaInt(portsoptions.getCurrent()) is False:
            messagebox.showinfo("Error", "Ports is None!")
        elif delay is None or delay.var() is None or varcontroller.variableCorrectaInt(delay.var().get()) is False:
            messagebox.showinfo("Error", "Delay, var or value is None!")
        elif tcp is None or varcontroller.variableCorrectaInt(tcp.getCurrent()) is False:
            messagebox.showinfo("Error", "TCP/UDP is None!")
        elif text is None or issubclass(text.__class__, GeneralTextAreaScrollTab) is False:
            print("Text no valido")
        else:
            ip_str = ip.getText()

            if portsoptions.getCurrent() == 1:
                portslist = self.get("Ports")
                if portslist is None or varcontroller.variableCorrecta(portslist.getText()) is False:
                    print("Port list is None")
                else:
                    ports = portslist.getText()
                    if ports.__contains__(" "):
                        ports = ports.replace(' ', ',')
                        print(ports)

            if delay.var().get() == 1:
                bdelay = self.get("BoxDelay")
                if bdelay is None:
                    print("Box delay is none")
                else:
                    delayval = bdelay.getCurrent()

            if tcp.getCurrent() == 0:
                tcp_param = True
            else:
                tcp_param = False

            if os_scan.var().get() == 0:
                os_scan_param = False
            else:
                os_scan_param = True

            if scripts.var().get() == 0:
                scripts_param = False
            else:
                scripts_param = True

            if version.var().get() == 0:
                version_param = False
            else:
                version_param = True

            if agressive.var().get() == 0:
                agressive_param = False
            else:
                agressive_param = True

        if varcontroller.variableCorrecta(ip_str) is True:
            self.printResults(scanner.custom_command(ip_str, ports=ports, os_ana=os_scan_param, script=scripts_param,
                                                     tcp=tcp_param, version=version_param,
                                                     agressive=agressive_param, delay=delayval))
        """print(ip_str)
        print(ports)
        print(delayval)
        print(os_scan_param)
        print(scripts_param)
        print(tcp_param)
        print(version_param)
        print(agressive_param)"""
        """print(type(ip), ip.getText())
        print(type(portsoptions), portsoptions.getCurrent())
        print("Ports", ports)
        print(type(delay), type(delay.var()), delay.var().get())
        print(type(os_scan), type(os_scan.var()), os_scan.var().get())
        print(type(scripts), type(scripts.var()), scripts.var().get())
        print(type(tcp), type(tcp.var()), tcp.var().get())
        print(type(version), type(version.var()), version.var().get())
        print(type(agressive), type(agressive.var()), agressive.var().get())"""

    def clear(self):
        text = self.get("Ultimo resultado")

        if text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            text.setText("")


class MainNMAPTab(GeneralTab):
    def __init__(self, parent: GeneralNotebook):
        super().__init__("Nmap", parent)
        MainNMAPDivTab(self)


# endregion
# region Spider Tab
class MainSpiderBotonSpider(GeneralButton):
    def __init__(self, name: str, parent: GeneralDivTab, row: int, col: int):
        super().__init__(name, parent, row, col, command=self.__ejecutarSpiderSimple)

    def __comprobarValidezUrl(self, url: str):
        resultado: bool = False
        if varcontroller.variableCorrecta(url):
            if urlcontroller.urlCorrectaType2(url):
                resultado = True
        return resultado

    def __ejecutarSpiderSimple(self):
        print("Ejecutando Spider simple...")
        text = self.parent.get("url")
        box1 = self.parent.get("BoxModes")
        box2 = self.parent.get("BoxEvades")

        if text is None:
            print("Text es none")
        elif box1 is None:
            print("Box1 es none")
        elif box2 is None:
            print("Box2 es none")
        elif issubclass(text.__class__, GeneralEntradaTexto) is False and type(text) == GeneralEntradaTexto:
            print("Text no es sublcass de GeneralEntradaTexto y tampoco es GeneralEntradaTexto")
        elif issubclass(box1.__class__, GeneralCombox) is False and type(box1) == GeneralCombox:
            print("Box1 no es sublcass de GeneralCombox y tampoco es GeneralCombox")
        elif issubclass(box1.__class__, GeneralCombox) is False and type(box1) == GeneralCombox:
            print("Box1 no es sublcass de GeneralCombox y tampoco es GeneralCombox")
        else:
            url = text.getText()
            modo = box1.getCurrent()
            evade = box2.getCurrent()
            if self.__comprobarValidezUrl(url) and \
                    varcontroller.variableCorrectaInt(modo) and varcontroller.variableCorrectaInt(evade):
                self.parent.rastreator = Rastreator(url=url,
                                                    mode=RastreatorModes(modo),
                                                    evademode=RastreatorEvade(evade))
                self.parent.rastreator.start()
                self.parent.printSpider()
            else:
                messagebox.showinfo("Aviso", "No se ha introducido una url correcta!")


class MainSpiderDivTab(GeneralDivTab):
    __last_rastreator: Rastreator = None

    def __init__(self, parent: GeneralTab):
        super().__init__("Div", parent)
        GeneralEntradaTexto("url", self, 0, 0)
        GeneralCombox("BoxModes", self, 0, 1, ["Simple", "Rastreator"])
        GeneralCombox("BoxEvades", self, 0, 2, ["Simple", "CloudFlare"])

        MainSpiderBotonSpider("Spider!", self, 1, 0)
        GeneralButton("Clear text!", self, 1, 1, command=self.clear)
        GeneralTextAreaScrollTab("Ultimo resultado", self, 2, 0, 7)

    @property
    def rastreator(self):
        return self.__last_rastreator

    @rastreator.setter
    def rastreator(self, rast: Rastreator):
        self.__last_rastreator = rast

    def printSpider(self):
        text = self.get("Ultimo resultado")
        if text is None or issubclass(text.__class__, GeneralTextAreaScrollTab) is False:
            print("Text no valido")
        elif self.__last_rastreator is None:
            text.setText("Aun no se ha realizado ningun spider", True)
        else:
            dicti: dict = self.__last_rastreator.getDict()
            text.setText(f"Url solicitada: {dicti['url_original']}\n")
            text.appendText(f"Url root: {dicti['root_url']}\n")
            text.appendText(f"Nombre de la carpeta creada con los contenidos de los objetos: "
                            f"./Spider/{dicti['filename']}\n")
            text.appendText("Urls visitadas:\n")
            text.appendText("\tcode\tbytes\turl\n")
            for i in dicti["results"]:
                text.appendText(f"\t{i['status_code']}\t{i['bytes']}\t{i['url']}\n")
            text.appendText(f"Objetos encontrados:\n")
            for i in dicti["urlFind"]:
                text.appendText(f"\t{i}\n")
            text.appendText("", readonly=True)

    def clear(self):
        text = self.get("Ultimo resultado")

        if text is None:
            messagebox.showerror("Error", "Texto no encontrado!")
        else:
            text.setText("")


class MainSpiderTab(GeneralTab):
    def __init__(self, parent: GeneralNotebook):
        super().__init__("Rastreator", parent)
        MainSpiderDivTab(self)


# endregion
class MainNotebook(GeneralNotebook):
    def __init__(self, parent: GeneralVentana, row: int, column: int):
        super().__init__("Funcionalidades Notebook", parent, row, column)
        MainSpiderTab(self)
        MainNMAPTab(self)
        MainFuzzersTab(self)
        MainInfoServerTab(self)


# endregion
class MainVentana(GeneralVentana):
    def __init__(self, titulo: str):
        super().__init__(titulo)
        self.nucleo.geometry("800x600")
        MainNotebook(self, 0, 0)
        MainMenu(self)


v = MainVentana("Web Analysis GUI")
v.start()
