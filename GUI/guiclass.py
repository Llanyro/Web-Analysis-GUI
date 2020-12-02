from tkinter import TOP, Button, Tk, E, W, N, S, messagebox, Menu, Scrollbar, Text, RIGHT, Y, LEFT, END, DISABLED, \
    NORMAL, Entry, Checkbutton, IntVar, PhotoImage
from tkinter.ttk import Notebook, Frame, Combobox


class GeneralVentana:
    __name: str
    __item_dict: dict
    __ventana: Tk
    __menubar = None

    def __init__(self, titulo: str):
        self.__name = titulo
        self.__item_dict = {}
        self.__ventana = Tk()
        self.__ventana.title(titulo)
        self.__ventana.protocol("WM_DELETE_WINDOW", self.closeWindow)

    def start(self):
        self.__ventana.mainloop()

    def closeWindow(self):
        if messagebox.askokcancel("Salir", "Quieres salir?"):
            print("Guardando datos...")
            self.__ventana.destroy()

    def addItem(self, item):
        if type(item) == GeneralNotebook:
            self.__item_dict.update({"type": "notebook", "item": item})

    @property
    def nucleo(self):
        return self.__ventana

    def setMenuBar(self, menu):
        if type(menu) == GeneralMenuBar:
            self.__menubar = menu


# region Objetos Individuales Linkeables


# endregion
# region Rama Tabs
class GeneralNotebook:
    __parent = None
    __name: str
    __tab_list: list
    __notebook: Notebook

    def __init__(self, name: str, parent, row: int, column: int):
        if type(parent) != GeneralDivTab and issubclass(parent.__class__, GeneralDivTab) is not True and \
                type(parent) != GeneralVentana and issubclass(parent.__class__, GeneralVentana) is not True:
            raise Exception
        self.__parent = parent
        self.__name = name
        self.__tab_list = []
        self.__parent.addItem(self)
        self.__notebook = Notebook(parent.nucleo)
        self.__notebook.grid(row=row, column=column, sticky=E+W+N+S)
        self.__parent.nucleo.bind("<Configure>", self.conf)

    def conf(self, event):
        # print(event)
        alto = self.__parent.nucleo.winfo_height()
        largo = self.__parent.nucleo.winfo_width()
        # self.__notebook.config(height=alto, width=int((largo*8)/10))

    def addItem(self, tab):
        if type(tab) == GeneralTab or issubclass(tab.__class__, GeneralTab):
            self.__tab_list.append(tab)
        else:
            print(tab.__class__, "No añadido")

    def get(self, id: str):
        item = None
        for i in self.__tab_list:
            if i.name == id:
                item = i
                break
        return item

    @property
    def name(self):
        return self.__name

    @property
    def nucleo(self):
        return self.__notebook

    @property
    def parent(self):
        return self.__parent


class GeneralTab:
    __parent: GeneralNotebook
    __name: str
    __div_list: list
    __tab: Frame
    __dict_keys: list = ("type", "item")

    def __init__(self, name: str, parent: GeneralNotebook):
        self.__parent = parent
        self.__name = name
        self.__div_list = []
        self.__parent.addItem(self)
        self.__tab = Frame(parent.nucleo)
        self.__parent.nucleo.add(self.__tab, text=self.__name, compound=TOP, sticky=N+S+E+W)

    def addItem(self, item):
        if type(item) == GeneralDivTab or issubclass(item.__class__, GeneralDivTab):
            self.__div_list.append(item)
        else:
            print(item.__class__)

    def get(self, id: str):
        item = None
        for i in self.__div_list:
            if i.name == id:
                item = i
                break
        return item

    @property
    def name(self):
        return self.__name

    @property
    def nucleo(self):
        return self.__tab

    @property
    def parent(self):
        return self.__parent


