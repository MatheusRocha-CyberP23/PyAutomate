import os, time, pyautogui
from tkinter import *
from tkinter import ttk

#Abaixo é a importação dos modulos de criar projeto, e executar a aplicação principal
from CreateProject import CreateProject
from MainWindow import MainWindow
from resizer import resize, resize_img


class HomePage:
    def __init__(self, window):
        screen_width, screen_height = pyautogui.size()
        #CONSTANTES ONDE É OBTIDO O CAMINHO DOS PROJETOS CRIADOS E IMAGENS
        self.imgs_path = (os.path.dirname(os.path.realpath(__file__)) + "/Imgs/HomePage/")
        self.projects_path = os.path.dirname(os.path.realpath(__file__)) + "/Projects"
        self.count = 0
        self.window = window        
        self.window.state('zoomed')
        self.window.title("PyAutomate")
        self.window.geometry(f"{screen_width}x{screen_height}")
        self.window.iconbitmap(os.path.join(self.imgs_path, "ico.ico"))
        self.window.configure(bg="#ffffff")

        self.canvas = Canvas(
            self.window,
            bg="#ffffff",
            height=screen_height,
            width=screen_width,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)
      
        
        self.background_img = PhotoImage(
            data=resize_img(os.path.join(self.imgs_path, "background.png"))
        )
        self.background = self.canvas.create_image(
            resize('width',961.5), resize('height',501.5), image=self.background_img
        )

        self.new_project_img = PhotoImage(
            data=resize_img(os.path.join(self.imgs_path, "newProject.png"))
        )
        self.new_project_button = Button(
            image=self.new_project_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.create_new_project,
            relief="flat",
        )
        self.new_project_button.place(
            x=int(resize('width',1264)), y=int(resize('height',292)), width=int(resize('width',223)), height=int(resize('height',56))
        )

        self.project_img = PhotoImage(
            data=resize_img(os.path.join(self.imgs_path, "project.png"))
        )

        self.start_frame = Frame(
            self.window,
            width=int(resize('width',1090)),
            height=int(resize('height',520)),
            highlightthickness=0,
        )
        self.start_frame.place(x=int(resize('width',427)),y=int(resize('height',420)))
        self.text_img = Text(
            self.start_frame,
            height=int(resize('height',30)),
            width=int(resize('width',130)),
            highlightthickness=0,
            borderwidth=0,
            bg="#FBFBFB",
        )
        self.text_img.tag_configure("tag_name", justify="center")
        self.text_img.pack(side=LEFT)
        self.scrollbar = ttk.Scrollbar(
            self.start_frame,
            command=self.text_img.yview,
            orient=VERTICAL,
        )
        self.scrollbar.pack(side=LEFT, fill=Y)
        self.text_img.configure(yscrollcommand=self.scrollbar.set)
        self.text_img.configure(state="disabled")
        self.text_img.config(cursor="arrow")
        self.names = []

    def update(self):
        self.text_img.configure(state="normal")
        self.text_img.delete("1.0", "end")
        self.text_img.configure(state="disabled")        
        for path in os.listdir(self.projects_path):
            if os.path.isfile(os.path.join(self.projects_path, path)):
                if (
                    path.endswith(".txt")
                    and not os.path.splitext(path)[0].endswith("T")
                    and not os.path.splitext(path)[0].endswith("TT")
                ):
                    self.names.append(os.path.splitext(path)[0])
       
            #long_name = max(self.names, key=len)
        
            long_name = 15

        for path in os.listdir(self.projects_path):
            if os.path.isfile(os.path.join(self.projects_path, path)):
                if (
                    path.endswith(".txt")
                    and not os.path.splitext(path)[0].endswith("T")
                    and not os.path.splitext(path)[0].endswith("TT")
                ):                   
                    ti_m = os.path.getmtime(
                        os.path.join(self.projects_path, path)
                    )
                    m_ti = time.ctime(ti_m)
                    t_obj = time.strptime(m_ti)
                    t_stamp = time.strftime("%Y/%m/%d", t_obj)
                    self.text_img.configure(state="normal") 
                    var = ((long_name)-len(os.path.splitext(path)[0]))                                                                           
                    btn = Button(
                        self.text_img,
                        image=self.project_img,
                        borderwidth=0,
                        highlightthickness=0,
                        relief="flat",
                        compound="center",
                        justify=CENTER,                        
                        text=os.path.splitext(path)[0].upper() + "⠀"*(var) + "⠀"*17 + f"{t_stamp}" + "⠀"*40,
                        fg="#000",
                        font=("Helvetica", int(resize('height',12))),
                        command=lambda text=os.path.splitext(path)[0]: self.open_project(
                            text
                        )
                    )                 
                    self.text_img.window_create("end",window=btn)
                    self.text_img.insert('end', "\n")
                    self.text_img.configure(state="disabled")
                    self.count += 1

    def create_new_project(self):
        create = CreateProject(window)
        create.main()
        self.window.quit()
        self.window.destroy()
        main = MainWindow(create.return_name())
        main.main()

    def open_project(self, text):
        self.window.quit()
        self.window.destroy()
        main = MainWindow(text)
        main.main()
    

window = Tk()
homepage = HomePage(window)
homepage.update()

window.mainloop()