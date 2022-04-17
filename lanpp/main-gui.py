import pyperclip
import ftpserver
import os
import json
import sys
import socket
import webserver
import webbrowser
from tkinter import *
from tkinter import messagebox
from ttkthemes import *
from tkinter.ttk import *
from multiprocessing import Process

def getip():
     try:
         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
         s.connect(('192.168.1.1', 0))
         ip = s.getsockname()[0]
     except:
         ip = "localhost"
     finally:
         s.close()
     return ip
def jsonget(key_name):
   with  open("setting.json") as f:
        json_data = f.read()
   data = json.loads(json_data)
   f.close()
   return data[key_name]
def webserver_ui():
    if True : 
        #webserverui_status = 1
        subwindow = ThemedTk(theme="yaru", toplevel=True, themebg=True)
        subwindow.title("WebServer | LAN++ Manager")
        subwindow.geometry("850x500")
        os.chdir(static_path)
        task = Process(target=webserver.start)
        def start():
            task.start()
            print("started")
        def __close__():
            task.terminate()
            os.chdir(static_path)
            print("closed")
        def close():
            if task.is_alive()  == False:
                start()
            __close__()
            os.chdir(static_path)
            subwindow.destroy()
        def copylink():
            pyperclip.copy("http://" + str(getip())  + ":" + jsonget("webserverport"))
        ntext = "    点击按钮以控制[浏览器文件管理服务]\n    [启动] - 启动服务\n    [关闭窗口并退出] - 退出窗口(退出服务)\n    [复制访问链接] - 复制链接以便访问服务" + '当前配置:\n    端口:' + jsonget("ftpserverport") + "\n    目录: " + jsonget("webserverroot") + "\n    打开服务后请用浏览器打开此链接以操作文件: [http://" + str(getip())  + ":" + jsonget("webserverport") + "]\n"
        lbl1 = Label(subwindow, text=ntext)
        lbl1.grid(column=1, row=1)
        wtext = "    已知Bug:终止服务后,端口仍会占用一段时间,建议终止服务后一分钟后重新启动服务\n    注意:在不了解此程序文档时请勿打开多个相同服务,如需要,可在Wiki的[特技]一栏中找到方法."
        lbl2 = Label(subwindow, text=wtext)
        lbl2.grid(column=1, row=2)
        start_btn = Button(subwindow, text="启动", command=start)
        start_btn.grid(column=1, row=3)
        close_btn = Button(subwindow, text="关闭窗口并退出", command=close)
        close_btn.grid(column=1, row=4)
        copy_btn = Button(subwindow, text="复制访问链接", command=copylink)
        copy_btn.grid(column=1, row=5)
        subwindow.protocol("WM_DELETE_WINDOW", close)
        subwindow.mainloop()
def ftpserver_ui():
    if True : 
        #webserverui_status = 1
        subwindow = ThemedTk(theme="yaru", toplevel=True, themebg=True)
        subwindow.title("FTPServer | LAN++ Manager")
        subwindow.geometry("850x500")
        os.chdir(static_path)
        task = Process(target=ftpserver.start)
        def start():
            task.start()
            print("started")
        def __close__():
            task.terminate()
            os.chdir(static_path)
            print("closed")
        def close():
            if task.is_alive() == False:
                start()
            __close__()
            os.chdir(static_path)
            subwindow.destroy()
        def copylink():
            pyperclip.copy("ftp://" + jsonget("ftpserveruser") + "@" + str(getip())  + ":" + jsonget("ftpserverport"))
        ntext = "    点击按钮以控制[FTP文件传输服务]\n    [启动] - 启动服务\n    [关闭窗口并退出] - 退出窗口(退出服务)\n    [复制访问链接] - 复制链接以便访问服务" + '当前配置:\n    端口:' + jsonget("ftpserverport") + "\n    目录: " + jsonget("ftpserverroot") + "\n    用户名:" + jsonget("ftpserveruser") + "\n    密码:" + jsonget("ftpserverpass") + "\n    打开服务后请通过此链接连接FTP服务器: [ftp://" + jsonget("ftpserveruser") + "@" + str(getip())  + ":" + jsonget("ftpserverport") + "]"
        lbl1 = Label(subwindow, text=ntext)
        lbl1.grid(column=1, row=1)
        wtext = "    已知Bug:终止服务后,端口仍会占用一段时间,建议终止服务后一分钟后重新启动服务\n    注意:在不了解此程序文档时请勿打开多个相同服务,如需要,可在Wiki的[特技]一栏中找到方法."
        lbl2 = Label(subwindow, text=wtext)
        lbl2.grid(column=1, row=2)
        start_btn = Button(subwindow, text="启动", command=start)
        start_btn.grid(column=1, row=3)
        close_btn = Button(subwindow, text="关闭窗口并退出", command=close)
        close_btn.grid(column=1, row=4)
        copy_btn = Button(subwindow, text="复制访问链接", command=copylink)
        copy_btn.grid(column=1, row=5)
        subwindow.protocol("WM_DELETE_WINDOW", close)
        subwindow.mainloop()
def setting_ui():
    pass
def runexit():
    sys.exit()
def about_ui():
    def visit():
        webbrowser.open("http://github.com/david-ajax/LANPP", new=0)
    subwindow = ThemedTk(theme="yaru", toplevel=True, themebg=True)
    subwindow.title("About | LAN++")
    subwindow.geometry("470x270")
    ntext = "  LAN++ -- A powerful tool for local area network  \n  Version: 1.0 (Beta)  \n  Repo: http://github.com/david-ajax/LANpp  \n  Powered By Wang Zhiyu \n  Use GPL 3.0 License"
    lbl1 = Label(subwindow, text=ntext)
    lbl1.grid(column=1, row=1)
    visit_btn = Button(subwindow, text="Visit The Repository", command=visit)
    visit_btn.grid(column=1, row=2)
    exit_btn = Button(subwindow, text="Exit", command=subwindow.destroy)
    exit_btn.grid(column=1, row=3)
def main():
    window = ThemedTk(theme="yaru", toplevel=True, themebg=True)
    window.title("LAN++ Manager")
    window.geometry("800x200")
    webserver = Button(window, text="浏览器文件管理服务", command=webserver_ui)
    webserver.grid(column=0, row=2)
    ftpserver = Button(window, text="FTP文件传输服务", command=ftpserver_ui)
    ftpserver.grid(column=1, row=2)
    setting = Button(window, text="设置", command=setting_ui)
    setting.grid(column=2, row=2)
    about = Button(window, text="关于", command=about_ui)
    about.grid(column=3, row=2)
    exit_btn = Button(window, text="退出", command=runexit)
    exit_btn.grid(column=4, row=2)
    window.mainloop()
if __name__ == '__main__':
    static_path = os.getcwd()
    fw=Tk()
    fw.withdraw()
    messagebox.showinfo(title='Welcome',message='欢迎使用LAN++ Beta Edition')
    main()