from tkinter import *
from tkinter import ttk, messagebox
import os,tempfile


ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

class CreateProject:
    def __init__(self, window):
        self.imgs_path = (os.path.dirname(os.path.realpath(__file__))) + '/Imgs/CreateProject/'
        self.projects_path = (os.path.dirname(os.path.realpath(__file__))) + "/Projects/"
        self.window = Toplevel(window)
        self.window.geometry("552x407+{}+{}".format(int(self.window.winfo_screenwidth() // 2 - (552/2)),int(self.window.winfo_screenheight() // 2 - (407/2))))
        self.window.title("Criar Projeto")
        self.window.wm_iconbitmap(ICON_PATH)
        self.window.configure(bg = "#ffffff")
        self.window.focus_force()
        self.window.lift()   
        self.window.grab_set()

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

        self.background_img = PhotoImage(
            file=os.path.join(self.imgs_path, "background.png")
        )
        self.background = self.canvas.create_image(
            461.5, 203.5, image=self.background_img
        )

        self.new_project_entry_img =  PhotoImage(
            file=os.path.join(self.imgs_path, "img_textBox0.png")
        )
        self.new_project_entry_background = self.canvas.create_image(
            287.5, 199.5, image=self.new_project_entry_img
        )
        self.entry_text = StringVar()
        self.new_project_name_entry = Entry(self.window,
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0,
            textvariable = self.entry_text
        )    

        self.new_project_name_entry.place(x = 63, y = 186, width = 450, height = 29)

        self.create_button_img = PhotoImage(
            file=os.path.join(self.imgs_path, "img0.png")
        )

        self.create_button = Button(
            self.window,
            image = self.create_button_img,
            borderwidth = 0,
            highlightthickness = 0,    
            command = self.create_project,        
            relief = "flat"
        )
        self.create_button.place(x = 423, y = 347, width = 122, height = 56)       
        self.entry_text.trace("w", lambda *args: self.character_limit(self.entry_text))
        self.old_value = ''
    def create_project(self):
        self.project_name = self.new_project_name_entry.get()
        if not self.new_project_name_entry.get():
            self.new_project_name_entry.focus_set()
            messagebox.showwarning("ERRO", "Campo 'Nome do Projeto' obrigatório.")

        elif os.path.exists(os.path.join(self.projects_path, self.new_project_name_entry.get()+".txt")):
            self.new_project_name_entry.focus_set()
            messagebox.showwarning("ERRO", f"{self.new_project_name_entry.get()} Já existe.")

        else:
            with open((os.path.dirname(os.path.realpath(__file__))) + f"/Projects/{self.new_project_name_entry.get()}.txt", "w") as created_project:
                created_project.write('')
            with open((os.path.dirname(os.path.realpath(__file__))) + f"/Projects/{self.new_project_name_entry.get()}T.txt", "w") as created_project:
                created_project.write('')
            with open((os.path.dirname(os.path.realpath(__file__))) + f"/Projects/{self.new_project_name_entry.get()}TT.txt", "w") as created_project:
                created_project.write('')
            self.window.quit()  
            self.window.destroy()

    def character_limit(self,entry_text):
        if len(self.entry_text.get()) <= 15:
            self.old_value = self.entry_text.get() # accept change
        else:
            self.entry_text.set(self.old_value) # reject change

    

    def return_name(self):   
        return self.project_name

    def main(self):
        self.window.resizable(False, False)
        self.window.mainloop()

   




   