class GeneralDivTab:
    __parent: GeneralTab
    __name: str
    __row: int
    __col: int
    __object_list: list
    __div: Frame
    __dict_keys: list = ("type", "item")

    def __init__(self, name: str, parent: GeneralTab, row: int = 0, col: int = 0):
        self.__parent = parent
        self.__name = name
        self.__row = row
        self.__col = col
        self.__object_list = []
        self.__parent.addItem(self)
        self.__div = Frame(parent.nucleo)
        self.__div.grid(row=self.__row, column=self.__col, sticky=N+S+E+W)

    # region Funciones Div
    def get(self, id: str):
        item = None
        for i in self.__object_list:
            if i[self.__dict_keys[1]].name == id:
                item = i[self.__dict_keys[1]]
                break
        return item

    def addItem(self, item):
        if type(item) == GeneralButton or issubclass(item.__class__, GeneralButton):
            self.__object_list.append({self.__dict_keys[0]: "button", self.__dict_keys[1]: item})
        elif type(item) == GeneralTextAreaScrollTab or issubclass(item.__class__, GeneralTextAreaScrollTab):
            self.__object_list.append({self.__dict_keys[0]: "text", self.__dict_keys[1]: item})
        elif type(item) == GeneralEntradaTexto or issubclass(item.__class__, GeneralEntradaTexto):
            self.__object_list.append({self.__dict_keys[0]: "text_insert", self.__dict_keys[1]: item})
        elif type(item) == GeneralCombox or issubclass(item.__class__, GeneralCombox):
            self.__object_list.append({self.__dict_keys[0]: "box", self.__dict_keys[1]: item})
        elif type(item) == GeneralCombox or issubclass(item.__class__, GeneralCheckBox):
            self.__object_list.append({self.__dict_keys[0]: "check_box", self.__dict_keys[1]: item})
        elif type(item) == GeneralNotebook or issubclass(item.__class__, GeneralNotebook):
            self.__object_list.append({self.__dict_keys[0]: "notebook", self.__dict_keys[1]: item})
        else:
            print(item.__class__)

    @property
    def name(self):
        return self.__name

    @property
    def nucleo(self):
        return self.__div

    @property
    def row(self):
        return self.__row

    @property
    def col(self):
        return self.__col

    @row.setter
    def row(self, value: int):
        self.__row = value

    @col.setter
    def col(self, value: int):
        self.__col = value

    @property
    def parent(self):
        return self.__parent

    # endregion


class GeneralTextAreaScrollTab:
    __parent: GeneralDivTab
    __name: str
    __text: Text = None
    __scroll: Scrollbar = None

    # def __init__(self, name: str, parent: GeneralDivTab, fill=Y, height=4, width=50):
    def __init__(self, name: str, parent: GeneralDivTab, row: int, col: int, columnspan: int):
        self.__name = name
        self.__parent = parent
        self.__scroll = Scrollbar(self.__parent.nucleo)
        self.__text = Text(self.__parent.nucleo)

        # self.__scroll.pack(side=RIGHT, fill=fill)
        # self.__text.pack(side=LEFT, fill=fill)
        # self.__text.rowconfigure(self.__parent.nucleo, 0, weight=1)
        # self.__text.columnconfigure(self.__parent.nucleo, 0, weight=1)

        self.__text.grid(row=row, column=col, columnspan=columnspan, sticky=N+S+E+W)
        self.__scroll.grid(row=row, column=col + columnspan + 1, sticky=N+S)

        self.__scroll.config(command=self.__text.yview)
        self.__text.config(yscrollcommand=self.__scroll.set)

        self.__parent.addItem(self)

    # region Funciones
    @property
    def parent(self):
        return self.__parent

    def appendText(self, contenido: str, readonly: bool = False):
        if self.__text is not None:
            self.__text.insert(END, contenido)
            self.setReadOnly(readonly=readonly)

    def clearText(self):
        if self.__text is not None:
            self.__text.delete('1.0', END)

    def setText(self, contenido: str, readonly: bool = False):
        self.clearText()
        self.appendText(contenido, readonly=readonly)

    def setReadOnly(self, readonly: bool):
        if readonly:
            self.__text.config(state=DISABLED)
        else:
            self.__text.config(state=NORMAL)

    @property
    def name(self):
        return self.__name

    # endregion


