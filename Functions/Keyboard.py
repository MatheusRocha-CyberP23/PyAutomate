from tkinter import *
from tkinter import ttk,messagebox
from Functions.Save import save, steps
import os,tempfile

IMGS_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Imgs/Keyboard/'))


ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

class KeyboardAction:
    def __init__(self,window,index_number,arg):

        self.window = Toplevel(window)

        self.window.configure(bg = "#ffffff")
        self.window.geometry("552x407+{}+{}".format(int(self.window.winfo_screenwidth() // 2 - (552/2)),int(self.window.winfo_screenheight() // 2 - (407/2))))  
        self.window.title("       ")
        self.window.wm_iconbitmap(ICON_PATH) 
        self.window.lift() 
        self.window.grab_set()  
        self.window.after(0, lambda: window.focus_force())                   
              
        self.text_var = StringVar()

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

        self.savebutton_img = PhotoImage(file = os.path.join(IMGS_PATH, "saveImg.png"))
        self.savebutton = Button(self.window,
            image = self.savebutton_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: save_parameters(index_number),
            relief = "flat"
        )

        self.savebutton.place(x = 422, y = 349, width = 122, height = 56)

        self.canvas.create_text(
            282.5, 79.5,
            text = "Armazene um texto específico em um arquivo",
            fill = "#000000",
            font = ("Inter-Light", int(14.0))
        )

        self.canvas.create_text(
            102.0, 23.0,
            text = "Armazenar texto",
            fill = "#000000",
            font = ("Inter-SemiBold", int(20.0))
        )

        self.canvas.create_text(
            110.0, 181.0,
            text = "Texto:",
            fill = "#000000",
            font = ("Inter-Light", int(12.0))
        )

        self.canvas.create_text(
            200, 271.0,
            text = 'Insira teclas especiais entre aspas e chaves "{}"\nE.G: Para dar enter em um texto'+ r" 'Oi"+r"{ENTER}'" ,
            fill = "#000000",
            font = ("Inter-Light", int(12.0))
        )
        
        
        if index_number == "Null":
            self.entry_text = ttk.Entry(self.window,
                width = 45,
                font = ("Inter-Regular", int(16.0)),
                textvariable = self.text_var
            )
            self.entry_text.place(x = 155.0, y = 171.0, height = 67.0, relwidth = 0.62)
        else:
            self.formated_text = arg
            self.formated_text = self.formated_text.replace("\n", "")
            self.formated_text = self.formated_text.rstrip()
            self.text_var.set(self.formated_text)
            self.entry_text = ttk.Entry(self.window,
                width = 45,
                font = ("Inter-Regular", int(16.0)),
                textvariable = self.text_var
            )
            self.entry_text.place(x = 155.0, y = 171.0, height = 67.0, relwidth = 0.62)

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
            self.formated_text = self.entry_text.get() 
            self.formated_text = self.formated_text.replace("\n", "")
            self.formated_text.rstrip()
            if self.entry_text.get():
                if index_number == "Null":     
                    save(f"send_keys('{self.entry_text.get()}')","Null",self.formated_text)
                    self.window.quit()  
                    self.window.destroy()
                else:
                    steps.pop(int(index_number))
                    save(f"send_keys('{self.entry_text.get()}')",index_number,self.formated_text)
                    self.window.quit()  
                    self.window.destroy() 
            else:
                self.entry_text.focus_set()
                messagebox.showwarning("ERRO", "Campo 'Texto' obrigatório")
        
        def delete_action(index_number):
            self.formated_text = self.entry_text.get() 
            self.formated_text = self.formated_text.replace("\n", "")
            self.formated_text.rstrip()
            steps.pop(int(index_number))  
            save(f"send_keys('{self.entry_text.get()}')",index_number,"del")
            self.window.quit()  
            self.window.destroy()   

        self.window.mainloop()


