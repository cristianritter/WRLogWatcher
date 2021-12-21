"""Biblioteca de criacao da interface do usuario"""
from sys import path
import wx.adv
import wx
import os
import locale
#import time

from wx.core import Panel

def InitLocale(self):
    """
    Substituição do método padrão devido a problemas relacionados a detecção de locale no Windows 7.
    Não foi testado no windows 10.
    """
    self.ResetLocale()
    try:
        lang, _ = locale.getdefaultlocale()
        self._initial_locale = wx.Locale(lang, lang[:2], lang)
        locale.setlocale(locale.LC_ALL, 'portuguese_brazil')  #pulo do gato
    except (ValueError, locale.Error) as ex:
        target = wx.LogStderr()
        orig = wx.Log.SetActiveTarget(target)
        wx.LogError("Unable to set default locale: '{}'".format(ex))
        wx.Log.SetActiveTarget(orig)
wx.App.InitLocale = InitLocale   #substituindo metodo que estava gerando erro por um metodo vazio
      
class TabPanel(wx.Panel):
    def __init__(self, parent):
        """
        """
        warning_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)

        super().__init__(parent=parent) 
       
        coluna = wx.BoxSizer(wx.VERTICAL) #cria uma coluna dentro do painel

        """Criação dos itens da janela"""
        box_linha01 = wx.BoxSizer(wx.HORIZONTAL) #cria uma linha 
    
        box_linha01b = wx.BoxSizer(wx.HORIZONTAL)  
        texto01b1 = wx.StaticText(self, label='Log de eventos do sistema de referência', style=wx.ALIGN_CENTER, size=(500,15))
        self.texto01b1b = wx.StaticText(self, label="Sem informações de caminho de arquivo", style=wx.ALIGN_CENTER, size=(500,15))
        self.logpanel_master = wx.TextCtrl(self, value='Carregando informações...', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, size=(500,400))  #cria um edit
        self.logpanel_master.SetBackgroundColour(wx.Colour(190,190,170))
        texto01b2 = wx.StaticText(self, label='Log de eventos do sistema monitorado', style=wx.ALIGN_CENTER, size=(500,15))
        self.texto01b2b = wx.StaticText(self, label="Sem informações de caminho de arquivo", style=wx.ALIGN_CENTER, size=(500,15))
        self.logpanel_slave = wx.TextCtrl(self, value='Carregando informações...', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, size=(500,400))  #cria um edit
        self.logpanel_slave.SetBackgroundColour(wx.Colour(190,190,170))
        coluna01a = wx.BoxSizer(wx.VERTICAL)
        coluna01b = wx.BoxSizer(wx.VERTICAL)   
        coluna01a.Add(self.logpanel_master, proportion=0, flag=wx.ALL, border=5)
        coluna01a.Add(texto01b1, proportion=0, flag=wx.ALL, border=5)        
        coluna01a.Add(self.texto01b1b, proportion=0, flag=wx.ALL, border=5)        
        coluna01b.Add(self.logpanel_slave, proportion=0, flag=wx.ALL, border=5)
        coluna01b.Add(texto01b2, proportion=0, flag=wx.ALL, border=5)        
        coluna01b.Add(self.texto01b2b, proportion=0, flag=wx.ALL, border=5)        
        box_linha01b.Add(coluna01a, proportion=0, flag=wx.ALL, border=5)
        box_linha01b.Add(coluna01b, proportion=0, flag=wx.ALL, border=5)

        box_linha02 = wx.BoxSizer(wx.HORIZONTAL)
        self.listbox1 = wx.ListBox(self, choices=["SAT POA", "SAT REG", "BARIX", "LINK DOWN"])
        self.listbox1.Disable()
        box_linha02.Add(wx.StaticText(self, label='Modo de operação detectado:'), proportion=0, flag=wx.CENTER | wx.ALL, border=20)
        box_linha02.Add(self.listbox1, proportion=0, flag=wx.CENTER | wx.ALL, border=20)
        
        self.led1 =  wx.StaticText(self, wx.ID_ANY, label='', size=(20,10))
        self.led1.SetBackgroundColour('gray')
        box_linha02a = wx.BoxSizer(wx.HORIZONTAL)
        box_linha02a.Add(self.led1, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        box_linha02a.Add(wx.StaticText(self, label='Posição da botoneira'), proportion=0, flag=wx.ALL | wx.CENTER, border=5)
       
        self.led2 =  wx.StaticText(self, wx.ID_ANY, label='', size=(20,10))
        self.led2.SetBackgroundColour('gray')
        box_linha02b = wx.BoxSizer(wx.HORIZONTAL)
        box_linha02b.Add(self.led2, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        box_linha02b.Add(wx.StaticText(self, label='Historico de interpretação dos comandos'), proportion=0, flag=wx.ALL | wx.CENTER, border=5)
       

        box_coluna02a = wx.BoxSizer(wx.VERTICAL)
        box_coluna02a.Add(box_linha02a, proportion=0, flag=wx.ALL, border=0)
        box_coluna02a.Add(box_linha02b, proportion=0, flag=wx.ALL, border=0)
        
        box_linha02.AddSpacer(50)
        box_linha02.Add(box_coluna02a, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
        
        self.texto02a = wx.StaticText(self, label='Verifique a sincronização de horário dos sistemas de referência e/ou monitorados.')
        self.texto02a.Font = warning_font
        self.texto02a.BackgroundColour = 'red'
                   
        coluna.Add(box_linha01, proportion=0, flag=wx.ALL | wx.CENTER, border=0)                      # adiciona itens à coluna
        coluna.Add(box_linha01b, proportion=0, flag=wx.ALL | wx.CENTER, border=0)
        coluna.Add(box_linha02, proportion=0, flag=wx.CENTER | wx.ALL, border=0)
        coluna.Add(self.texto02a, proportion=0, flag=wx.CENTER |wx.CENTER, border=0) 
        
        self.SetSizer(coluna)
        self.Show()
    
    def set_error_led(self, selecao='led1'):
        """Funcao que pinta o led de vermelho"""
        if selecao.lower() == 'led1':
            self.led1.SetBackgroundColour('Red')
        if selecao.lower() == 'led2':
            self.led2.SetBackgroundColour('Red')    
        self.Refresh()

    def clear_error_led(self, selecao='led1'):
        """Funcao que pinta o led de verde"""
        if selecao.lower() == 'led1':
            self.led1.SetBackgroundColour('Green')
        if selecao.lower() == 'led2':
            self.led2.SetBackgroundColour('Green')
        self.Refresh()

    def set_interface_paths(self, paths):
        """
        Funcao que seta o texto da interface que indica os paths monitorados
        Recebe uma lista no estilo [path master, path slave]
        """
        self.texto01b1b.SetLabel(paths[0])
        self.texto01b2b.SetLabel(paths[1])

    def set_listbox_selected(self, mode):
        """
        Funcao que seleciona uma opcao no listbox dos modos de operacao\n
        Recebe uma string com o nome do modo de servico. Suporta as opcoes listadas no listbox\n
        SAT POA, SAT REG, BARIX, LINK DOWN
        """
        for idx, content in enumerate(self.listbox1.GetItems()):
            if mode in content:
                self.listbox1.Select(idx)

    def adiciona_informacoes(self, conteudo, estilo_do_texto, selecao='master'):
        """Funcao que atualiza o painel de informacoes do log. \n
        Recebe uma string contendo o conteudo do log\n
        a selecao suporta as opcoes 'master' ou 'slave' para escolher o destino das informacoes.
        """
        if selecao == 'master':
            painel = self.logpanel_master    
        
        elif selecao == 'slave':
            painel = self.logpanel_slave

        else:
            raise(NameError, 'parametro incorreto em adiciona informacoes')
          
        if (not conteudo in painel.Value):
            if estilo_do_texto == 'FLAG':
                painel.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.WHITE))
            elif estilo_do_texto == 'ERROR':
                painel.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.RED))
            else:
                painel.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.LIGHT_GREY))
            painel.AppendText(conteudo)
        #self.Refresh()
    
    def clear_content(self):
            self.logpanel_master.Clear()  
            self.logpanel_slave.Clear()


