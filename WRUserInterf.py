from wx.core import CENTER
import parse_config
import wx.adv
import wx
import os

configuration = parse_config.ConfPacket()
configs = configuration.load_config('default')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
TRAY_TOOLTIP = 'WRLogWatcher - ' + configs['default']['nome_praca']
task_icon = os.path.join(ROOT_DIR, 'task_icon.png')

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(task_icon)
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
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):      
        frame.Show()
        
    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()


class MyFrame(wx.Frame):    
    def __init__(self, prog_name):
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
            title=f"{prog_name} - {configs['default']['nome_praca']}", 
            #style=wx.CAPTION,  #remove o botão de maximizar, minimizar ou fechar a janela
            size=(600, 600)
        ) 
        
        self.Centre()    #centraliza a janela  
        
        panel = wx.Panel(self) #cria um painel dentro da janela

        coluna = wx.BoxSizer(wx.VERTICAL) #cria uma coluna dentro do painel

        """Criação dos itens da janela"""
        box_linha01 = wx.BoxSizer(wx.HORIZONTAL) #cria uma linha 
        texto01 = wx.StaticText(panel, label=prog_name, style=wx.ALIGN_CENTER, size=(600,33))
        texto01.SetBackgroundColour('black')
        texto01.SetForegroundColour('white')
        box_linha01.Add(texto01, proportion=0, flag=wx.ALL, border=5)   #adiciona elemento de texto na linha01 
         
        self.logpanel = wx.TextCtrl(panel, value='Carregando informações...', style=wx.TE_MULTILINE | wx.TE_READONLY, size=(1,400))  #cria um edit
        self.logpanel.SetBackgroundColour(wx.Colour(190,190,170))
        
        box_linha02 = wx.BoxSizer(wx.HORIZONTAL)
        self.led1 =  wx.StaticText(panel, wx.ID_ANY, label='', size=(20,15))
        self.led1.SetBackgroundColour('gray')
        box_linha02.Add(self.led1, proportion=0, flag=wx.ALL, border=10)
        box_linha02.Add(wx.StaticText(panel, label='Status de problemas'), proportion=0, flag=wx.ALL, border=10)

        esconder_bt = wx.Button(panel, label='Esconder')  #cria botao de Esconder janela
                  
        coluna.Add(box_linha01, proportion=0, flag=wx.ALL | wx.CENTER, border=0)                      # adiciona itens à coluna
        coluna.Add(self.logpanel, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
        coluna.AddSpacer(20) 
        coluna.Add(box_linha02, proportion=0, flag=wx.CENTER, border=0) 
        coluna.Add(esconder_bt, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        
        panel.SetSizer(coluna)
        
        texto01.SetFont(tittle_font)
        self.Show()
        
        esconder_bt.Bind(wx.EVT_BUTTON, self.on_press)  #associa funcao ao botao

    def on_press(self, event):
        frame.Hide()
    def set_error_led(self):
        frame.led1.SetBackgroundColour('Red')
        frame.Refresh()
    def clear_error_led(self):
        frame.led1.SetBackgroundColour('Gray')
        frame.Refresh()

def carrega_informacoes(_frame, informacoes):
    """_frame recebe a janela do aplicativo; informações recebe a string com o texto do painel"""
    _frame.logpanel.Value=informacoes

def informa_erro(_frame):
    """_frame recebe a janela do aplicativo  """
    _frame.set_error_led()
    

def informa_ok(_frame):
    """_frame recebe a janela do aplicativo  """
    frame.clear_error_led()
    

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame("WR LogWatcher")  #criacao do frame recebe o nome da janela
    carrega_informacoes(frame, 'teste')
    informa_erro(frame)
    frame.SetIcon(wx.Icon(task_icon))
    TaskBarIcon(frame)
    app.MainLoop()
