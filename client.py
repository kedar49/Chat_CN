import socket
import threading
# import time
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, Scrollbar, Text
# import os
# import traceback


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#1FA8CF'
WHITE = "white"
FONT = ("Helvetica", 16, "bold")
BUTTON_FONT = ("Aptos", 17)
SMALL_FONT = ("Helvetica", 13)
ICON_FONT = ("Helvetica", 22, "bold")
FILE_FONT = ("Helvetica", 18, "bold")
EXIT_FONT = ("Helvetica", 20)

uzer = "-"
email = ""
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver = ""
current_chat = ""
messages_box = dict()
buttons = []

def add_message(message, target, is_server=False, sent_by_me=False):
    target = target.strip()
    sender, message = message.split(":")
    try:
        messages_box[current_chat].config(state=tk.NORMAL)
        if is_server:
            messages_box[target].insert(tk.END, message + "\n", 'server')
        elif sent_by_me:
            messages_box[target].insert(tk.END, message + "\n", 'sent_by_me')
        elif sender != "all":
            if target == sender:
                messages_box[target].insert(tk.END, message + "\n")
            else:
                messages_box[sender].config(state=tk.NORMAL)
                messages_box[sender].insert(tk.END, sender + " ➡️ " + message + "\n", 'sent_by_others')
                messages_box[sender].config(state=tk.DISABLED)
        messages_box[target].config(state=tk.DISABLED)
    except:
        pass


def connect():
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
    except:
        pass#messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST}:{PORT}")

    uzer = username.get()

    global email
    email = username.get()

    if uzer != '':
        client.sendall(uzer.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")


    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()


def send_message(event=None):
    message = message_textbox.get()
    if message != '':
        message_textbox.delete(0, len(message))
        message = f"{receiver}:{message}"
        add_message(message, receiver)
        client.sendall(message.encode())
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")


def exit_application():
    try:
        client.sendall('exit'.encode('ascii'))
        print("exit message Sent")# Send exit message to the server
    except Exception as e:
        print(f"Error sending exit message to server: {e}")
    root.destroy()


def listen_for_messages_from_server(client):
    while True:
        data = client.recv(4096)
        if data:
            message = data.decode('utf-8')
            username, target, content = message.split(":")
            add_message(f"{username}:{content}", target.strip(), sent_by_me=(username.strip() == email))

        else:
            messagebox.showerror("Error", "Message received from server is empty")


def top_label(master, text, bgColor, fgColor, width):
    frame = tk.Frame(master, width=width, height=30, bg=bgColor, )
    frame.place(x=0, y=0)
    tk.Label(frame, text=text, font=("Helvetica", 15, "bold"), bg=bgColor, fg=fgColor).place(x=50, y=0)

    tk.Button(frame, text="❌", font=("Helvetica", 12, "bold"), command=frame.destroy, bg=bgColor, fg=fgColor,
              border=0).place(x=width - 30, y=0)


def login():
    users = []
    try:
        with open("./users.csv", "r") as data:
            datas = data.read().split("\n")
            for d in datas:
                users.append(d)
        data.close()
    except:
        data = open("./users.csv", "w")
        data.close()

    if username.get() == "" or password.get() =="":
        top_label(rt, "Username/ Password cannot be empty", "red", "white", 500)
        return 0

    for user in users:
        try:
            if f"{username.get()}, {password.get()}" in user:
                global uzer
                uzer = user.split(", ")[0] + " " + user.split(", ")[1]
                connect()
                rt.destroy()
                break
        except:
            continue

    else:
        top_label(rt, "Invalid username password", "red", "white", 500)


def clear_chat():
    # x.destroy()
    # messages_box[current_chat].pack
    # messages_box[current_chat].pack
    messages_box[current_chat] = Text(canvas, font=SMALL_FONT, bg="#566573", fg=WHITE, width=53, height=30)
    messages_box[current_chat].config(state=tk.DISABLED)
    messages_box[current_chat].place(x=0, y=0)


class Button:
    def __init__(self, master, name, target):
        self.button = tk.Button(master, text=name, font=("Helvetica", 12, "bold"), command=self.click,  bg="white", fg="black", border=1, width=20, height=2, justify="left")
        self.target = target

    def click(self):
        message_textbox.pack(side=tk.LEFT, padx=2, pady=2)
        message_button.pack(side=tk.LEFT, padx=2, pady=2)
        ind = buttons.index(self)
        indicator1.place(x=205, y=(80+(ind*55)))
        indicator2.place(x=0, y=(80+(ind*55)))

        global receiver
        receiver = self.target


        users = []
        with open("./users.csv", "r") as data:
            datas = data.read().split("\n")
            for d in datas:
                if uzer not in d:
                    users.append(d.split(", "))
        data.close()

        global current_chat

        if receiver == 'all':
            messages_box["all"].place(x=0, y=0)
            current_chat = "all"
            for i, e in messages_box.items():
                if (i != email) and (i != "all"):
                    e.place(x=500, y=0)
        else:
            for i, e in enumerate(users):
                try:
                    if receiver == e[2]:
                        messages_box[e[2]].place(x=0, y=0)
                        current_chat = receiver

                    else:
                        messages_box[e[2]].place(x=500, y=0)
                except:
                    pass

    def pack(self):
        self.button.pack(side=tk.TOP, pady=2)

def load_users():
    users = []
    with open("./users.csv", "r") as data:
        datas = data.read().split("\n")
        for d in datas:
            users.append(d.split(", "))
    data.close()
    buttons.append(Button(middle_frame1, "Broadcast", "all"))
    for i, e in enumerate(users):
        try:
            if uzer != e[0] + " " + e[1]:
                buttons.append(Button(middle_frame1, e[0] + " " + e[1], e[2]))
                messages_box[e[2]] = Text(canvas, font=SMALL_FONT, bg=f"#566573", fg=WHITE, width=53, height=30)
        except:
            pass

    for bt in buttons:
        bt.pack()


def signin():
    sr = tk.Tk()
    sr.geometry("500x350")
    sr.resizable(False, False)

    tk.Label(sr, text="First Name", font=FONT, ).place(x=50, y=50)
    tk.Label(sr, text="Last Name", font=FONT, ).place(x=50, y=110)
    tk.Label(sr, text="Email", font=FONT, ).place(x=50, y=170)
    tk.Label(sr, text="Password", font=FONT, ).place(x=50, y=230)

    firstname = tk.Entry(sr, width=20, font=FONT)
    firstname.place(x=200, y=50)

    lastname = tk.Entry(sr, width=20, font=FONT)
    lastname.place(x=200, y=110)

    email = tk.Entry(sr, width=20, font=FONT)
    email.place(x=200, y=170)

    signin_password = tk.Entry(sr, width=20, font=FONT)
    signin_password.place(x=200, y=230)

    def save_user():
        if firstname.get() == "" or lastname.get() == "" or email.get() == "" or signin_password == "":
            top_label(sr, "Please fill all data", "red", "white", 500)
            return 0
        file = open("users.csv", "a")
        file.write(f"\n{firstname.get()}, {lastname.get()}, {email.get()}, {signin_password.get()}")
        file.close()
        top_label(rt, "Signin Successful", "green", "white", 500)
        sr.destroy()

    tk.Button(sr, text="Signin", width=10, bg="green", border=0, fg="white", font=BUTTON_FONT, command=save_user).place(
        x=200, y=280)
    sr.mainloop()


rt = tk.Tk()
rt.geometry("500x300")
rt.resizable(False, False)

tk.Label(rt, text="Username", font=FONT, ).place(x=50, y=50)
tk.Label(rt, text="Password", font=FONT, ).place(x=50, y=110)

username = tk.Entry(rt, width=20, font=FONT)
username.place(x=200, y=50)

password = tk.Entry(rt, width=20, font=FONT)
password.place(x=200, y=110)

tk.Button(rt, text="Login", width=10, bg="green", border=0, fg="white", font=BUTTON_FONT, command=login).place(x=200, y=160)
tk.Button(rt, text="Signin", width=10, bg="red", border=0, fg="white", font=BUTTON_FONT, command=signin).place(x=200, y=210)


while uzer == "-":
    rt.mainloop()

root = tk.Tk()
root.geometry("630x550")
root.title("Messenger Client")
root.resizable(False, False)

main_frame = tk.Frame(root, width=600, height=600, bg="#17202A")
main_frame.grid(row=0, column=0)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=3)