class TabView(wx.Panel):
    def __init__(self, parent, names, lista_paths, flag):
        """
        """
        warning_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)

        super().__init__(parent=parent) 
        self.FLAG = flag
        coluna = wx.BoxSizer(wx.VERTICAL) #cria uma coluna dentro do painel
        self.lista_paths = lista_paths
        self.names = names
        """Criação dos itens da janela"""
        box_linha01 = wx.BoxSizer(wx.HORIZONTAL) #cria uma linha 
    
        box_linha01b = wx.BoxSizer(wx.HORIZONTAL)  
        texto01b1 = wx.StaticText(self, label='Log de eventos', style=wx.ALIGN_CENTER, size=(500,15))
        self.texto01b1b = wx.StaticText(self, label="Selecione a praça para agilizar a busca do arquivo", style=wx.ALIGN_CENTER, size=(500,15))
        self.logpanel_master = wx.TextCtrl(self, value='Sem informações para exibir', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, size=(500,400))  #cria um edit
        self.logpanel_master.SetBackgroundColour(wx.Colour(190,190,170))
        texto01b2 = wx.StaticText(self, label='Log de eventos', style=wx.ALIGN_CENTER, size=(500,15))
        self.texto01b2b = wx.StaticText(self, label="Selecione a praça para agilizar a busca do arquivo", style=wx.ALIGN_CENTER, size=(500,15))
        self.logpanel_slave = wx.TextCtrl(self, value='Sem informações para exibir', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, size=(500,400))  #cria um edit
        self.logpanel_slave.SetBackgroundColour(wx.Colour(190,190,170))
        list_choices = list(names.values())
        list_choices.append('CABEÇA de REDE')
        self.listbox1 = wx.ListBox(self, choices=list_choices)
        self.filepick01 = wx.FilePickerCtrl(self, path="",
               message="Selecione o arquivo de log", size=(390,25), style=wx.FLP_USE_TEXTCTRL)
        self.listbox2 = wx.ListBox(self, choices=list_choices)
        self.filepick02 = wx.FilePickerCtrl(self, path="",
               message="Selecione o arquivo de log", size=(390,25), style=wx.FLP_USE_TEXTCTRL)
        
        coluna01a = wx.BoxSizer(wx.VERTICAL)
        coluna01b = wx.BoxSizer(wx.VERTICAL)   
        coluna01a.Add(self.logpanel_master, proportion=0, flag=wx.ALL, border=5)
        coluna01a.Add(texto01b1, proportion=0, flag=wx.ALL, border=5)        
        coluna01a.Add(self.texto01b1b, proportion=0, flag=wx.ALL, border=5)        
        coluna01a.Add(self.listbox1, proportion=0, flag=wx.ALL | wx.CENTER, border=5)        
        coluna01a.Add(self.filepick01, proportion=0, flag=wx.ALL | wx.CENTER, border=5)

        coluna01b.Add(self.logpanel_slave, proportion=0, flag=wx.ALL, border=5)
        coluna01b.Add(texto01b2, proportion=0, flag=wx.ALL, border=5)        
        coluna01b.Add(self.texto01b2b, proportion=0, flag=wx.ALL, border=5)        
        coluna01b.Add(self.listbox2, proportion=0, flag=wx.ALL | wx.CENTER, border=5)        
        coluna01b.Add(self.filepick02, proportion=0, flag=wx.ALL | wx.CENTER, border=5)

        box_linha01b.Add(coluna01a, proportion=0, flag=wx.ALL, border=5)
        box_linha01b.Add(coluna01b, proportion=0, flag=wx.ALL, border=5)

        box_linha02 = wx.BoxSizer(wx.HORIZONTAL)
                   
        coluna.Add(box_linha01, proportion=0, flag=wx.ALL | wx.CENTER, border=0)                      # adiciona itens à coluna
        coluna.Add(box_linha01b, proportion=0, flag=wx.ALL | wx.CENTER, border=0)
        coluna.Add(box_linha02, proportion=0, flag=wx.CENTER | wx.ALL, border=0)
        
        self.listbox1.Bind(wx.EVT_LISTBOX, lambda event: self.on_select(event, 'listbox1'))  #associa funcao ao botao
        self.listbox2.Bind(wx.EVT_LISTBOX, lambda event: self.on_select(event, 'listbox2'))  #associa funcao ao botao
        self.filepick01.Bind(wx.EVT_FILEPICKER_CHANGED, lambda event: self.on_open(event, 'filepick01'))  #associa funcao ao botao
        self.filepick02.Bind(wx.EVT_FILEPICKER_CHANGED, lambda event: self.on_open(event, 'filepick02'))  #associa funcao ao botao
        self.SetSizer(coluna)
        self.Show()
    
    def on_select(self, event, selecao):
        if selecao == 'listbox1':
            listbox = self.listbox1
            filepick = self.filepick01

        elif selecao == 'listbox2':
            listbox = self.listbox2
            filepick = self.filepick02
        
        text = listbox.GetStringSelection()
        for item in self.names:
            if (self.names[item] == text):
                filepick.Path = os.path.join(self.lista_paths[item].split(', ')[1], '') 
                break
            else:
                filepick.Path = os.path.join(self.lista_paths[item].split(',')[0], '') #se nao for nenhuma anterior entao é cabeça de rede

    def on_open(self, event, selecao):
        if (selecao == 'filepick01'):    
            filepick = self.filepick01
            self.texto01b1b.SetLabel(filepick.Path)
            self.logpanel_master.Clear()  
            self.adiciona_informacoes(filepick.Path, 'filepick01')
 
        elif (selecao == 'filepick02'):
            filepick = self.filepick02
            self.texto01b2b.SetLabel(filepick.Path)
            self.logpanel_slave.Clear()  
            self.adiciona_informacoes(filepick.Path, 'filepick02')
 
        

    def adiciona_informacoes(self, arquivo_de_log, selecao='filepick01'):
        """Funcao que atualiza o painel de informacoes do log. \n
        Recebe uma string contendo o conteudo do log\n
        a selecao suporta as opcoes 'master' ou 'slave' para escolher o destino das informacoes.
        """
        if selecao == 'filepick01':
            painel = self.logpanel_master    
        
        elif selecao == 'filepick02':
            painel = self.logpanel_slave

        else:
            raise(NameError, 'parametro incorreto em adiciona informacoes')

        with open(arquivo_de_log, mode='r', encoding='utf-8', errors='ignore') as frb:  #le o arquivo em ordem inversa pois os valores atuais estao nas ultimas linhas
            for idx, linha in enumerate((frb.readlines())):  #reversed removed
                if (self.FLAG in linha):
                    painel.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.WHITE))
                elif ('Error' in linha or 'filtrado' in linha or 'Set' in linha):
                    painel.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.RED))
                else:
                    painel.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.LIGHT_GREY))
          
                painel.AppendText(f'{idx} - {linha}')                
    def clear_content(self):
        self.logpanel_master.SetLabel('Sem informações para exibir')  
        self.logpanel_slave.SetLabel('Sem informações para exibir')
        self.filepick01.SetPath("")
        self.filepick02.SetPath("")
        