class GeneralEntradaTexto:
    __parent: GeneralDivTab
    __name: str
    __text: Entry

    # def __init__(self, name: str, parent: GeneralDivTab, fill=Y, height=4, width=50, side=RIGHT):
    def __init__(self, name: str, parent: GeneralDivTab, row: int, col: int, height=4, width=50, columnspan=1):
        self.__name = name
        self.__parent = parent
        self.__text = Entry(self.__parent.nucleo)
        # self.__text.pack(side=side, fill=fill)
        self.__text.grid(row=row, column=col, columnspan=columnspan, sticky=N+S+E+W)
        self.__parent.addItem(self)

    # region Funciones
    def getText(self):
        return self.__text.get()

    @property
    def name(self):
        return self.__name

    @property
    def parent(self):
        return self.__parent

    def clearText(self):
        if self.__text is not None:
            self.__text.delete(0, END)

    def setText(self, contenido: str):
        self.clearText()
        self.__text.insert(0, contenido)

    # endregion


class GeneralButton:
    __parent: GeneralDivTab
    __name: str
    __button: Button

    def __init__(self, name: str, parent: GeneralDivTab, row: int, col: int, command=None):
        self.__parent = parent
        self.__name = name
        self.__parent.addItem(self)
        self.__button = Button(parent.nucleo, text=self.__name, command=command)
        self.__button.grid(row=row, column=col)

    # region Funciones
    @property
    def parent(self):
        return self.__parent

    @property
    def name(self):
        return self.__name

    @property
    def nucleo(self):
        return self.__button

    # endregion


class GeneralCombox:
    __parent: GeneralDivTab
    __name: str
    __box: Combobox

    def __init__(self, name: str, parent: GeneralDivTab, row: int, col: int, values: list):
        self.__parent = parent
        self.__name = name
        self.__parent.addItem(self)
        self.__box = Combobox(self.parent.nucleo, values=values)
        self.__box.grid(row=row, column=col)
        self.__box.current(0)

    # region Funciones
    @property
    def parent(self):
        return self.__parent

    @property
    def name(self):
        return self.__name

    @property
    def nucleo(self):
        return self.__box

    def getCurrent(self):
        return self.__box.current()

    def getCurrentText(self):
        return self.__box.get()

    # endregion


class GeneralCheckBox:
    __parent: GeneralDivTab
    __name: str
    __box: Checkbutton
    __variable: IntVar

    def __init__(self, name: str, parent: GeneralDivTab, row: int, col: int):
        self.__parent = parent
        self.__name = name
        self.__parent.addItem(self)
        self.__variable = IntVar()
        self.__box = Checkbutton(self.__parent.nucleo, text=name, variable=self.__variable, onvalue=1, offvalue=0)
        self.__box.grid(row=row, column=col)

    # region Funciones
    @property
    def parent(self):
        return self.__parent

    @property
    def name(self):
        return self.__name

    @property
    def nucleo(self):
        return self.__box

    def var(self):
        return self.__variable

    # endregion


# endregion
# region Menu
class GeneralMenuBar:
    __parent: GeneralVentana
    __name: str
    __menu_list: list
    __menubar: Menu

    def __init__(self, name: str, parent: GeneralVentana):
        self.__parent = parent
        self.__name = name
        self.__menu_list = []
        self.__parent.setMenuBar(self)
        self.__menubar = Menu(self.__parent.nucleo)
        self.__parent.nucleo.config(menu=self.__menubar)

    def addMenu(self, menu):
        if type(menu) == GeneralMenu:
            self.__menu_list.append(menu)

    @property
    def nucleo(self):
        return self.__menubar


class GeneralMenu:
    __parent: GeneralMenuBar
    __name: str
    __menu: Menu

    def __init__(self, name: str, parent: GeneralMenuBar):
        self.__parent = parent
        self.__name = name
        self.__parent.addMenu(self)
        self.__menu = Menu(self.__parent.nucleo, tearoff=0)
        self.__parent.nucleo.add_cascade(label=self.__name, menu=self.__menu)

    @property
    def nucleo(self):
        return self.__menu


# endregion


"""v = GeneralVentana("Ventana1")
v.ventana.geometry("800x400")
g = GeneralNotebook("Notebook", v)
t = GeneralTab("Tab1", g)
t2 = GeneralTab("Tab1", g)
b = GeneralButtonTab("Butt", t)
b2 = GeneralButtonTab("Butt2", t)
b3 = GeneralButtonTab("Butt", t2)
b4 = GeneralButtonTab("Butt2", t2)

v.ventana.mainloop()"""
