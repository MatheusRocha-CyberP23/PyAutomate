from tkinter import * 
from tkinter import ttk,messagebox
from Functions.Save import save, steps
import os,tempfile
IMGS_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Imgs/Wait/'))


ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

class WaitAction:
    def __init__(self,window,index_number,arg):

        self.window = Toplevel(window)

        self.window.configure(bg = "#ffffff")
        self.window.geometry("552x407+{}+{}".format(int(self.window.winfo_screenwidth() // 2 - (552/2)),int(self.window.winfo_screenheight() // 2 - (407/2))))  
        self.window.title("       ")
        self.window.wm_iconbitmap(ICON_PATH) 
        self.window.lift() 
        self.window.grab_set()  
        self.window.after(0, lambda: window.focus_force())            

        self.selected_time_measure = StringVar()
       
        self.time = StringVar()

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

        self.savebutton_img = PhotoImage(file = os.path.join(IMGS_PATH, "saveImg.png"))
        self.savebutton = Button(self.window,
            image = self.savebutton_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.save_parameters(index_number),
            relief = "flat"
        )

        self.savebutton.place(x = 422, y = 349, width = 122, height = 56)

        self.canvas.create_text(
            110.0, 182.5,
            text = "Medidas:",
            fill = "#000000",
            font = ("Inter-Regular", int(20.0)))

        self.select_time_measure_img = PhotoImage(file = os.path.join(IMGS_PATH, "img_textBox0.png"))
        self.select_time_measure_bg = self.canvas.create_image(
            321.0, 182.5,
            image = self.select_time_measure_img
        )

        if index_number == "Null":
            self.select_time_measure = ttk.OptionMenu(self.window,
                self.selected_time_measure,
                'Segundos','Segundos', 'Minutos', 'Horas', command=self.callback
            )
            self.selected_time_measure.set('Segundos')
            self.select_time_measure.place(x = 171, y = 170, width = 300, height = 27)
        else:
            if "SEGUNDOS" in arg:
                self.select_time_measure = ttk.OptionMenu(self.window,
                    self.selected_time_measure,
                    'Segundos','Segundos', 'Minutos', 'Horas', command=self.callback
                )
                self.select_time_measure.place(x = 171, y = 170, width = 300, height = 27)
            if "MINUTOS" in arg:
                self.select_time_measure = ttk.OptionMenu(self.window,
                    self.selected_time_measure,
                    'Minutos','Segundos', 'Minutos', 'Horas', command=self.callback
                )
                self.select_time_measure.place(x = 171, y = 170, width = 300, height = 27)
            if "HORAS" in arg:
                self.select_time_measure = ttk.OptionMenu(self.window,
                    self.selected_time_measure,
                    'Horas','Segundos', 'Minutos', 'Horas', command=self.callback
                )
                self.select_time_measure.place(x = 171, y = 170, width = 300, height = 27)

        self.canvas.create_text(
            110.0, 218.5,
            text = "Tempo:",
            fill = "#000000",
            font = ("Inter-Regular", int(20.0))
        )

        self.entry_time_img = PhotoImage(file = os.path.join(IMGS_PATH, "img_textBox1.png"))
        self.entry_time_bg = self.canvas.create_image(
            321.0, 218.5,
            image = self.entry_time_img
        )   
        
        if index_number == "Null":
            self.entry_time = Entry(self.window,
                textvariable=self.time,
                bd = 0,
                bg = "#ffffff",
                highlightthickness = 0)

            self.entry_time.place(x = 171, y = 206, width = 300, height = 27)
        else:                     
            only_digits = [c for c in arg if c.isdigit()]       
            self.formated_numbers = int(''.join(only_digits))       
            self.time.set( self.formated_numbers)  
            self.entry_time = Entry(self.window,
                textvariable=self.time,
                bd = 0,
                bg = "#ffffff",
                highlightthickness = 0)

            self.entry_time.place(x = 171, y = 206, width = 300, height = 27)
        
        self.delete_img = PhotoImage(file = os.path.join(IMGS_PATH, "deleteImage.png"))

        if index_number == "Null":
            pass
        else:
            self.deletebutton = Button(self.canvas,
            image = self.delete_img,
            borderwidth = 0,
            highlightthickness = 0,
            command= lambda: self.delete_action(index_number),
            relief = "flat"
            )   
            self.deletebutton.place(x = 290, y = 349, width = 122, height = 56)

    def callback(self,selection):            
        self.selected_time_measure = selection 

    def is_type_int(self,*args):
        item = self.time.get()
        try:
            item_type = type(int(item))
            if item_type == type(int(1)):
                return
        except:
            self.entry_time.delete(0, 'end')

    def save_parameters(self,index):  
        try:                
            selected = self.selected_time_measure.get()
        except:               
            selected = self.selected_time_measure           
        if index == "Null":                      
            if selected == "Segundos":
                save(f"sleep({int(self.entry_time.get())})", "Null", f"{self.entry_time.get()} SEGUNDOS")
                self.window.quit()  
                self.window.destroy()  
            elif selected == "Minutos":
                formated = int(self.entry_time.get())*60
                print(formated)
                save(f"sleep({formated})","Null", f"{self.entry_time.get()} MINUTOS")
                self.window.quit()  
                self.window.destroy()
            elif selected == "Horas":
                formated = int(self.entry_time.get())*60*60
                save(f"sleep({formated})","Null", f"{self.entry_time.get()} HORAS")
                self.window.quit()  
                self.window.destroy()
            else:
                self.select_time_measure.focus_set()
                messagebox.showwarning("ERRO", "Campo 'Botão' obrigatório")
        else:        
            if selected == "Segundos":
                steps.pop(int(index))
                save(f"sleep({int(self.entry_time.get())})", index, f"{self.entry_time.get()} SEGUNDOS")
                self.window.quit()  
                self.window.destroy()  
            elif selected == "Minutos":
                steps.pop(int(index))
                save(f"sleep({int(self.entry_time.get())*60})",index, f"{self.entry_time.get()} MINUTOS")
                self.window.quit()  
                self.window.destroy()
            elif selected == "Horas":
                steps.pop(int(index))
                save(f"sleep({int(self.entry_time.get())*60*60})",index, f"{self.entry_time.get()} HORAS")
                self.window.quit()  
                self.window.destroy()
            else:
                self.select_time_measure.focus_set()
                messagebox.showwarning("ERRO", "Campo 'Botão' obrigatório")


    def delete_action(self,index_number):
        steps.pop(int(index_number))  
        save(f"delete",index_number,"del")
        self.window.quit()  
        self.window.destroy()
            

    def main(self):
        self.time.trace("w", self.is_type_int)
        self.window.resizable(False, False)
        self.window.mainloop()





