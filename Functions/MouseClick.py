from tkinter import *
from tkinter import ttk, messagebox
import keyboard,os,re,tempfile
from Functions.MouseFuncs import getpos
from Functions.Save import save,steps

IMGS_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Imgs/MouseClick/'))

  
ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

class MouseClickAction:
    def __init__(self,window,index_number,arg):
   
        self.window = Toplevel(window)

        self.window.configure(bg = "#ffffff")
        self.window.geometry("552x407+{}+{}".format(int(self.window.winfo_screenwidth() // 2 - (552/2)),int(self.window.winfo_screenheight() // 2 - (407/2))))  
        self.window.title("       ")
        self.window.wm_iconbitmap(ICON_PATH) 
        self.window.lift() 
        self.window.grab_set()  
        self.window.after(0, lambda: window.focus_force())        
        self.selected_button =  StringVar()
      
        self.x = StringVar()
        self.y = StringVar()
    

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
            image= self.background_img
        )

        self.canvas.create_text(
            112.0, 288.5,
            text = "Botão",
            fill = "#000000",
            font = ("Inter-Light", int(16.0))
        )

        self.canvas.create_text(
            129.0, 208.5,
            text = "X:",
            fill = "#000000",
            font = ("Inter-Light", int(16.0))
        )

        self.canvas.create_text(
            129.0, 245.5,
            text = "Y:",
            fill = "#000000",
            font = ("Inter-Light", int(16.0))
        )

        if index_number == "Null":
            self.select_button = ttk.OptionMenu(self.window,
                self.selected_button,'Selecione o botão','Direito', 'Esquerdo', 'Scroll', command=self.callback
            )
            self.select_button.place(x = 145, y = 274, width = 180, height = 30)
            
        else:            
            if "DIREITO" in arg:                                                                          
                self.select_button = ttk.OptionMenu(self.window,
                    self.selected_button,'Direito','Direito', 'Esquerdo', 'Scroll', command=self.callback
                )                                                                            
            elif "ESQUERDO" in arg:                                
                self.select_button = ttk.OptionMenu(self.window,
                    self.selected_button,'Esquerdo','Direito', 'Esquerdo', 'Scroll', command=self.callback
                )
                self.selected_button.set("Esquerdo")   
            elif "MEIO" in arg:                            
                self.select_button = ttk.OptionMenu(self.window,
                    self.selected_button,'Scroll','Direito', 'Esquerdo', 'Scroll', command=self.callback
                )
                self.selected_button.set("Scroll") 
            self.select_button.place(x = 145, y = 274, width = 180, height = 30)            

        self.x_img = PhotoImage(file = os.path.join(IMGS_PATH, "img_textBox1.png"))
        self.x_bg = self.canvas.create_image(
            160.0, 209.0,
            image = self.x_img
        )

        if index_number == "Null":
            self.x_entry = Entry(self.window,
                textvariable=self.x,
                bd = 0,
                bg = "#ffffff",
                highlightthickness = 0
            )

            self.x_entry.place(x = 145, y = 197, width = 29, height = 25)
        else:
            only_digits = re.findall(r'(?<=X:)\d+|(?<=Y:)\d+', arg)       
            self.formated_text_x = int(only_digits[0])      
            self.x.set(self.formated_text_x)  
            self.x_entry = Entry(self.window,
                textvariable=self.x,
                bd = 0,
                bg = "#ffffff",
                highlightthickness = 0
            )

            self.x_entry.place(x = 145, y = 197, width = 29, height = 25)

        self.y_img = PhotoImage(file = os.path.join(IMGS_PATH, "img_textBox2.png"))
        self.y_bg = self.canvas.create_image(
            160.0, 247.0,
            image = self.y_img
        )

        if index_number == "Null":
            self.y_entry = Entry(self.window,
                textvariable=self.y,
                bd = 0,
                bg = "#ffffff",
                highlightthickness = 0
            )

            self.y_entry.place(x = 145, y = 235, width = 27, height = 25)

        else:
            only_digits = re.findall(r'(?<=X:)\d+|(?<=Y:)\d+', arg)       
            self.formated_text_y = int(only_digits[1])              
            self.y.set(self.formated_text_y)           
            self.y_entry = Entry(self.window,
                textvariable=self.y,
                bd = 0,
                bg = "#ffffff",
                highlightthickness = 0
            )

            self.y_entry.place(x = 145, y = 235, width = 27, height = 25)

        self.savebutton_img = PhotoImage(file = os.path.join(IMGS_PATH, "saveButton.png"))
        self.savebutton = Button(self.window,
            image = self.savebutton_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.save_parameters(index_number),
            relief = "flat"
        )

        self.savebutton.place( x = 423, y = 347, width = 122, height = 56)

        self.deletebutton_img = PhotoImage(file = os.path.join(IMGS_PATH, "deleteImage.png"))
        if index_number == "Null":
            pass
        else:
            self.deleteButton = Button(self.canvas,
            image = self.deletebutton_img,
            borderwidth = 0,
            highlightthickness = 0,
            command= lambda: self.delete_action(index_number),
            relief = "flat"
            )   

            self.deleteButton.place(x = 290, y = 349, width = 122, height = 56)           

    def callback(self,selection):     
        self.selected_button = selection 
         
    def is_type_int(self,*args):
        item = self.x.get()
        try:
            item_type = type(int(item))
            if item_type == type(int(1)):
                return
        except:
            self.x_entry.delete(0, 'end')
        item = self.y.get()
        try:
            item_type = type(int(item))
            if item_type == type(int(1)):
                return
        except:
            self.y_entry.delete(0, 'end')

        self.x.trace("w", self.is_type_int)
        self.y.trace("w", self.is_type_int)

    def get_x_y_position(self):
        return getpos()    

    def capture_position(self):
        if not keyboard.is_pressed('ctrl'):               
            self.is_pressed = False
        if not self.is_pressed:
            if keyboard.is_pressed('ctrl'):
                self.x_entry.delete(0, 'end')
                self.y_entry.delete(0,'end')
                self.get_x_y_position()
                self.x_entry.insert(0,self.get_x_y_position()[0])
                self.y_entry.insert(0,self.get_x_y_position()[1])
                self.is_pressed = True                              
        self.window.after(1, self.capture_position)

    def save_parameters(self,index_number):     
        if self.x.get() and self.y.get():
            if index_number == "Null":  
                if self.selected_button == "Direito":
                    save(f"pyautogui.rightClick({self.x.get()},{self.y.get()})","Null",f"DIREITO EM X:{self.x.get()} Y:{self.y.get()}")
                    self.window.quit()  
                    self.window.destroy()  
                elif self.selected_button == "Esquerdo":
                    save(f"pyautogui.leftClick({self.x.get()},{self.y.get()})","Null",f"ESQUERDO EM X:{self.x.get()} Y:{self.y.get()}")
                    self.window.quit()  
                    self.window.destroy() 
                elif self.selected_button == "Scroll":
                    save(f"pyautogui.middleClick({self.x.get()},{self.y.get()})","Null",f"MEIO EM X:{self.x.get()} Y:{self.y.get()}")
                    self.window.quit()  
                    self.window.destroy() 
                else:
                    self.select_button.focus_set()
                    messagebox.showwarning("ERRO", "Campo 'Botão' obrigatório")
            else:        
                try:
                    selected = self.selected_button.get()
                except:
                    selected = self.selected_button              
                if selected == 'Direito':
                    steps.pop(int(index_number))
                    save(f"pyautogui.rightClick({self.x.get()},{self.y.get()})",index_number,f"DIREITO EM X:{self.x.get()} Y:{self.y.get()}")
                    self.window.quit()  
                    self.window.destroy() 
                elif selected == "Esquerdo":
                    steps.pop(int(index_number))
                    save(f"pyautogui.leftClick({self.x.get()},{self.y.get()})",index_number,f"ESQUERDO EM X:{self.x.get()} Y:{self.y.get()}")
                    self.window.quit()  
                    self.window.destroy()
                elif selected == "Scroll":
                    steps.pop(int(index_number))
                    save(f"pyautogui.middleClick({self.x.get()},{self.y.get()})",index_number,f"MEIO EM X:{self.x.get()} Y:{self.y.get()}")
                    self.window.quit()  
                    self.window.destroy()
                else:
                    self.select_button.focus_set()                    
                    messagebox.showwarning("ERRO", "Campo 'Botão' obrigatório")
        else:
            messagebox.showwarning("ERRO", "Campos 'X e Y' obrigatório")

    def delete_action(self,index_number):
        steps.pop(int(index_number))  
        save(f"delete",index_number,"del")
        self.window.quit()  
        self.window.destroy()
            
    def main(self):
        self.window.resizable(False, False)
        self.window.after(1, self.capture_position)
        self.window.mainloop()




                

    
