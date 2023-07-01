import PySimpleGUI as sg
import socket, threading, sys, os, base64
from cryptography.fernet import Fernet

def help_win():
    layout = [[sg.Text(open(f"{os.environ['PSCPath']}\\HELP.TXT", "r").read())]]
    Tabs = [
        [sg.TabGroup([[sg.Tab("Version", [[sg.Text("Version 1.0.0")]]), sg.Tab("Help", layout)]],(0,0))],
    ]
    windowh = sg.Window("Help", Tabs, size=(545, 250))
    
    while True:
        event, value = windowh.read()
        if event == sg.WIN_CLOSED:
            windowh.close()
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("127.0.0.1", 808))

messages = []

layout = [
    [sg.Listbox(messages, size=(25,10), key="--LISTBOX--")],
    [sg.Input(size=(55,20), key="--INPUTMESSAGE--")],
    [sg.Button("Send", key="--SEND--"), sg.Button("Close", key="--CLOSE--"),sg.Button("Help", key="--HELP--")],
]


window = sg.Window("Hello World", layout, size=(400,300), finalize=True)

nickname = sg.popup_get_text("Entry your nickname: ", "Chatroom", size=(100,200))
server.send(nickname.encode("utf-8"))

recv_stop = False
def receive():
    while True:
        msg = Fernet(base64.urlsafe_b64encode(b"AnonymousKeyAnonymousKey12345678")).decrypt(server.recv(1024)).decode("utf-8")
        messages.append(msg)
        if recv_stop == True:
            break
        else:
            window["--LISTBOX--"].update(messages)

recv_thrd = threading.Thread(target=receive)
recv_thrd.start()


while True:
    event, value = window.read()
    if event == "--SEND--":
        if not value["--INPUTMESSAGE--"] == ":exit":
            server.send(value["--INPUTMESSAGE--"].encode("utf-8"))
            window["--INPUTMESSAGE--"].update("")
        else:
            server.send(value["--INPUTMESSAGE--"].encode("utf-8"))
            recv_stop = True
            window.close()
            sys.exit()
    if event == "--HELP--":
        help_win()
    if event == "--CLOSE--":
        recv_stop = True
        window.close()
        server.send(":exit".encode("utf-8"))
        sys.exit()