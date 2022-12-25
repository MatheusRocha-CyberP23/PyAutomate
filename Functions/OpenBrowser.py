from tkinter import *
from Functions.Save import save, steps
from tkinter import messagebox
import os,tempfile

IMGS_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Imgs/OpenBrowser/'))


ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

class OpenBrowserAction:
    def __init__(self,window,index_number,arg):

        self.window = Toplevel(window)

        self.window.configure(bg = "#ffffff")
        self.window.geometry("552x407+{}+{}".format(int(self.window.winfo_screenwidth() // 2 - (552/2)),int(self.window.winfo_screenheight() // 2 - (407/2))))  
        self.window.title("       ")
        self.window.wm_iconbitmap(ICON_PATH) 
        self.window.lift() 
        self.window.grab_set()  
        self.window.after(0, lambda: window.focus_force())                   
        
        self.canvas = Canvas(
            self.window,
            bg = "#ffffff",
            height = 407,
            width = 552,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)

        self.background_img = PhotoImage(file = os.path.join(IMGS_PATH, "background.png"))
        self.background = self.canvas.create_image(
            461.5, 203.5,
            image= self.background_img)

        self.canvas.create_text(
            93.0, 190.5,
            text = "URL:",
            fill = "#000000",
            font = ("Inter-Light", int(16.0)))

        self.canvas.create_text(
            115.0, 23.0,
            text = "Abrir Navegador",
            fill = "#000000",
            font = ("Inter-SemiBold", int(20.0)))

        self.canvas.create_text(
            262.5, 79.5,
            text = "Abre uma nova aba no navegador \nno URL configurado. ",
            fill = "#000000",
            font = ("Inter-Light", int(14.0)))

        self.url_entry_img = PhotoImage(file = os.path.join(IMGS_PATH, "img_textBox0.png"))

        self.url_entry_bg = self.canvas.create_image(
            339.5, 189.0,
            image =  self.url_entry_img 
        )

       
        if index_number == "Null":
            self.url_entry = Entry(self.canvas,
                bd = 0,
                bg = "#ffffff",
                highlightthickness = 0
            )

            self.url_entry.place(x = 156, y = 176, width = 350,height = 26)
        else:
            self.text_var = StringVar()
            self.formated_text = arg
            self.formated_text = self.formated_text.replace("\n", "")   
            self.text_var.set(self.formated_text)
            self.url_entry = Entry(self.canvas,
                textvariable=self.text_var,
                bd = 0,
                bg = "#ffffff",
                highlightthickness = 0)

            self.url_entry.place(x = 156, y = 176, width = 350,height = 26)

        self.savebutton_img = PhotoImage(file = os.path.join(IMGS_PATH, "saveImage.png"))
        self.savebutton = Button(self.canvas,
            image = self.savebutton_img,
            borderwidth = 0,
            highlightthickness = 0,
            command= lambda: save_parameters(index_number),
            relief = "flat"
        )   

        self.savebutton.place(x = 422, y = 349, width = 122,height = 56)

        self.delete_img = PhotoImage(file = os.path.join(IMGS_PATH, "deleteImage.png"))

        if index_number == "Null":
            pass
        else:
            self.deletebutton = Button(self.canvas,
            image = self.delete_img,
            borderwidth = 0,
            highlightthickness = 0,
            command= lambda: delete_action(index_number),
            relief = "flat"
            )   
            self.deletebutton.place(x = 290, y = 349, width = 122, height = 56)

        def save_parameters(index_number):
            self.formated_text = self.url_entry.get() 
            self.formated_text = self.formated_text.replace("\n", "")
            self.formated_text.rstrip()
            if self.url_entry.get():
                if index_number == "Null":     
                    save(f"webbrowser.open_new_tab('{self.url_entry.get()}')","Null",self.formated_text)
                    self.window.quit()  
                    self.window.destroy()
                else:
                    steps.pop(int(index_number))
                    save(f"webbrowser.open_new_tab('{self.url_entry.get()}')",index_number,self.formated_text)
                    self.window.quit()  
                    self.window.destroy() 
            else:
                self.url_entry.focus_set()
                messagebox.showwarning("ERRO", "Campo 'URL' obrigatório")

        def delete_action(index_number):
            self.formated_text = self.url_entry.get() 
            self.formated_text = self.formated_text.replace("\n", "")
            self.formated_text.rstrip()
            steps.pop(int(index_number))  
            save(f"webbrowser.open_new_tab('{self.url_entry.get()}')",index_number,"del")
            self.window.quit()  
            self.window.destroy()   

        self.window.resizable(False, False)
        self.window.mainloop()


