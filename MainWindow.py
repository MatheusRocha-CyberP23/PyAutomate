#Bibliotecas 
import tempfile,os,sys,pyautogui
from tkinter import *
from Functions.Save import return_action_name, steps
from Functions.OpenBrowser import OpenBrowserAction
from Functions.MouseClick import MouseClickAction
from Functions.Keyboard import KeyboardAction
from Functions.Wait import WaitAction
from Functions.Compiler import executar
from time import sleep
import tkinter as TKINTER
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
from threading import Thread
from functools import partial
from resizer import resize, resize_img

IMGS_PATH = (os.path.dirname(os.path.realpath(__file__))) + '/IMGS/MainWindow/'

#Variaveis Globais
ALL_ACTIONS = [" > Aguardar", " > Sistema", " > Teclado e Mouse"]
ACTIONS = ["          Abrir Navegador "]
ACTIONS_WAIT = ["          Aguardar "]
ACTIONS_KEYBOARD = ["          Inserir teclas ", "          Mouse Click "]
SELECTED_ACTIONS = []
CREATED_ACTIONS_PARAMETERS = []
CREATED_ACTIONS_NAME = []




class MainWindow:
    def __init__(self, window):
        self.screen_width, self.screen_height = pyautogui.size()
        print(pyautogui.size())
        self.window = Tk()
        self.FINISH = False
        self.UPTODATE = False
        self.dragging = False
        self.actual_process = 0
        self.ACTION_BUTTON_IMG = PhotoImage(data = resize_img(os.path.join(IMGS_PATH, "actionButton.png")))
        self.ACTIVE_ACTION_BUTTON = PhotoImage(data = resize_img(os.path.join(IMGS_PATH, "activeAction.png")))
        self.END_BUTTON_IMG = PhotoImage(data = resize_img(os.path.join(IMGS_PATH, "actionButtonEND.png")))
        self.actionbuttons = []
        self.labelbutton = []
        
        self.window_name = window
        self.window.geometry(f"{self.screen_width}x{self.screen_height}")
        self.window.state('zoomed')
        self.window.iconbitmap(os.path.join(IMGS_PATH, "ico.ico"))
        self.window.configure(bg="#ffffff")
        self.window.title(window)

        self.canvas = Canvas(
            self.window,
            bg = "#dceaff",
            height = int(resize('height',1080)),
            width = int(resize('width',1920)),
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)

        self.background_img = PhotoImage(data = resize_img(os.path.join(IMGS_PATH, "background.png")))
        self.background = self.canvas.create_image(
            resize('width',910.0), resize('height',517.0),
            image=self.background_img
        )

        self.status = self.canvas.create_text(
            resize('width',560.0), resize('height',768),
            text = "",
            fill = "#000000",
            font = ("Inter-Light", int(resize('height',16.0)))
        )

        self.searchbox_img = PhotoImage(data = resize_img(os.path.join(IMGS_PATH, "img_textBox0.png")))
        self.searchbox_bg  = self.canvas.create_image(
            resize('width',143.5), resize('height',165.0),
            image = self.searchbox_img
        )

        self.searchbox = Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0
        )
        self.searchbox.place(x =  resize('width',42.0), y =  resize('height',145), width = resize('width',150.0), height = resize('height',40))

        self.search_button_img = PhotoImage(data = resize_img(os.path.join(IMGS_PATH, "searchButton.png")))
        self.search_button = Button(
            image = self.search_button_img,
            borderwidth = 0,
            highlightthickness = 0,
            relief = "flat"
        )
        self.search_button.place(x = int(resize('width',208)), y = int(resize('height',150)), width = int(resize('width',35)), height = int(resize('height',31)))
        self.search_button.configure(command=self.aplicar_filtro)

        self.save_img = PhotoImage(data = resize_img(os.path.join(IMGS_PATH,"saveButton.png"))) 
        self.save_button = Button(
            image = self.save_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.save_project,
            relief = "flat"
        )
        self.save_button.place(x = int(resize('width',562)), y = int(resize('height',22)), width = int(resize('width',60)), height = int(resize('height',58)))

        self.playbutton_img = PhotoImage(data = resize_img(os.path.join(IMGS_PATH, "playButton.png")))
        self.playbutton = Button(
            image = self.playbutton_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.run,
            relief = "flat"
        )
        self.playbutton.place(x = int(resize('width',419)), y = int(resize('height',22)), width = int(resize('width',60)), height = int(resize('height',58)))        

        self.stopbutton_img = PhotoImage(data = resize_img(os.path.join(IMGS_PATH, "stopButton.png")))
        self.stopbutton = Button(
            image = self.stopbutton_img,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.stop,
            state=DISABLED,
            relief = "flat"
        )
        self.stopbutton.place(x =  int(resize('width',488)), y = int(resize('height',22)), width = int(resize('width',65)), height = int(resize('height',58)))

        self.pausebutton_img = PhotoImage(data = resize_img(os.path.join(IMGS_PATH, "pauseButton.png")))
        self.pausebutton = Button(
                    image = self.pausebutton_img,
                    borderwidth = 0,
                    highlightthickness = 0,
                    command = self.pause,
                    relief = "flat",state=DISABLED
        )
        self.pausebutton.place(x = int(resize('width',419)), y = int(resize('height',22)), width = int(resize('width',60)), height = int(resize('height',58)))
        self.playbutton.tkraise()
        self.actions_frame = Frame(self.window)
        self.actions_frame.place(x = resize('width',18.1), y = resize('height',270),width = resize('width',251.46), height = resize('height',680))

        self.scrollbar_actions = ttk.Scrollbar(self.actions_frame, orient= VERTICAL)

        self.actions_list = Listbox(
            self.actions_frame,
            width=int(resize('width',251)),
            height=int(resize('height',720)), 
            yscrollcommand= self.scrollbar_actions.set,
            font=('Inter',int(resize('height',17))),
            borderwidth=0,
            highlightthickness=0,
            selectbackground="#cbcccd", 
            selectforeground="black",
            selectmode='single',
            activestyle='none'
        )        

        self.actions_list.insert(0,
            " > Aguardar",
            " > Sistema", 
            " > Teclado e Mouse"
        )

        self.scrollbar_actions.config(command=self.actions_list.yview)
        self.scrollbar_actions.pack(side=RIGHT, fill=Y)
        self.actions_list.pack()        
        self.actions_list.bind("<<ListboxSelect>>", self.action_clicked)

        self.actionsbuttons_frame_container = Frame(self.window)    
        self.actionsbuttons_canvas_container = Canvas(
            self.actionsbuttons_frame_container, 
            height=int(resize('height',500)), 
            width=int(resize('width',1200)),
            background="#FFF"
        )

        self.actionsbuttons_scrollbar = ttk.Scrollbar(
            self.actionsbuttons_frame_container,
            orient= VERTICAL,
            command= self.actionsbuttons_canvas_container.yview, style='Vertical.TScrollbar'
        )

        self.actionsbuttons_frame_container_2 = Frame(self.actionsbuttons_frame_container)

        self.actionsbuttons_canvas_container.create_window((0, 0), window=self.actionsbuttons_frame_container_2, anchor='nw')
        self.actionsbuttons_canvas_container.configure(yscrollcommand=self.actionsbuttons_scrollbar.set,scrollregion="0 0 0 %s" % self.actionsbuttons_frame_container_2.winfo_height(),yscrollincrement='1m')
        self.actionsbuttons_canvas_container.pack(side=LEFT)
        self.actionsbuttons_scrollbar.pack(side=RIGHT, fill = Y)
        self.actionsbuttons_frame_container.place(x=int(resize('width',435)),y=int(resize('height',120)))

 
        

    def open_project(self):
        count = 0
        #Abre os arquivos de determinado projeto com os dados salvos 
        with open(f"projects/{self.window_name}TT.txt", "r") as project_action_parameters:       
            text = project_action_parameters.readlines()
             
        with open(f"projects/{self.window_name}.txt", "r") as project_steps:
            #Cada linha de código salva nos arquivos é lida e armazenada na lista "steps", para execução do código ao apertar o botão play
            for i in project_steps.readlines():                     
                steps.append(i)

        with open(f"projects/{self.window_name}T.txt", "r") as project_action_name:
            #Cada linha de texto salva nos arquivos é lida e armazenada na lista "CreatedActions" e "CreatedActionsName", para criação e atualização dos botões das ações
            for i in project_action_name.readlines():                
                CREATED_ACTIONS_NAME.append(i)
                CREATED_ACTIONS_PARAMETERS.append(text[count])
                self.create_actionbutton('\n'+i, text[count])
                count=count+1

       
    def save_project(self):     
        #Abre os arquivos de texto com o nome do projeto, e salva os códigos como o texto
        with open((os.path.dirname(os.path.realpath(__file__))) + f"/projects/{self.window_name}.txt", "w") as save_actions: 
            save_actions.writelines(steps) 

        with open((os.path.dirname(os.path.realpath(__file__))) + f"/projects/{self.window_name}T.txt", "w") as save_actions_name:
            save_actions_name.writelines(CREATED_ACTIONS_NAME) 

        with open((os.path.dirname(os.path.realpath(__file__))) + f"/projects/{self.window_name}TT.txt", "w") as save_actions_parameters:                  
            save_actions_parameters.writelines(CREATED_ACTIONS_PARAMETERS)  
        
        
    def action_clicked(self,event):
        #Função que pega o index do 'gatilho' pressionado, e acrescenta as funções disponiveis, dando impressão de dropdown
        selection = event.widget.curselection()
        if selection:
            selected_action_name = self.actions_list.get(ANCHOR)
            if selected_action_name == " > Sistema":  
                if "sistema" in SELECTED_ACTIONS:
                    selected_action = self.actions_list.index(ANCHOR)
                    for action in ACTIONS:
                        self.actions_list.delete(selected_action+1)
                        SELECTED_ACTIONS.remove('sistema')
                else:            
                    SELECTED_ACTIONS.append('sistema')          
                    selected_action = self.actions_list.index(ANCHOR)
                    for action in ACTIONS:
                        self.actions_list.insert(selected_action+1,action)

            if selected_action_name == " > Aguardar":  
                if "aguardar" in SELECTED_ACTIONS:
                    selected_action = self.actions_list.index(ANCHOR)
                    for action in ACTIONS_WAIT:
                        self.actions_list.delete(selected_action+1)
                        SELECTED_ACTIONS.remove('aguardar')
                else:            
                    SELECTED_ACTIONS.append('aguardar')          
                    selected_action = self.actions_list.index(ANCHOR)
                    for action in ACTIONS_WAIT:
                        self.actions_list.insert(selected_action+1,action)

            if selected_action_name == " > Teclado e Mouse":  
                if "teclado" in SELECTED_ACTIONS:
                    selected_action = self.actions_list.index(ANCHOR)
                    for action in ACTIONS_KEYBOARD:
                        self.actions_list.delete(selected_action+1)
                    SELECTED_ACTIONS.remove('teclado')
                else:            
                    SELECTED_ACTIONS.append('teclado')          
                    selected_action = self.actions_list.index(ANCHOR)
                    for action in ACTIONS_KEYBOARD:
                        self.actions_list.insert(selected_action+1,action)
                        
            if selected_action_name == "          Abrir Navegador ":                                  
                    OpenBrowserAction(self.window,"Null","") 
                    CREATED_ACTIONS_NAME.append("ABRIR NAVEGADOR\n") 
                    CREATED_ACTIONS_PARAMETERS.append(return_action_name()+"\n")                                                                      
                    self.create_actionbutton("ABRIR NAVEGADOR\n", return_action_name())
                
            if selected_action_name == "          Mouse Click ":                                                    
                    MouseClickAction(self.window,"Null","").main()                      
                    CREATED_ACTIONS_NAME.append("CLICAR COM O MOUSE\n")  
                    CREATED_ACTIONS_PARAMETERS.append(return_action_name()+"\n")                                  
                    self.create_actionbutton("CLICAR COM O MOUSE\n", return_action_name())
                   
            if selected_action_name == "          Aguardar ":                                                    
                    WaitAction(self.window,"Null","").main()     
                    CREATED_ACTIONS_NAME.append("AGUARDAR\n") 
                    CREATED_ACTIONS_PARAMETERS.append(return_action_name()+"\n")                               
                    self.create_actionbutton("AGUARDAR\n", return_action_name())
             
            if selected_action_name == "          Inserir teclas ":                                   
                    KeyboardAction(self.window,"Null","")        
                    CREATED_ACTIONS_NAME.append("INSERIR TECLAS\n")   
                    CREATED_ACTIONS_PARAMETERS.append(return_action_name()+"\n")                       
                    self.create_actionbutton("INSERIR TECLAS\n", return_action_name())

    def run_code(self):
        items = len(steps)
        for i in range(self.actual_process, items):
            if self.running == True:    
                self.actualIN = i      
                self.actual_process = i+1     
                self.UPTODATE = True                             
                executar(steps[i])                                    
                for i in range(30):
                    try:
                        if self.running == True:
                            sleep(0.01)       
                    except:        
                        pass                                   
            else:            
                break  
            if self.actual_process == items:
                self.FINISH = True
    
    def update(self):
        if self.UPTODATE == True:               
            self.actionbuttons[self.actualIN].configure(image = self.ACTIVE_ACTION_BUTTON)         
            if self.actualIN > 0:                             
                self.actionbuttons[self.actualIN-1].configure(image = self.ACTION_BUTTON_IMG)
                self.window.after(1, self.update)                                 
            else:
                self.window.after(1, self.update)            
            self.UPTODATE = False         
        else:
            self.window.after(1, self.update) 

    def finished(self):
        if self.FINISH == True:
            self.FINISH = False           
            self.actual_process = 0   
            for button in self.actionbuttons:         
                button.bind("<Button-1>", partial(self.on_button_dragging_start, action_btn_event=button))
                button.bind("<ButtonRelease-1>", partial(self.on_button_dragging_end, action_button_event=button))
            self.actionbuttons[self.actualIN].configure(image = self.ACTION_BUTTON_IMG)
            self.actions_list.configure(state="normal")
            self.pause() 
            self.stopbutton.config(state=DISABLED)
        else:
            self.window.after(1, self.finished) 

    def run(self):
        if len(steps) < 1:
            return 
        else:            
            self.running = True
            self.stopbutton.config(state=NORMAL)
            self.playbutton.config(state=DISABLED)
            self.pausebutton.config(state=NORMAL)
            self.pausebutton.tkraise()
            t1=Thread(target= self.run_code)
            for button in self.actionbuttons:       
                button.unbind("<Button-1>")
                button.unbind("<ButtonRelease-1>") 
            self.actions_list.configure(state="disabled")
            self.canvas.itemconfig(self.status, text="RODANDO", fill = "#03fc3d")
            t1.start()
            self.window.after(1, self.finished)
            self.window.after(1, self.update)  

    def pause(self):    
        self.canvas.itemconfig(self.status, text="PAUSADO", fill = "#fc0303")
        self.running = False
        self.playbutton.config(state=NORMAL)
        self.stopbutton.config(state=NORMAL)    
        self.pausebutton.config(state=DISABLED)
        self.playbutton.tkraise() 

    def stop(self):    
        self.running = False
        self.FINISH = True
        self.playbutton.config(state=NORMAL)
        self.stopbutton.config(state=DISABLED)
        self.pausebutton.config(state=DISABLED)
        self.actions_list.configure(state="normal")
        for button in self.actionbuttons:
            button.bind("<Button-1>", partial(self.on_button_dragging_start, action_btn_event=button))  
            button.bind("<ButtonRelease-1>", partial(self.on_button_dragging_end, action_button_event=button)) 
        self.playbutton.tkraise()

                                   

    def create_actionbutton(self,action_name,action_parameter): 
        if len(self.actionbuttons) < 1:     
            self.action_button = Label(
                self.actionsbuttons_frame_container_2, 
                text=f"{action_name}{action_parameter}\n",
                image=self.END_BUTTON_IMG, 
                justify=CENTER, 
                compound='center', 
                font=('Inter',int(resize('height',15))), 
                fg="#fff", 
                borderwidth=0, 
                highlightthickness=0, 
                relief="flat"
            )                                         
        else:
            self.action_button = Button(
                    self.actionsbuttons_frame_container_2, 
                    text=f"{action_name}{action_parameter}\n", 
                    image=self.ACTION_BUTTON_IMG, 
                    justify=CENTER, 
                    compound='center', 
                    font=('Inter',int(resize('height',15))), 
                    fg="#fff", 
                    borderwidth=0, 
                    highlightthickness=0, 
                    relief="flat"
                )             
            self.action_button.bind("<Button-1>", partial(self.on_button_dragging_start, action_btn_event=self.action_button))              
            self.action_button.bind("<ButtonRelease-1>", partial(self.on_button_dragging_end, action_button_event=self.action_button)) 

        self.action_button.pack() 
        self.actionbuttons.append(self.action_button)                                                             
        if len(self.actionbuttons) <= 1:
            self.labelbutton.append(self.action_button)
        else:           
            self.labelbutton[0].pack_forget()
            self.actionbuttons.remove(self.labelbutton[0])
            for button in self.actionbuttons:
                button.pack_forget()
                button.pack()
            self.actionbuttons.append(self.labelbutton[0])
            self.labelbutton[0].pack()
        self.actionsbuttons_frame_container_2.update() 
        self.actionsbuttons_canvas_container.configure(yscrollcommand=self.actionsbuttons_scrollbar.set, scrollregion="0 0 0 %s" % self.actionsbuttons_frame_container_2.winfo_height())

    def on_button_dragging_start(self,event,action_btn_event):
        if action_btn_event == self.actionbuttons[-1]:            
            return None
        else:                
            self.start_pos_y = event.y                    
            action_btn_event.lift()          
            action_btn_event.unbind("<B1-Motion>")
            self.action_button_posistion = True                 
            for i, item in enumerate(self.actionbuttons):
                if item == action_btn_event:                    
                    self.button_index_number = i     
                    self.removed_step = steps.pop(i)
                    self.removed_action_name = CREATED_ACTIONS_NAME.pop(i)
                    self.removed_action_parameter = CREATED_ACTIONS_PARAMETERS.pop(i)           
                    break                            
            
           
            def start_dragging():                                        
                action_btn_event.bind("<B1-Motion>", partial(self.on_button_dragging, action_button_event = action_btn_event))
            self.aa = self.actionsbuttons_frame_container_2.winfo_height()/ self.actionsbuttons_scrollbar.get()[1]              
            self.window.after(500, start_dragging) 

    def on_button_dragging(self,event,action_button_event):
        if action_button_event == self.actionbuttons[-1]:   
            return None
        else:
            if self.start_pos_y:         
                self.dragging = True         
                self.y = action_button_event.winfo_y() - self.start_pos_y + event.y                                                                                  
                if action_button_event.winfo_y() < (self.actionsbuttons_frame_container_2.winfo_height()):      
                    if self.actionsbuttons_frame_container_2.winfo_height() < int(resize('height',500)):                        
                        pass
                
                    for button in self.actionbuttons:      
                        if button != action_button_event:      
                            if action_button_event.winfo_y() < self.actionsbuttons_canvas_container.winfo_y()-int(resize('height',50)):                                                                                                                                             
                                return None
                                
                            if action_button_event.winfo_y() > self.actionsbuttons_frame_container_2.winfo_height()-int(resize('height',50)):                                
                                return None

                            else:                                                                                                                                                                        
                                if action_button_event.winfo_y() < button.winfo_y():
                                    action_button_event.place(y= self.y)
                                    
                                    # Remove o botão da lista e insere novamente na posição do botão que está acima
                                    self.actionbuttons.remove(action_button_event)                                                   
                                    self.actionbuttons.insert(self.actionbuttons.index(button), action_button_event)                            
                                    if self.action_button_posistion == True:                            
                                        self.action_button_index_number = self.actionbuttons.index(button)-1                        
                                    # Atualiza a posição de todos os botões
                                    for i, btn in enumerate(self.actionbuttons):                                     
                                        action_button_event.place(y= self.y)      
                                        btn.place(y= i * int(resize('height',125)))
                                                                              
                                    break
                    action_button_event.place(y= self.y) 
                else:
                    pass

    def on_button_dragging_end(self,event,action_button_event):                 
        if self.dragging == False:                        
            self.action_button_index_number = self.button_index_number                            
        if action_button_event == self.actionbuttons[-1]:     
            return None
        else:
            action_button_event.unbind("<B1-Motion>")            
            self.start_pos_y = None
            for button in self.actionbuttons:        
                if button != action_button_event:                                    
                    # Verifica se o botão foi solto acima do primeiro botão
                    if action_button_event.winfo_y() < button.winfo_y():
                        # Remove o botão da lista e insere novamente na primeira posição
                        self.actionbuttons.remove(action_button_event)                
                        self.actionbuttons.insert(self.actionbuttons.index(button), action_button_event) 
                        if self.action_button_posistion == True:                   
                            steps.insert(self.action_button_index_number,  self.removed_step)                            
                            CREATED_ACTIONS_NAME.insert(self.action_button_index_number, self.removed_action_name)
                            CREATED_ACTIONS_PARAMETERS.insert(self.action_button_index_number, self.removed_action_parameter) 
                            self.action_button_posistion = False                                     
                        # Atualiza a posição de todos os botões                        
                        for i, btn in enumerate( self.actionbuttons):                            
                            btn.place(y= i * int(resize('height',125)))                           
                        break                         
                    else:        
                        if self.action_button_posistion == True:                    
                            steps.insert(self.action_button_index_number,  self.removed_step)                            
                            CREATED_ACTIONS_NAME.insert(self.action_button_index_number, self.removed_action_name)
                            CREATED_ACTIONS_PARAMETERS.insert(self.action_button_index_number, self.removed_action_parameter) 
                            self.action_button_posistion = False                           
                        for i, btn in enumerate(self.actionbuttons):
                            btn.place(y= i * int(resize('height',125)))                                                                  
                        break 
            if self.dragging == False:   
                self.open_action(self.action_button_index_number)               
            self.dragging = False  

    
    def open_action(self,index_number):
        try:
            if CREATED_ACTIONS_NAME[index_number] == 'ABRIR NAVEGADOR\n':
                OpenBrowserAction(self.window,index_number,CREATED_ACTIONS_PARAMETERS[index_number])
                if return_action_name() == "del":
                    CREATED_ACTIONS_NAME.pop(index_number)
                    CREATED_ACTIONS_PARAMETERS.pop(index_number)                    
                    self.actionbuttons[index_number].destroy()
                    self.actionbuttons.pop(index_number)             
                    self.actionsbuttons_frame_container_2.update()
                    for i, btn in enumerate(self.actionbuttons):                            
                        btn.place(y= i * int(resize('height',125)))                           
                else:          
                    CREATED_ACTIONS_PARAMETERS.pop(index_number)
                    CREATED_ACTIONS_PARAMETERS.insert(index_number, return_action_name()+"\n")
                    self.actionbuttons[index_number].configure(text=f"{CREATED_ACTIONS_NAME[index_number]}{return_action_name()}\n")
        except:
            pass

        try:            
            if CREATED_ACTIONS_NAME[index_number] == 'INSERIR TECLAS\n':
                KeyboardAction(self.window,index_number,CREATED_ACTIONS_PARAMETERS[index_number])
                if return_action_name() == "del":
                    CREATED_ACTIONS_NAME.pop(index_number)
                    CREATED_ACTIONS_PARAMETERS.pop(index_number)                    
                    self.actionbuttons[index_number].destroy()
                    self.actionbuttons.pop(index_number)             
                    self.actionsbuttons_frame_container_2.update()
                    for i, btn in enumerate(self.actionbuttons):                            
                        btn.place(y= i * int(resize('height',125)))                           
                else:          
                    CREATED_ACTIONS_PARAMETERS.pop(index_number)
                    CREATED_ACTIONS_PARAMETERS.insert(index_number, return_action_name()+"\n")
                    self.actionbuttons[index_number].configure(text=f"{CREATED_ACTIONS_NAME[index_number]}{return_action_name()}\n")
        except:
            pass
        
        try:
            if CREATED_ACTIONS_NAME[index_number] == 'AGUARDAR\n':
                WaitAction(self.window,index_number,CREATED_ACTIONS_PARAMETERS[index_number]).main()
                if return_action_name() == "del":
                    CREATED_ACTIONS_NAME.pop(index_number)
                    CREATED_ACTIONS_PARAMETERS.pop(index_number)                    
                    self.actionbuttons[index_number].destroy()
                    self.actionbuttons.pop(index_number)             
                    self.actionsbuttons_frame_container_2.update()
                    for i, btn in enumerate(self.actionbuttons):                            
                        btn.place(y= i * int(resize('height',125)))                           
                else:          
                    CREATED_ACTIONS_PARAMETERS.pop(index_number)
                    CREATED_ACTIONS_PARAMETERS.insert(index_number, return_action_name()+"\n")
                    self.actionbuttons[index_number].configure(text=f"{CREATED_ACTIONS_NAME[index_number]}{return_action_name()}\n")
        except:
            pass

        try:           
           if CREATED_ACTIONS_NAME[index_number] == 'CLICAR COM O MOUSE\n':
                MouseClickAction(self.window,index_number,CREATED_ACTIONS_PARAMETERS[index_number]).main() 
                if return_action_name() == "del":
                    CREATED_ACTIONS_NAME.pop(index_number)
                    CREATED_ACTIONS_PARAMETERS.pop(index_number)                    
                    self.actionbuttons[index_number].destroy()
                    self.actionbuttons.pop(index_number)             
                    self.actionsbuttons_frame_container_2.update()
                    for i, btn in enumerate(self.actionbuttons):                            
                        btn.place(y= i * int(resize('height',125)))                           
                else:          
                    CREATED_ACTIONS_PARAMETERS.pop(index_number)
                    CREATED_ACTIONS_PARAMETERS.insert(index_number, return_action_name()+"\n")
                    self.actionbuttons[index_number].configure(text=f"{CREATED_ACTIONS_NAME[index_number]}{return_action_name()}\n")
        except:
            pass

    def aplicar_filtro(self):
        filtro = self.searchbox.get().lower()
        self.actions_list.delete(0, END)
        for item in ALL_ACTIONS:
            if filtro in item.lower():
                self.actions_list.insert(END, item)

    def on_closing(self):
        if messagebox.askokcancel("Confirmação", "Tem certeza de que deseja fechar a janela?\n\nCertifique-se de salvar o projeto antes de fechar,\ncaso contrário as mudanças feitas serão perdidas."):
            self.window.destroy()
            sys.exit()

    def main(self):       
        self.create_actionbutton("FIM","")  
        self.open_project()  
        
        self.window.tk.call("source", "breeze.tcl")
        style=ttk.Style()
        style.theme_use('breeze')
        self.window.resizable(True, True)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()        

       
        