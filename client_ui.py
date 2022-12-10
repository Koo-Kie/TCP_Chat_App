import customtkinter as ctk
from PIL import Image, ImageTk
import socket, threading

root = ctk.CTk()
root.geometry('1000x1000')
ctk.set_appearance_mode('system')
root.title('Chat App By Kais')
root.wm_iconbitmap('logo.ico')

chat = ctk.CTkTextbox(
    root,
    font=('Arial', 20),
    state = 'normal',
    fg_color = ["gray92", "gray14"],
    border_color = ["#979DA2", "#565B5E"],
    border_width = 5,
    width=1000,
    height=900
)
chat.grid(column=0, row=0, columnspan=2, sticky='nsew')

type = ctk.CTkEntry(
    root,
    font=('Arial', 20),
    height=80,
    placeholder_text='Message',
    width=900,
    corner_radius= 50
)
type.grid(column=0, row=1, sticky='nsew', padx=(10,5),pady=10)

def click():
    message = type.get()
    type.delete('0', 'end')
    try:    
        if len(message.strip()) == 0:
            pass
        else:
            s.send(message.encode('UTF-8'))
    except socket.error:
        connexion()

image = ctk.CTkImage(light_image=Image.open("logo.png"),dark_image=Image.open("logo.png"),size=(70, 70))

button = ctk.CTkButton(
    root,
    image=image,
    width=0,
    height=0,
    text='',
    fg_color= ["gray92", "gray14"],
    hover_color= ["gray92", "gray14"],
    command=click
)
button.grid(column=1, row=1, columnspan=2, sticky='w')

# ____________________________________________________________

def backend():
    global connexion
    ip = "127.0.0.1"
    port = 4444

    dialog = ctk.CTkInputDialog(text="Username:", title="Log In")
    username = dialog.get_input()

    def connexion():
        global s
        chat.configure(state='normal')
        chat.insert('0.0', 'Connecting...')
        s = socket.socket()
        while True:
            try:
                s.connect((ip,port))
                s.send(username.encode('UTF-8'))
                chat.insert('end','\nConnected!')
                break
            except socket.error:
                continue

    def receiver():
        try:
            while True:
                chat.insert('end','\n' + s.recv(1024).decode('UTF-8'))
        except socket.error:
            connexion()

    connexion()
    t = threading.Thread(target= receiver)
    t.start()

back = threading.Thread(target= backend)
back.start()


# ____________________________________________________________

root.mainloop()