main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=4)
main_frame.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(main_frame, width=450, height=75, bg="white")
top_frame.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=2, pady=2)

middle_frame1 = tk.Frame(main_frame, width=150, height=400, bg="white")
middle_frame1.grid(row=1, column=0, rowspan=2, sticky=tk.NSEW, padx=2, pady=2)

middle_frame2 = tk.Frame(main_frame, width=450, height=400, bg="white")
middle_frame2.grid(row=1, column=1, sticky=tk.NSEW, padx=2, pady=2)

bottom_frame = tk.Frame(main_frame, width=450, height=100, bg="#17202A", )
bottom_frame.grid(row=2, column=1, sticky=tk.NSEW, padx=2, pady=2)

username_label = tk.Label(top_frame, text=f"Welcome {uzer}!", font=("Aptos ExtraBold", 20), bg="white", fg="#17202A")
username_label.place(x=0, y=12)

# delete_button = tk.Button(top_frame, text="🗑", font=EXIT_FONT, bg="#C70039", fg="white", command=clear_chat,height=1, border=0)
# delete_button.place(x=500, y=12)

exit_button = tk.Button(top_frame, text="🏃", font=EXIT_FONT, bg="#FA7070", fg="#000000", command=exit_application,height=1, border=0)
exit_button.place(x=570, y=12)

message_textbox = tk.Entry(bottom_frame, font=BUTTON_FONT, bg="white", fg="#17202A", width=30)
message_button = tk.Button(bottom_frame, text=" ➡️", font=("Aptos", 15, "bold"), bg="white", fg="#17202A", command=send_message, width=3, border=0)

message_textbox.bind("<Return>", send_message)

canvas = tk.Canvas(middle_frame2, width=550, height=415, bg='white')
canvas.pack(expand=True, fill='both')

messages_box["all"] = Text(canvas, font=SMALL_FONT, bg="#566573", fg=WHITE, width=53, height=30)
messages_box["all"].place(x=0, y=0)

indicator1 = tk.Label(root, bg="red", height=3)
indicator2 = tk.Label(root, bg="red", height=3)

load_users()

if uzer != "-" and len(uzer) > 2:
    root.mainloop()
