"""Biblioteca de criacao da interface do usuario"""
import wx.adv
import wx
import os
import locale

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
    def __init__(self, parent, tab_text):
        """
        """
        self.tab_text = tab_text
        tittle_font = wx.Font(19, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        warning_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)

        super().__init__(parent=parent) 
       
        coluna = wx.BoxSizer(wx.VERTICAL) #cria uma coluna dentro do painel

        """Criação dos itens da janela"""
        box_linha01 = wx.BoxSizer(wx.HORIZONTAL) #cria uma linha 
        #texto011 = wx.StaticText(self, label=prog_name, style=wx.ALIGN_CENTER, size=(600,33))
        #texto011.SetBackgroundColour('black')
        #texto011.SetForegroundColour('white')
        #box_linha01.Add(texto011, proportion=0, flag=wx.TOP, border=10)   #adiciona elemento de texto na linha01 
      
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
        
        #texto011.SetFont(tittle_font)
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
            raise(NameError, 'parametro incorreto')
          
        if (not conteudo in painel.Value):
            if estilo_do_texto == 'FLAG':
                painel.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.WHITE))
            else:
                painel.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.LIGHT_GREY))
            painel.AppendText(conteudo)
        self.Refresh()

    def limpa_informacoes(self, selecao='master'):
        if selecao == 'master':
            self.logpanel_master.Clear()
        
        elif selecao == 'slave':
            self.logpanel_slave.Clear()

        else:
            raise(NameError, 'parametro incorreto')
    

class TaskBarIcon(wx.adv.TaskBarIcon):
    """
    Criacao de um icone na bandeja do systema para controle do aplicativo, e existencia no tray do sistema
    """
    def __init__(self, prog_name, frame, tabs_dict, names):
        """
        Funcao que inicializa o tray do sistema \n
        prog_name recebe uma string com o nome do programa a ser apresentado no icone tray\n
        frame_names recebe um dicionario no estilo chave :key {profile_name :apelido_praca}\n
        list_of_frames recebe um dicionario no estilo chave :key {profile_name :instancia de inicializacao do frame}\n
        
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
        pass

    def on_right_down(self, event, tab):
        """
        Metodo executado ao clicar com o botao direito em submenus\n
        button_label recebe o frame especifico de casa submenu
        a funcao frame.Show() realiza a exibicao da janela especificada 
        """
        self.frame.Show()
        for idx, name in enumerate(self.names):
            if name == tab:
                self.frame.notebook.SetSelection(idx)
      
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
    def __init__(self, prog_name, tabs, names):
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
            tabs[nome] = TabPanel(notebook, names[nome])
            notebook.AddPage(tabs[nome], tabs[nome].tab_text)

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
        self.Hide()

        


if __name__ == '__main__':
    """
    Este trecho do código permite testar a biblioteca individualmente e fornece também exemplos de uso.
    """
    app = wx.App(useBestVisual=True)

    names = {'praca01': 'WINRADIO ATL BLU', 'praca02': 'WINRADIO ATL CHA', 'praca03': 'WINRADIO ATL CRI', 'praca04': 'WINRADIO ATL JOI', 'praca05': 'WINRADIO BKP'}
    tabs_dict = {}
    frame = MyFrame("WR LogWatcher", tabs_dict, names)  #criacao do frame recebe o nome da janela
    
    #frame.tabs[names[0]].adiciona_informacoes('teste', estilo_do_texto='FLAG', selecao='master')
    #frame.tabs[0].adiciona_informacoes('teste2', estilo_do_texto='NENHUM', selecao='slave')

    frame_names = {'nome_do_perfil' : 'apelido'}
    frames_dict = {'nome_do_perfil' :frame}
    TaskBarIcon("WR LogWatcher - ATL_JOI", frame, tabs_dict, names)

    #TabPanel.SetF

    app.MainLoop()
