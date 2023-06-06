#Boa:Frame:Mainframe

import wx, wx.stc, wx.grid, pickle, wx.richtext, socket, sys, os
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from math import sin,cos
from animacia import animuj

def create(parent):
    return Mainframe(parent)

[wxID_MAINFRAME, wxID_MAINFRAMEADRESA, wxID_MAINFRAMEANIME_BTN, 
 wxID_MAINFRAMECONDT_LBL, wxID_MAINFRAMECONDT_TXTCTRL, 
 wxID_MAINFRAMECONNECT_BTN, wxID_MAINFRAMEDATABAZA, wxID_MAINFRAMEDRAW_BTN, 
 wxID_MAINFRAMEHELP_BTN, wxID_MAINFRAMEKI_CTRL, wxID_MAINFRAMEKP_CTRL, 
 wxID_MAINFRAMELOAD_VARS_BTN, wxID_MAINFRAMEPLOT_BTN, 
 wxID_MAINFRAMERICHTEXTCTRL1, wxID_MAINFRAMESHOW_F, wxID_MAINFRAMESHOW_X1, 
 wxID_MAINFRAMESHOW_X2, wxID_MAINFRAMESHOW_X3, wxID_MAINFRAMESHOW_X4, 
 wxID_MAINFRAMESTART_BTN, wxID_MAINFRAMESTEP_LBL, wxID_MAINFRAMESTEP_SLDR, 
 wxID_MAINFRAMETIME_RANGE_LBL, wxID_MAINFRAMETIME_SLDR, 
 wxID_MAINFRAMEVAR1_LBL, wxID_MAINFRAMEVARIABLES_TEXTCTRL, 
] = [wx.NewId() for _init_ctrls in range(26)]

