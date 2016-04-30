import PersonFrame
import TypeFrame
import ConditionsFrame
import CreditFrame
import datetime
import wx
import wx.grid
import psycopg2
from psycopg2.extensions import register_type, UNICODE

CONN_STR = "host='nix.agtu.ru' dbname='db371102' user='mispisit371102_03' password='mispisit371102_03'"

class DatabaseFrame(wx.Frame):
    def __init__(self, parent, id):
        register_type(UNICODE)
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        cur.execute('select personal_id, credit_id from credit where date_end < current_date')
        cols = cur.description
        row = cur.fetchall()
        c = len(row)+1

        wx.Frame.__init__(self, parent, id, 'Working with Database', \
        size=(400, 300), style=wx.DEFAULT_FRAME_STYLE)
        self.window1 = wx.SplitterWindow(self, -1, style=wx.BORDER_DEFAULT)
        self.panel1 = wx.Panel(self.window1, -1)
        self.panel2 = wx.Panel(self.window1, -1)
        self.Bind(wx.EVT_CLOSE, lambda event: self.Destroy())
        self.personal = wx.Button(self.panel2, -1, 'Personal')
        self.types = wx.Button(self.panel2, -1, 'Types')
        self.conditions = wx.Button(self.panel2, -1, 'Conditions')
        self.credits = wx.Button(self.panel2, -1, 'Credits')

        self.grid = wx.grid.Grid(self.panel1, -1, size=(1,1))
        self.grid.CreateGrid(10, 2)
        self.grid.SetRowLabelSize(40)
        self.grid.SetColLabelSize(40)
        self.grid.SetMinSize((300, 400))
        self.grid.SetColLabelValue(0, 'personal_id')
        self.grid.SetColSize(0, 100)
        self.grid.SetColLabelValue(1, 'credit_id')
        self.grid.SetColSize(1, 100)

        self.Bind(wx.EVT_BUTTON, self.on_person, self.personal)
        self.Bind(wx.EVT_BUTTON, self.on_type, self.types)
        self.Bind(wx.EVT_BUTTON, self.on_conditions, self.conditions)
        self.Bind(wx.EVT_BUTTON, self.on_credit, self.credits)

        self.panel1.SetMinSize((3000, 300))
        self.panel2.SetMinSize((100, 300))
        self.window1.SetMinSize((520, 300))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)

        sizer1.Add(self.grid, -1, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        sizer2.AddMany([(self.personal, -1, wx.EXPAND|wx.ADJUST_MINSIZE, 0),
        (self.types, -1, wx.EXPAND|wx.ADJUST_MINSIZE, 0),
        (self.conditions, -1, wx.EXPAND|wx.ADJUST_MINSIZE, 0),
        (self.credits, -1, wx.EXPAND|wx.ADJUST_MINSIZE, 0)])
        self.panel1.SetSizer(sizer1)
        self.panel2.SetSizer(sizer2)
        self.window1.SplitVertically(self.panel1, self.panel2)
        sizer.Add(self.window1, 1, wx.ALL|wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()
        self.Centre()
        self.printDebt()

    def printDebt(self):
        register_type(UNICODE)
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        cur.execute('select personal_id, credit_id from credit where date_end < current_date')
        row = cur.fetchone()
        cols = cur.description
        i = 0
        while row:
            for col in xrange(len(cols)):
                self.grid.SetCellValue(i, col, unicode(row[col]))
            i += 1
            self.grid.SetReadOnly(i, 0, True)
            row = cur.fetchone()

        row = cur.fetchall()
        if i==0:
            self.grid.DeleteRows(i, self.grid.GetNumberRows()-i-1, False)
            self.grid.SetCellValue(0,0,'No person')
            self.grid.SetCellValue(0,1,'with debt')
        else:
            self.grid.DeleteRows(i, self.grid.GetNumberRows()-i, False)
        cur.close()
        conn.close()

    def on_person(self, event):
        frame = PersonFrame.PersonFrame(parent=None, id=-1)
        frame.Show()

    def on_type(self, event):
        frame = TypeFrame.TypeFrame(parent=None, id=-1)
        frame.Show()

    def on_conditions(self, event):
        frame = ConditionsFrame.ConditionsFrame(parent=None, id=-1)
        frame.Show()

    def on_credit(self, event):
        frame = CreditFrame.CreditFrame(parent=None, id=-1)
        frame.Show()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = DatabaseFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()