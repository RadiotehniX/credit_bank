import wx
import wx.grid
import psycopg2
from psycopg2.extensions import register_type, UNICODE

CONN_STR = "host='nix.agtu.ru' dbname='db371102' user='mispisit371102_03' password='mispisit371102_03'"

class ConditionsFrame(wx.Frame):
    def __init__(self, parent, id):
        register_type(UNICODE)
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        cur.execute('select * from conditions')
        cols = cur.description
        row = cur.fetchall()
        c = len(row)+1

        wx.Frame.__init__(self, parent, id, 'Working with Conditions', \
        size=(500, 400), style=wx.DEFAULT_FRAME_STYLE)
        self.window1 = wx.SplitterWindow(self, -1, style=wx.NO_BORDER)
        self.panel1 = wx.Panel(self.window1, -1)
        self.panel2 = wx.Panel(self.window1, -1)
        self.Bind(wx.EVT_CLOSE, lambda event: self.Destroy())
        self.download = wx.Button(self.panel2, -1, 'Download')
        self.new = wx.Button(self.panel2, -1, 'New')
        self.update = wx.Button(self.panel2, -1, 'Update')
        self.delete = wx.Button(self.panel2, -1, 'Delete')
        self.grid = wx.grid.Grid(self.panel1, -1, size=(1,1))
        self.grid.CreateGrid(c, 3)
        self.grid.SetRowLabelSize(40)
        self.grid.SetColLabelSize(40)
        self.grid.SetMinSize((500, 300))
        self.grid.SetColLabelValue(0, 'id')
        self.grid.SetColSize(0, 40)
        self.grid.SetColLabelValue(1, 'SumMin')
        self.grid.SetColSize(1, 200)
        self.grid.SetColLabelValue(2, 'SumMax')
        self.grid.SetColSize(2, 200)
        self.Bind(wx.EVT_BUTTON, self.on_download, self.download)
        self.Bind(wx.EVT_BUTTON, self.on_new, self.new)
        self.Bind(wx.EVT_BUTTON, self.on_update, self.update)
        self.Bind(wx.EVT_BUTTON, self.on_delete, self.delete)
        self.grid.Bind(wx.EVT_KEY_DOWN, self.keydown)
        self.panel1.SetMinSize((500, 370))
        self.panel2.SetMinSize((500, 30))
        self.window1.SetMinSize((500, 400))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.grid, -1, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        sizer2.AddMany([(self.download, -1, wx.EXPAND|wx.ADJUST_MINSIZE, 0),
        (self.new, -1, wx.EXPAND|wx.ADJUST_MINSIZE, 0),
        (self.update, -1, wx.EXPAND|wx.ADJUST_MINSIZE, 0),
        (self.delete, -1, wx.EXPAND|wx.ADJUST_MINSIZE, 0)])
        self.panel1.SetSizer(sizer1)
        self.panel2.SetSizer(sizer2)
        self.window1.SplitHorizontally(self.panel1, self.panel2)
        sizer.Add(self.window1, 1, wx.ALL|wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()
        self.Centre()
        self.printConditions()

    def on_download(self, event):
        self.printConditions()

    def printConditions(self):
        register_type(UNICODE)
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        cur.execute('select * from conditions')
        row = cur.fetchone()
        cols = cur.description
        i = 0
        while row:
            for col in xrange(len(cols)):
                self.grid.SetCellValue(i, col, unicode(row[col]))
            i += 1
            self.grid.SetReadOnly(i, 0, True)
            row = cur.fetchone()
        self.grid.DeleteRows(i, self.grid.GetNumberRows()-i, False)
        cur.close()
        conn.close()

    def keydown(self, event):
        if event.GetKeyCode() == wx.WXK_INSERT:
            self.grid.InsertRows(self.grid.GetNumberRows(), 1, False)

    def on_new(self, event):
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        tb = self.grid.GetTable()
        try:
            for i in xrange(self.grid.GetNumberRows()):
                if tb.GetValue(i, 1) != '' and i == self.grid.GetGridCursorRow():
                    cur.callproc('"AddConditions"', [tb.GetValue(i, 1), tb.GetValue(i, 2)])
        except psycopg2.DatabaseError as e: wx.MessageBox(str(e),'Error',wx.OK|wx.ICON_ERROR)
        conn.commit()
        cur.close()
        conn.close()

    def on_update(self, event):
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        tb = self.grid.GetTable()
        try:
            for i in xrange(self.grid.GetNumberRows()):
                if tb.GetValue(i, 1) != '' and i == self.grid.GetGridCursorRow():
                    if (wx.MessageBox('Realy update conditions?','Update Conditions',wx.YES_NO|wx.ICON_QUESTION)) == 2:
                        cur.callproc('"updateConditions"', [tb.GetValue(i, 0), tb.GetValue(i, 1), tb.GetValue(i, 2)])
        except psycopg2.DatabaseError as e: wx.MessageBox(str(e),'Error',wx.OK|wx.ICON_ERROR)
        conn.commit()
        cur.close()
        conn.close()

    def on_delete(self, event):
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        tb = self.grid.GetTable()
        try:
            for i in xrange(self.grid.GetNumberRows()):
                if i == self.grid.GetGridCursorRow():
                    if (wx.MessageBox('Realy?','Delete Conditions',wx.YES_NO|wx.ICON_QUESTION)) == 2:
                        cur.callproc('"deleteConditions"', [tb.GetValue(i, 0)])
        except psycopg2.DatabaseError as e: wx.MessageBox(str(e),'Error',wx.OK|wx.ICON_ERROR)
        conn.commit()
        cur.close()
        conn.close()
        self.printConditions()