class Mainframe(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_MAINFRAME, name=u'Mainframe',
              parent=prnt, pos=wx.Point(392, 181), size=wx.Size(946, 554),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Terminal')
        self.SetClientSize(wx.Size(946, 554))
        self.SetToolTipString(u'Main window')
        self.SetIcon(wx.Icon(u'/home/stanke/Documents/s.ico',
              wx.BITMAP_TYPE_ICO))

        self.adresa = wx.TextCtrl(id=wxID_MAINFRAMEADRESA, name=u'adresa',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(272, 31), style=0,
              value=u'localhost:all')
        self.adresa.SetToolTipString(u'Adress and port of listening server')
        self.adresa.SetEditable(True)
        self.adresa.Enable(True)
        self.adresa.Bind(wx.EVT_CHAR, self.adress_key_enter)

        self.connect_btn = wx.Button(id=wxID_MAINFRAMECONNECT_BTN,
              label=u'Connect', name=u'connect_btn', parent=self,
              pos=wx.Point(272, 0), size=wx.Size(144, 31), style=0)
        self.connect_btn.SetToolTipString(u'Connect to server')
        self.connect_btn.Bind(wx.EVT_BUTTON, self.connect_to_server,
              id=wxID_MAINFRAMECONNECT_BTN)

        self.richTextCtrl1 = wx.richtext.RichTextCtrl(id=wxID_MAINFRAMERICHTEXTCTRL1,
              parent=self, pos=wx.Point(0, 32), size=wx.Size(416, 232),
              style=wx.richtext.RE_MULTILINE, value=u'Succesfully started')
        self.richTextCtrl1.SetLabel(u'')
        self.richTextCtrl1.SetToolTipString(u'Server-related informations')
        self.richTextCtrl1.SetEditable(False)
        self.richTextCtrl1.SetHelpText(u'')
        self.richTextCtrl1.Enable(False)

        self.load_vars_btn = wx.Button(id=wxID_MAINFRAMELOAD_VARS_BTN,
              label=u'Load variables', name=u'load_vars_btn', parent=self,
              pos=wx.Point(0, 264), size=wx.Size(120, 32), style=0)
        self.load_vars_btn.SetToolTipString(u'Re/Load variables from param file')
        self.load_vars_btn.Enable(False)
        self.load_vars_btn.Bind(wx.EVT_BUTTON, self.load_variables,
              id=wxID_MAINFRAMELOAD_VARS_BTN)

        self.start_btn = wx.Button(id=wxID_MAINFRAMESTART_BTN,
              label=u'Start simulation', name=u'start_btn', parent=self,
              pos=wx.Point(120, 264), size=wx.Size(120, 32), style=0)
        self.start_btn.SetToolTipString(u'Start simulation on server')
        self.start_btn.Enable(False)
        self.start_btn.Bind(wx.EVT_BUTTON, self.start_simulation,
              id=wxID_MAINFRAMESTART_BTN)

        self.plot_btn = wx.Button(id=wxID_MAINFRAMEPLOT_BTN,
              label=u'Draw graph', name=u'plot_btn', parent=self,
              pos=wx.Point(666, 0), size=wx.Size(126, 32), style=0)
        self.plot_btn.SetToolTipString(u'Plot all data received from server')
        self.plot_btn.Enable(False)
        self.plot_btn.Bind(wx.EVT_BUTTON, self.plot_values,
              id=wxID_MAINFRAMEPLOT_BTN)

        self.help_btn = wx.Button(id=wxID_MAINFRAMEHELP_BTN, label=u'Help',
              name=u'help_btn', parent=self, pos=wx.Point(352, 264),
              size=wx.Size(64, 31), style=0)
        self.help_btn.SetToolTipString(u'Help me please, I am stuck!')
        self.help_btn.Enable(True)
        self.help_btn.Bind(wx.EVT_BUTTON, self.get_help,
              id=wxID_MAINFRAMEHELP_BTN)

        self.step_sldr = wx.Slider(id=wxID_MAINFRAMESTEP_SLDR, maxValue=100,
              minValue=10, name=u'step_sldr', parent=self, pos=wx.Point(104,
              296), size=wx.Size(312, 24), style=wx.SL_HORIZONTAL, value=20)
        self.step_sldr.SetLabel(u'')
        self.step_sldr.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK,
              self.step_size_modified, id=wxID_MAINFRAMESTEP_SLDR)

        self.step_lbl = wx.StaticText(id=wxID_MAINFRAMESTEP_LBL,
              label=u'Step size 20ms', name=u'step_lbl', parent=self,
              pos=wx.Point(0, 296), size=wx.Size(104, 19), style=0)

        self.time_range_lbl = wx.StaticText(id=wxID_MAINFRAMETIME_RANGE_LBL,
              label=u'Time range 10s', name=u'time_range_lbl', parent=self,
              pos=wx.Point(0, 320), size=wx.Size(104, 19), style=0)

        self.time_sldr = wx.Slider(id=wxID_MAINFRAMETIME_SLDR, maxValue=100,
              minValue=1, name=u'time_sldr', parent=self, pos=wx.Point(104,
              320), size=wx.Size(312, 21), style=wx.SL_HORIZONTAL, value=10)
        self.time_sldr.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK,
              self.time_range_modified, id=wxID_MAINFRAMETIME_SLDR)

        self.variables_textctrl = wx.richtext.RichTextCtrl(id=wxID_MAINFRAMEVARIABLES_TEXTCTRL,
              parent=self, pos=wx.Point(0, 400), size=wx.Size(208, 184),
              style=wx.richtext.RE_MULTILINE,
              value=u'M0=4\nM1=0.36\nM=M0+M1\nls=0.451\ntheta=0.08433\nN=0.1624\nN01=0.3413**0.5\nFr=10\nC=0.00145\ng=9.81\nF=0')
        self.variables_textctrl.SetToolTipString(u'Conditions and variables')
        self.variables_textctrl.SetLabel(u'')
        self.variables_textctrl.SetName(u'variables_textctrl')

        self.var1_lbl = wx.StaticText(id=wxID_MAINFRAMEVAR1_LBL,
              label=u'Variables', name=u'var1_lbl', parent=self, pos=wx.Point(0,
              344), size=wx.Size(208, 24), style=0)

        self.condt_txtctrl = wx.richtext.RichTextCtrl(id=wxID_MAINFRAMECONDT_TXTCTRL,
              parent=self, pos=wx.Point(208, 368), size=wx.Size(208, 224),
              style=wx.richtext.RE_MULTILINE,
              value=u'x1_0=1\nx2_0=0\nx3_0=0\nx4_0=0\nxf_0=0')
        self.condt_txtctrl.SetLabel(u'')
        self.condt_txtctrl.SetName(u'condt_txtctrl')

        self.condt_lbl = wx.StaticText(id=wxID_MAINFRAMECONDT_LBL,
              label=u'Conditions', name=u'condt_lbl', parent=self,
              pos=wx.Point(208, 344), size=wx.Size(208, 24), style=0)

        self.databaza = wx.richtext.RichTextCtrl(id=wxID_MAINFRAMEDATABAZA,
              parent=self, pos=wx.Point(416, 32), size=wx.Size(528, 520),
              style=wx.richtext.RE_MULTILINE, value=u'')
        self.databaza.SetLabel(u'')
        self.databaza.SetToolTipString(u'Database')
        self.databaza.SetName(u'databaza')

        self.show_x1 = wx.CheckBox(id=wxID_MAINFRAMESHOW_X1, label=u'X1',
              name=u'show_x1', parent=self, pos=wx.Point(416, 0),
              size=wx.Size(50, 32), style=0)
        self.show_x1.SetValue(True)

        self.show_x2 = wx.CheckBox(id=wxID_MAINFRAMESHOW_X2, label=u'X2',
              name=u'show_x2', parent=self, pos=wx.Point(466, 0),
              size=wx.Size(50, 32), style=0)
        self.show_x2.SetValue(True)

        self.show_x3 = wx.CheckBox(id=wxID_MAINFRAMESHOW_X3, label=u'X3',
              name=u'show_x3', parent=self, pos=wx.Point(516, 0),
              size=wx.Size(50, 32), style=0)
        self.show_x3.SetValue(True)

        self.show_x4 = wx.CheckBox(id=wxID_MAINFRAMESHOW_X4, label=u'X4',
              name=u'show_x4', parent=self, pos=wx.Point(566, 0),
              size=wx.Size(50, 32), style=0)
        self.show_x4.SetValue(True)

        self.show_f = wx.CheckBox(id=wxID_MAINFRAMESHOW_F, label=u'F',
              name=u'show_f', parent=self, pos=wx.Point(616, 0),
              size=wx.Size(50, 32), style=0)
        self.show_f.SetValue(True)

        self.anime_btn = wx.Button(id=wxID_MAINFRAMEANIME_BTN,
              label=u'Reserved', name=u'anime_btn', parent=self,
              pos=wx.Point(240, 264), size=wx.Size(112, 32), style=0)
        self.anime_btn.SetToolTipString(u"Show result")
        self.anime_btn.Enable(False)

        self.draw_btn = wx.Button(id=wxID_MAINFRAMEDRAW_BTN,
              label=u'Draw animation', name=u'draw_btn', parent=self,
              pos=wx.Point(792, 0), size=wx.Size(152, 32), style=0)
        self.draw_btn.SetToolTipString(u'Show animation of process')
        self.draw_btn.Bind(wx.EVT_BUTTON, self.draw_anim,
              id=wxID_MAINFRAMEDRAW_BTN)

        self.ki_ctrl = wx.SpinCtrl(id=wxID_MAINFRAMEKI_CTRL, initial=10,
              max=1000, min=0, name=u'ki_ctrl', parent=self, pos=wx.Point(104,
              368), size=wx.Size(104, 31), style=wx.SP_ARROW_KEYS)
        self.ki_ctrl.SetToolTipString(u'Regulator speed multiplier')

        self.kp_ctrl = wx.SpinCtrl(id=wxID_MAINFRAMEKP_CTRL, initial=10,
              max=1000, min=0, name=u'kp_ctrl', parent=self, pos=wx.Point(0,
              368), size=wx.Size(104, 31), style=wx.SP_ARROW_KEYS)
        self.kp_ctrl.SetToolTipString(u'Stabilisator response multiplier')

    def __init__(self, parent):
        self._init_ctrls(parent)
        #own variables
        self.connected=False
                
        
    def connect(self, adress):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            HOST,PORT=adress.split(":")
            if PORT=="all": #vyskusa vsetky porty od 20000 do 30000
                for i in range(20000,30000):
                    try:
                        self.s.connect((HOST, int(i)))
                        PORT=i
                        break
                    except:pass
                if PORT=="all":
                    self.richTextCtrl1.SetValue("No host available")
                    raise socket.error
            else:
                self.s.connect((HOST, int(PORT)))

            self.richTextCtrl1.SetValue(f"Connected to {HOST}:{PORT}")
            self.adresa.SetValue(f"{str(HOST)}:{str(PORT)}")
            self.adresa.Disable()
            self.connect_btn.SetLabel("Disconnect and Close")
            self.connect_btn.SetToolTipString(u'Terminate communication with host server and exit program')
            self.connected=True
            self.load_vars_btn.Enable()

        except socket.error:
            self.richTextCtrl1.SetValue("Connection refused (no host listening?)")
        except socket.gaierror:
            self.richTextCtrl1.SetValue("Connection refused (unknown host?)")
        except ValueError:
            self.richTextCtrl1.SetValue("Connection refused (bad port?)")
            
    def connect_to_server(self, event=None):
        if self.connected:
            self.richTextCtrl1.SetValue("Exitting")
            self.s.sendall("exit")
            self.s.close()
            quit()
        else:
            self.connect(self.adresa.GetValue())
            self.load_vars_btn.SetFocus()

    def step_size_modified(self, event):
        self.step_lbl.SetLabel(u'Step size %dms'%self.step_sldr.GetValue())
        self.load_vars_btn.SetFocus()

    def time_range_modified(self, event):
        self.time_range_lbl.SetLabel(u'Time range %ds'%self.time_sldr.GetValue())
        self.load_vars_btn.SetFocus()

    def adress_key_enter(self, event):
        if event.GetKeyCode()==13:
            self.connect_to_server()
        else:
            event.Skip()
                       
    def start_simulation(self, event):
        vrange=int(self.time_sldr.GetValue())
        vstep=int(self.step_sldr.GetValue())
        self.s.sendall("simu")
        while self.s.recv(128)[:3] != "gmt": pass

        self.richTextCtrl1.SetValue("Sending time frame")
        self.t=[t/1000.0*vstep for t in range(int(vrange*1000/vstep))]

        self.s.sendall(str(len(self.t)+128))
        while self.s.recv(128)[:3] != "ack": pass

        self.s.sendall("t=[t/1000.0*%d for t in range(int(%d*1000.0/%d))] "%(vstep, vrange, vstep))

        while self.s.recv(1024)[:3] != "gmx": pass
        self.richTextCtrl1.SetValue("Sending default values")
        self.s.sendall("x0=[%f,%f,%f,%f,%f]\nK=%f"%(self.x1_0,self.x2_0,self.x3_0,self.x4_0, self.xf_0, self.xf_0))

        data=self.s.recv(1024)
        while data[:4] != "data":
            data = self.s.recv(1024)[:4]

        self.richTextCtrl1.SetValue("Receiving values")

        f = self.s.makefile('rb', int(data[4:])+1024 )
        data = pickle.load(f)
        f.close()

        text=""
        for i in data:
            for j in i:
                text+="%.3f "%j
            text+="\n"
        self.databaza.SetValue(text)

        self.sol=data
        self.plot_btn.Enable()
        self.anime_btn.Enable()
        self.richTextCtrl1.SetValue("Simulation finished succesfully!\nData ready for plotting.")

        subor=file("simulation.dat","w")
        subor.write(str(self.step_sldr.GetValue())+"\n"+self.databaza.GetValue())
        subor.close()

        self.plot_btn.SetFocus()
        
    def plot_values(self, event):
        plt.ion()
        plt.figure()
        
        if self.show_x1.GetValue(): plt.plot(self.t,self.sol[:,0],label="x1")
        if self.show_x2.GetValue(): plt.plot(self.t,self.sol[:,1],label="x2")
        if self.show_x3.GetValue(): plt.plot(self.t,self.sol[:,2],label="x3")
        if self.show_x4.GetValue(): plt.plot(self.t,self.sol[:,3],label="x4")
        if self.show_f.GetValue():  plt.plot(self.t,self.sol[:,4],label="F")
        
        plt.grid()
        plt.xlabel('Time')
        plt.ylabel('')
        plt.title('Values')
        plt.legend(loc=0)
        
    def get_help(self, event):
        info = wx.AboutDialogInfo()
        info.Name = 'pySim'
        info.Version = '1.0.0'
        info.Copyright = '(C) Stanislav Rubint 2013'
        info.Description = 'Client-server based simulation and regulation program written in python 2.7.3'
        wx.AboutBox(info)

    def draw_anim(self, event):
        os.system("python animacia.py")
        
    def load_variables(self, event): #nasleduje vypocet bulharskych konstant
        vars="kP=%f\nkI=%f\n"%(self.kp_ctrl.GetValue(),self.ki_ctrl.GetValue())+self.variables_textctrl.GetValue()+"\nb2=-theta/(N01**2)\nb4=-N/(N01**2)\na22=-theta*Fr/(N01**2)\na23=-N**2*g/(N01**2)\na24=N*C/(N01**2)\na25=theta*N/(N01**2)\na42=N*Fr/(N01**2)\na43=M*N*g/(N01**2)\na44=-M*C/(N01**2)\na45=-N**2/(N01**2)"

        self.s.sendall(f"exec{vars}")
        while self.s.recv(16)[:3] != "ack":pass
        self.richTextCtrl1.SetValue("Variables transmitted to server")
        self.load_vars_btn.SetLabel("Reload variables")
        exec(self.condt_txtctrl.GetValue().replace("x","self.x"))
        self.start_btn.Enable()
        self.start_btn.SetFocus()
        

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show()
    #app.MainLoop()
