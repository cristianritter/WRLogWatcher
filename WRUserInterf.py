"""Biblioteca de criacao da interface do usuario"""
import wx.adv
import wx
import os
import locale
import time

def InitLocale(self):
    """
    Substituição do método padrão devido a problemas relacionados a detecção de locale no Windows 7.
    Não foi testado no windows 10.
    """
    self.ResetLocale()
    try:
        lang, enc = locale.getdefaultlocale()
        self._initial_locale = wx.Locale(lang, lang[:2], lang)
        locale.setlocale(locale.LC_ALL, 'portuguese_brazil')  #pulo do gato
    except (ValueError, locale.Error) as ex:
        target = wx.LogStderr()
        orig = wx.Log.SetActiveTarget(target)
        wx.LogError("Unable to set default locale: '{}'".format(ex))
        wx.Log.SetActiveTarget(orig)
wx.App.InitLocale = InitLocale   #substituindo metodo que estava gerando erro por um metodo vazio

      
class MyFrame(wx.Frame):
    def __init__(self, prog_name):
        """
        Criacao dos frames, define o layout de todos os componentes e as variaveis utilizadas

        font family can be:
        wx.DECORATIVE, wx.DEFAULT,wx.MODERN, wx.ROMAN, wx.SCRIPT or wx.SWISS.

        style can be:
        wx.NORMAL, wx.SLANT or wx.ITALIC.

        weight can be:
        wx.NORMAL, wx.LIGHT, or wx.BOLD
        
        sizer flags applies to aplied borders TOP BOTTOM LEFT RIGHT ALL 
        """
        tittle_font = wx.Font(19, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        warning_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)

        super().__init__( # cria uma janela
            parent=None, 
            title=prog_name, 
            style=wx.CAPTION | wx.FRAME_TOOL_WINDOW,  #remove o botão de maximizar, minimizar ou fechar a janela
            size=(1200, 690)
        ) 
        #ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
        #task_icon = os.path.join(ROOT_DIR, 'task_icon.png')
        #self.SetIcon(wx.Icon(task_icon))

        self.Centre()    #centraliza a janela  
        
        panel = wx.Panel(self) #cria um painel dentro da janela

        coluna = wx.BoxSizer(wx.VERTICAL) #cria uma coluna dentro do painel

        """Criação dos itens da janela"""
        box_linha01 = wx.BoxSizer(wx.HORIZONTAL) #cria uma linha 
        texto011 = wx.StaticText(panel, label=prog_name, style=wx.ALIGN_CENTER, size=(600,33))
        texto011.SetBackgroundColour('black')
        texto011.SetForegroundColour('white')
        box_linha01.Add(texto011, proportion=0, flag=wx.TOP, border=10)   #adiciona elemento de texto na linha01 
      
        box_linha01b = wx.BoxSizer(wx.HORIZONTAL)  
        texto01b1 = wx.StaticText(panel, label='Log de eventos do sistema de referência', style=wx.ALIGN_CENTER, size=(500,15))
        self.texto01b1b = wx.StaticText(panel, label="Sem informações de caminho de arquivo", style=wx.ALIGN_CENTER, size=(500,15))
        self.logpanel_master = wx.TextCtrl(panel, value='Carregando informações...', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, size=(500,400))  #cria um edit
        self.logpanel_master.SetBackgroundColour(wx.Colour(190,190,170))
        texto01b2 = wx.StaticText(panel, label='Log de eventos do sistema monitorado', style=wx.ALIGN_CENTER, size=(500,15))
        self.texto01b2b = wx.StaticText(panel, label="Sem informações de caminho de arquivo", style=wx.ALIGN_CENTER, size=(500,15))
        self.logpanel_slave = wx.TextCtrl(panel, value='Carregando informações...', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, size=(500,400))  #cria um edit
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
        self.listbox1 = wx.ListBox(panel, choices=["SAT POA", "SAT REG", "BARIX", "LINK DOWN"])
        self.listbox1.Disable()
        box_linha02.Add(wx.StaticText(panel, label='Modo de operação detectado:'), proportion=0, flag=wx.CENTER | wx.ALL, border=20)
        box_linha02.Add(self.listbox1, proportion=0, flag=wx.CENTER | wx.ALL, border=20)
        
        self.led1 =  wx.StaticText(panel, wx.ID_ANY, label='', size=(20,10))
        self.led1.SetBackgroundColour('gray')
        box_linha02a = wx.BoxSizer(wx.HORIZONTAL)
        box_linha02a.Add(self.led1, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        box_linha02a.Add(wx.StaticText(panel, label='Posição da botoneira   '), proportion=0, flag=wx.ALL | wx.CENTER, border=5)
       
        self.led2 =  wx.StaticText(panel, wx.ID_ANY, label='', size=(20,10))
        self.led2.SetBackgroundColour('gray')
        box_linha02b = wx.BoxSizer(wx.HORIZONTAL)
        box_linha02b.Add(self.led2, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        box_linha02b.Add(wx.StaticText(panel, label='Falha no historico de interpretação dos comandos'), proportion=0, flag=wx.ALL | wx.CENTER, border=5)
       

        box_coluna02a = wx.BoxSizer(wx.VERTICAL)
        box_coluna02a.Add(box_linha02a, proportion=0, flag=wx.ALL, border=0)
        box_coluna02a.Add(box_linha02b, proportion=0, flag=wx.ALL, border=0)

        box_linha02.Add(box_coluna02a, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
        
        esconder_bt = wx.Button(panel, label='Esconder')  #cria botao de Esconder janela
        self.texto02a = wx.StaticText(panel, label='Verifique a sincronização de horário dos sistemas de referência e/ou monitorados.')
        self.texto02a.Font = warning_font
        self.texto02a.BackgroundColour = 'red'
                   
        coluna.Add(box_linha01, proportion=0, flag=wx.ALL | wx.CENTER, border=0)                      # adiciona itens à coluna
        coluna.Add(box_linha01b, proportion=0, flag=wx.ALL | wx.CENTER, border=0)
        coluna.Add(box_linha02, proportion=0, flag=wx.CENTER | wx.ALL, border=0)
        coluna.Add(self.texto02a, proportion=0, flag=wx.CENTER |wx.CENTER, border=0) 
        coluna.Add(esconder_bt, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        
        panel.SetSizer(coluna)
        
        texto011.SetFont(tittle_font)
        self.Show()
        
        esconder_bt.Bind(wx.EVT_BUTTON, self.on_press)  #associa funcao ao botao

    def on_press(self, event):
        """Funcao executada ao pressionar o botao Esconder"""
        self.Hide()

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


   # def informa_erro(self, estado):
        """
        Função que informa o status de erros do sistema.\n
        Recebe um booleano contendo True se existem erros, e False se nao existem.
        """
   #     if (estado == True):
   #         self.set_error_led()
   #     else:
   #         self.clear_error_led()
    

class TaskBarIcon(wx.adv.TaskBarIcon):
    """
    Criacao de um icone na bandeja do systema para controle do aplicativo, e existencia no tray do sistema
    """
    def __init__(self, prog_name, frame_names, list_of_frames):
        """
        Funcao que inicializa o tray do sistema \n
        prog_name recebe uma string com o nome do programa a ser apresentado no icone tray\n
        frame_names recebe um dicionario no estilo chave :key {profile_name :apelido_praca}\n
        list_of_frames recebe um dicionario no estilo chave :key {profile_name :instancia de inicializacao do frame}\n
        
        """
        self.frame = (list(list_of_frames.values())[0])
        self.FRAME_NAMES = frame_names
        self.LIST_OF_FRAMES = list_of_frames
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
        for item in self.FRAME_NAMES:
            # definindo metodos para cada submenu criado, funcao lambda permite enviar parametros especificos para cada submenu
            self.create_menu_item(menu, f'View {self.FRAME_NAMES[item]}', lambda evt, temp=self.LIST_OF_FRAMES[item]: self.on_right_down(evt, temp)) 
        
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Fechar a aplicação', self.on_exit) #on exit program clique
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Sobre', self.on_get_info) #apresentacao de informacoes sobre o desenvolvedor
        return menu

    def on_left_down(self, event): 
        """
        Metodo executado ao clicar com o botao esquerdo
        """
        pass

    def on_right_down(self, event, button_label):
        """
        Metodo executado ao clicar com o botao direito em submenus\n
        button_label recebe o frame especifico de casa submenu
        a funcao frame.Show() realiza a exibicao da janela especificada 
        """
        button_label.Show()
      
    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        for item in self.LIST_OF_FRAMES:
            self.LIST_OF_FRAMES[item].Close();

    def on_get_info(self, event):
        wx.MessageBox("Feito por Cristian Ritter para NSC TV", 'Sobre o aplicativo')


if __name__ == '__main__':
    """
    Este trecho do código permite testar a biblioteca individualmente e fornece também exemplos de uso.
    """
    app = wx.App(useBestVisual=True)

    frame = MyFrame("WR LogWatcher")  #criacao do frame recebe o nome da janela
    
    frame.adiciona_informacoes('teste', estilo_do_texto='FLAG', selecao='master')
    frame.adiciona_informacoes('teste2', estilo_do_texto='NENHUM', selecao='slave')
    #print()
#    frame.logpanel_master.

    frame_names = {'nome_do_perfil' : 'apelido'}
    frames_dict = {'nome_do_perfil' :frame}

    TaskBarIcon("WR LogWatcher - ATL_JOI", frame_names, frames_dict)
    app.MainLoop()