class TaskBarIcon(wx.adv.TaskBarIcon):
    """
    Criacao de um icone na bandeja do systema para controle do aplicativo, e existencia no tray do sistema
    """
    def __init__(self, prog_name, frame, tabs_dict, names):
        """
        Funcao que inicializa o tray do sistema \n  
        """
        self.frame = frame
        self.tabs_dict = tabs_dict
        self.names = names
        super(TaskBarIcon, self).__init__()
        
        self.TRAY_TOOLTIP = prog_name
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
        task_icon = os.path.join(ROOT_DIR, 'task_icon.png')          
        self.SetIcon(wx.Icon(task_icon), self.TRAY_TOOLTIP)

        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down) #funcao que define o metodo de clique esquerdo no trayicon

    def create_menu_item(self, menu, label, func):
            item = wx.MenuItem(menu, -1, label)
            menu.Bind(wx.EVT_MENU, func, id=item.GetId())
            menu.Append(item)
            return item

    def CreatePopupMenu(self):
        menu = wx.Menu()
        for name in self.tabs_dict.keys():
            # definindo metodos para cada submenu criado, funcao lambda permite enviar parametros especificos para cada submenu
            self.create_menu_item(menu, f'View {self.names[name]}', lambda evt, temp=name: self.on_right_down(evt, temp)) 
        
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Fechar a aplicação', self.on_exit) #on exit program clique
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Sobre', self.on_get_info) #apresentacao de informacoes sobre o desenvolvedor
        return menu

    def on_left_down(self, event): 
        """
        Metodo executado ao clicar com o botao esquerdo
        """
        self.frame.Show()
        self.frame.Raise()
        self.frame.notebook.SetSelection(1)  #seleciona a tab selecionada
      
    def on_right_down(self, event, tab):
        """
        Metodo executado ao clicar com o botao direito em submenus\n
        button_label recebe a tab especifica de cada submenu 
        """
        self.frame.Show()
        for idx, name in enumerate(self.names):
            if name == tab:
                self.frame.notebook.SetSelection(idx)  #seleciona a tab selecionada
      
    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

    def on_get_info(self, event):
        wx.MessageBox("Feito por Cristian Ritter para NSC TV", 'Sobre o aplicativo')


class MyFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
    #----------------------------------------------------------------------
    def __init__(self, prog_name, tabs, names, paths, flag):
        """Constructor"""     
        super().__init__(None, style=wx.CAPTION | wx.FRAME_TOOL_WINDOW, 
                          title=prog_name,
                          size=(1050,720)
                          ) 
           
        self.Centre()    #centraliza a janela    
        panel = wx.Panel(self)    
        notebook = wx.Notebook(panel)
        self.tabs = tabs
        self.notebook = notebook
        for nome in names:
            tabs[nome] = TabPanel(notebook)
            notebook.AddPage(tabs[nome], names[nome])
        self.log_analyzer = TabView(notebook, names=names, lista_paths=paths, flag=flag)
        notebook.AddPage(self.log_analyzer, "ANTIGOS")


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, proportion=0, flag=wx.ALL, border=5)
        hide_bt = wx.Button(panel, label='Esconder')  #cria botao de Esconder janela
        sizer.Add(hide_bt, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        hide_bt.Bind(wx.EVT_BUTTON, self.on_press)  #associa funcao ao botao

        panel.SetSizer(sizer)
        self.Layout()     
        self.Show()

    def on_press(self, event):
        """Funcao executada ao pressionar o botao Esconder"""
        self.log_analyzer.clear_content()
        self.Hide()      


if __name__ == '__main__':
    """
    Este trecho do código permite testar a biblioteca individualmente e fornece também exemplos de uso.
    """
    app = wx.App(useBestVisual=True)

    names = {'praca01': 'WINRADIO ATL BLU', 'praca02': 'WINRADIO ATL CHA', 'praca03': 'WINRADIO ATL CRI', 'praca04': 'WINRADIO ATL JOI', 'praca05': 'WINRADIO BKP'}
    paths = {'praca01': 'C:\\, C:\\', 'praca02': 'C:\\, C:\\', 'praca03': 'C:\\, C:\\', 'praca04': 'C:\\, C:\\', 'praca05': 'C:\\, C:\\'}
    tabs_dict = {}
    frame = MyFrame("WR LogWatcher", tabs_dict, names, paths)  #criacao do frame recebe o nome da janela
    
    frame_names = {'nome_do_perfil' : 'apelido'}
    frames_dict = {'nome_do_perfil' :frame}
    TaskBarIcon("WR LogWatcher - ATL_JOI", frame, tabs_dict, names)

    app.MainLoop()
