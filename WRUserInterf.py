"""Biblioteca de criacao da interface do usuario"""
import wx.adv
import wx
import os

def InitLocale(self):
    """
    Try to ensure that the C and Python locale is in sync with the wxWidgets
    locale on Windows. If you have troubles from the default behavior of this
    method you can override it in a derived class to behave differently.
    Please report the problem you encountered.
    """
    self.ResetLocale()
    #if 'wxMSW' in PlatformInfo:
    import locale
    try:
        lang, enc = locale.getdefaultlocale()
        self._initial_locale = wx.Locale(lang, lang[:2], lang)
        #print(lang, enc)
        #print(locale.locale_alias)
        locale.setlocale(locale.LC_ALL, 'portuguese_brazil')  #pulo do gato
        #print(locale.getlocale())
    except (ValueError, locale.Error) as ex:
        target = wx.LogStderr()
        orig = wx.Log.SetActiveTarget(target)
        wx.LogError("Unable to set default locale: '{}'".format(ex))
        wx.Log.SetActiveTarget(orig)


wx.App.InitLocale = InitLocale   #substituindo metodo que estava gerando erro por um metodo vazio

class TaskBarIcon(wx.adv.TaskBarIcon):
    """Criacao de um icone na bandeja do systema para controle do aplicativo, e existencia minimizada"""
    def __init__(self, frame, prog_name, prog_name2):
        self.frame = frame   
        super(TaskBarIcon, self).__init__()

        ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
        task_icon = os.path.join(ROOT_DIR, 'task_icon.png')          
        self.TRAY_TOOLTIP = prog_name + prog_name2
        self.SetIcon(wx.Icon(task_icon), self.TRAY_TOOLTIP)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def create_menu_item(self, menu, label, func):
            item = wx.MenuItem(menu, -1, label)
            menu.Bind(wx.EVT_MENU, func, id=item.GetId())
            menu.Append(item)
            return item

    def CreatePopupMenu(self):
        menu = wx.Menu()
        self.create_menu_item(menu, 'Exibir aplicação', self.on_left_down)
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Fechar a aplicação', self.on_exit)
        self.create_menu_item(menu, 'Sobre', self.on_get_info)
        return menu

    def on_left_down(self, event):      
        frame.Show()
        
    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

    def on_get_info(self, event):
        wx.MessageBox("Feito por Cristian Ritter para NSC TV FLOPS", 'Sobre o aplicativo')
      

class MyFrame(wx.Frame):
    def __init__(self, prog_name, prog_name2):
        """font family can be:
        wx.DECORATIVE, wx.DEFAULT,wx.MODERN, wx.ROMAN, wx.SCRIPT or wx.SWISS.

        style can be:
        wx.NORMAL, wx.SLANT or wx.ITALIC.

        weight can be:
        wx.NORMAL, wx.LIGHT, or wx.BOLD
        
        sizer flags applies to aplied borders TOP BOTTOM LEFT RIGHT ALL 
        """
        
        tittle_font = wx.Font(19, wx.DECORATIVE, wx.NORMAL, wx.BOLD)


        super().__init__( # cria uma janela
            parent=None, 
            title=f"{prog_name} - {prog_name2}", 
            #style=wx.CAPTION,  #remove o botão de maximizar, minimizar ou fechar a janela
            size=(1200, 660)
        ) 
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
        texto01b1 = wx.StaticText(panel, label='Log de eventos do sistema de referência', style=wx.ALIGN_CENTER, size=(500,33))
        self.logpanel_master = wx.TextCtrl(panel, value='Carregando informações...', style=wx.TE_MULTILINE | wx.TE_READONLY, size=(500,400))  #cria um edit
        self.logpanel_master.SetBackgroundColour(wx.Colour(190,190,170))
        texto01b2 = wx.StaticText(panel, label='Log de eventos do sistema monitorado', style=wx.ALIGN_CENTER, size=(500,33))
        self.logpanel_slave = wx.TextCtrl(panel, value='Carregando informações...', style=wx.TE_MULTILINE | wx.TE_READONLY, size=(500,400))  #cria um edit
        self.logpanel_slave.SetBackgroundColour(wx.Colour(190,190,170))
        coluna01a = wx.BoxSizer(wx.VERTICAL)
        coluna01b = wx.BoxSizer(wx.VERTICAL)   
        coluna01a.Add(self.logpanel_master, proportion=0, flag=wx.ALL, border=5)
        coluna01a.Add(texto01b1, proportion=0, flag=wx.ALL, border=5)        
        coluna01b.Add(self.logpanel_slave, proportion=0, flag=wx.ALL, border=5)
        coluna01b.Add(texto01b2, proportion=0, flag=wx.ALL, border=5)        
        box_linha01b.Add(coluna01a, proportion=0, flag=wx.ALL, border=5)
        box_linha01b.Add(coluna01b, proportion=0, flag=wx.ALL, border=5)

        box_linha02 = wx.BoxSizer(wx.HORIZONTAL)
        self.led1 =  wx.StaticText(panel, wx.ID_ANY, label='', size=(20,15))
        self.led1.SetBackgroundColour('gray')
        box_linha02.Add(self.led1, proportion=0, flag=wx.ALL, border=10)
        box_linha02.Add(wx.StaticText(panel, label='Status de problemas'), proportion=0, flag=wx.ALL, border=10)

        esconder_bt = wx.Button(panel, label='Esconder')  #cria botao de Esconder janela
                  
        coluna.Add(box_linha01, proportion=0, flag=wx.ALL | wx.CENTER, border=0)                      # adiciona itens à coluna
        coluna.Add(box_linha01b, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
        coluna.AddSpacer(20) 
        coluna.Add(box_linha02, proportion=0, flag=wx.CENTER, border=0) 
        coluna.Add(esconder_bt, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        
        panel.SetSizer(coluna)
        
        texto011.SetFont(tittle_font)
        self.Show()
        
        esconder_bt.Bind(wx.EVT_BUTTON, self.on_press)  #associa funcao ao botao

    def on_press(self, event):
        self.Hide()
    def set_error_led(self):
        self.led1.SetBackgroundColour('Red')
        self.Refresh()
    def clear_error_led(self):
        self.led1.SetBackgroundColour('Gray')
        self.Refresh()

    def carrega_informacoes(self, informacoes, descricao='master'):
        """_frame recebe a janela do aplicativo; informações recebe a string com o texto do painel"""
        if descricao == 'master':
            painel = self.logpanel_master
        elif descricao == 'slave':
            painel = self.logpanel_slave
        else:
            raise(NameError, 'parametro incorreto')

        if (not informacoes in painel.Value):
            painel.Value=informacoes

    def informa_erro(self, estado):
        """recebe o estado de erros  """
        if (estado == True):
            self.set_error_led()
        else:
            self.clear_error_led()
    

if __name__ == '__main__':
    app = wx.App(useBestVisual=True)
    frame = MyFrame("WR LogWatcher", "ATL_JOI")  #criacao do frame recebe o nome da janela
    frame.carrega_informacoes('teste')
    frame.informa_erro(True)
    TaskBarIcon(frame, "WR LogWatcher", "ATL_JOI")
    app.MainLoop()
