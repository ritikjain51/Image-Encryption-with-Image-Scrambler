import wx,sys
from tkinter import *
from tkinter.filedialog import *
from tkinter import Tk, ttk, messagebox
from hashlib import sha256
import Image_operation_Library as op

filename=""
file_destination=""
tc2 = ""
tc1 = ""
pwd = None

#Input source file
def File_Input(x):
    global filename
    root = Tk()
    filename = askopenfilename(title = "Select File",filetype = (('PNG','.*png'),('RTK','*.RTK')))
    tc1.SetValue(filename)
    root.destroy()
    return

#Input destination file
def Folder_Input(x):
    global file_destination
    root = Tk()
    file_destination= askdirectory()
    tc2.SetValue(file_destination)
    root.destroy()

def Successfully_Decrypted():
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Success", "You Image has been Decrypted")
    return

def Successfully_encrypted():
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Success", "You Image has been Encrypted")
    return

def about_us_panel(x):
    root = Tk()
    root.withdraw()
    messagebox.showinfo("About US","Ritik Jain \nritikjain51@gmail.com\nShuabham Jain \nshubhamjaintsj@gmail.com")
    return

#Initial Frame method
class RootFrame(wx.Frame):

    def __init__(self, parent, title):    
        super(RootFrame, self).__init__(parent, title=title, size=(500, 300))

        self.InitUI()
        self.Centre()
        self.Show()     

    def InitUI(self):      
          global password
          panel = wx.Panel(self)

          sizer = wx.GridBagSizer(5, 5)
          #Inserting Image
          icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('icon.jpg'))
          sizer.Add(icon, pos=(0, 4), flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT,border=5)
         

          line = wx.StaticLine(panel)
          sizer.Add(line, pos=(1, 0), span=(1, 5), flag=wx.EXPAND|wx.BOTTOM, border=10)
          
          global tc2,tc1

          #Label printing
          text2 = wx.StaticText(panel, label="Browse Source File")
          sizer.Add(text2, pos=(2, 0), flag=wx.LEFT|wx.TOP, border=10)

          # Insert Textbox
          tc1 = wx.TextCtrl(panel)
          sizer.Add(tc1, pos=(2, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)

          #Button for source input
          button1 = wx.Button(panel, label="Browse...")
          sizer.Add(button1, pos=(2, 4), flag=wx.TOP|wx.RIGHT, border=5)
          button1.Bind(wx.EVT_BUTTON,File_Input)
          
          #Textbox for destination folder input
          text3 = wx.StaticText(panel, label="Browse Destination Folder")
          sizer.Add(text3, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)

          #Textbox for Textbox
          tc2 = wx.TextCtrl(panel)
          sizer.Add(tc2, pos=(3, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)
          
          #Button for destination folder input
          button2 = wx.Button(panel, label="Browse...")
          sizer.Add(button2, pos=(3, 4), flag=wx.TOP|wx.RIGHT, border=5)
          button2.Bind(wx.EVT_BUTTON,Folder_Input)

          text4 = wx.StaticText(panel, label="Enter Password")
          sizer.Add(text4, pos=(4, 0), flag=wx.LEFT, border=10)

          #Textbox for password
          global pwd
          pwd = wx.TextCtrl(panel, style= wx.TE_PASSWORD)
          sizer.Add(pwd, pos=(4, 1), span=(1, 3), flag=wx.EXPAND)
          
 
          button4 = wx.Button(panel, label="Encrypt")
          sizer.Add(button4, pos=(5, 3))
          button4.Bind(wx.EVT_BUTTON,image_open)

          button5 = wx.Button(panel, label="Decrypt")
          sizer.Add(button5, pos=(5, 4), span=(1, 1), flag=wx.BOTTOM|wx.RIGHT, border=5)
          button5.Bind(wx.EVT_BUTTON,cipher_open)

          button6 = wx.Button(panel, label= 'About US')
          sizer.Add(button6, pos=(0,0), span=(0,1))
          button6.Bind(wx.EVT_BUTTON, about_us_panel)
          
          sizer.AddGrowableCol(2)
          panel.SetSizer(sizer)


def checkpassword(password):

    '''
    Password consist of Lower characters,
    upper characters, digits, symbols
    '''
    import string
    flags = flagc = flagd = flagsy = False

    if len(password)<8:
        return False

    for i in password:
        if i in string.ascii_lowercase:
            flags = True
        elif i in string.ascii_uppercase:
            flagc = True
        elif i in string.digits:
            flagd = True
        elif i in string.punctuation + " ":
            flagsy = True

    if flags and flagc and flagd and flagsy:
        return True
    else:
        return False



def image_open(x):

    #Calling global Variables
    global filename
    global file_destination
    global pwd
    password = pwd.GetValue()

    root = Tk()

    x = ('.PNG','.png')

    #checking for source file
    if filename == "":
        messagebox.showerror("Error", "Select File")
        
    #checking for destination
    elif file_destination == "":
        messagebox.showerror("Error", "Select File Destination")
        
    #Checking for extension
    elif  not (filename.endswith(x)):
        messagebox.showerror("Error", "Invalid File")
        
    #Checking for null password
    elif password == "":
        messagebox.showerror("Error", "Enter Password")
    elif password != "" and filename != "":
        if not checkpassword(password):
          messagebox.showinfo("Error", "Enter a strong password")
        else:           
            password = sha256(password.encode()).hexdigest()
            op.encrypt_image(password,filename,file_destination)
            Successfully_encrypted()

def cipher_open(x):
    
    global filename
    global file_destination
    global pwd
    password = pwd.GetValue()
    
    root = Tk()

    
    x = ('.RTK')
    #Variable Validation
    if filename == "":
        messagebox.showerror("Error", "Select File")
    elif file_destination == "":
        messagebox.showerror("Error", "Select File Destination")
    elif password == "":
        messagebox.showerror("Error", "Enter password")
    elif not(filename.endswith(x)):
        messagebox.showerror("Error", "Invalid File")
    elif password != "" and filename != "":
        if not checkpassword(password):
            messagebox.showinfo("Error", "Enter a strong password")
        else :          
            password = sha256(password.encode()).hexdigest()
            op.decrypt_image(password,filename,file_destination)
            Successfully_Decrypted()


if __name__ == '__main__':
  
    app = wx.App()
    RootFrame(None, title="Image Encryptor")
    app.MainLoop()
