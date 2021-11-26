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
        self.create_menu_item(menu, 'Abrir log', self.on_left_down)
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Exit', self.on_exit)
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
    def __init__(self):
        tittle_font = wx.Font(24, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        normal_font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        super().__init__( # cria uma janela
            parent=None, 
            title='WRLogWatcher - ' + configs['default']['nome_praca'], 
            style=wx.CAPTION,  #remove o botão de maximizar, minimizar ou fechar a janela
            size=(600, 400)
        ) 
        
        self.Centre()    #centraliza a janela  
        
        panel = wx.Panel(self) #cria um painel dentro da janela

        coluna = wx.BoxSizer(wx.VERTICAL) #cria uma coluna dentro do painel

        """Criação dos itens da janela"""
        linha01 = wx.BoxSizer(wx.HORIZONTAL) #cria uma linha 
        texto01 = wx.StaticText(panel, label='WRLogWatcher')
        linha01.Add(texto01, proportion=0, flag=wx.TOP, border=20)   #adiciona elemento de texto na linha01
         
        self.logpanel = wx.TextCtrl(panel, value='Ainda não existe um log disponível este mês.', style=wx.TE_MULTILINE | wx.TE_READONLY, size=(1,250))  #cria um edit
        
        linha02 = wx.BoxSizer(wx.HORIZONTAL)
        self.led1 =  wx.StaticText(panel, wx.ID_ANY, label='', size=(20,15))
        self.led1.SetBackgroundColour('gray')
        linha02.Add(self.led1, proportion=0, flag=wx.TOP, border=5)
        linha02.Add(wx.StaticText(panel, label='Status de problemas'), proportion=0, flag=wx.TOP, border=5)

        esconder_bt = wx.Button(panel, label='Esconder')  #cria botao de Esconder janela
                  
        coluna.Add(linha01, proportion=0, flag=wx.CENTER, border=0)                      # adiciona itens à coluna
        coluna.Add(self.logpanel, proportion=0, flag=wx.ALL | wx.EXPAND, border=0) 
        coluna.Add(linha02, proportion=0, flag=wx.CENTER, border=0) 
        coluna.Add(esconder_bt, proportion=0, flag=wx.TOP | wx.CENTER, border=0)
        
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

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    #frame.SetIcon(wx.Icon(task_icon))
    #TaskBarIcon(frame)
    app.MainLoop()
