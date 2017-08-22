import tkinter as tk
from requests import get

LARGE_FONT = ("Verdana", 12)


class Gapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.title('Gapp')
        self.geometry('600x400')
        self.resizable(width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page in (Login, ChatList, ChatPage):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Login(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # Username label
        tk.Label(self, text="Username", font=LARGE_FONT).pack(pady=10, padx=10)

        # Where to enter our username
        self.__username_entry = tk.Entry(self)
        self.__username_entry.pack(pady=10, padx=10)

        # Button to register on server
        tk.Button(self, text='Register', command=lambda: self.__register_request()).pack(pady=10, padx=10)

    def __register_request(self):
        response = get("http://127.0.0.1:5000/sign_in/{}/".format(self.__username_entry.get())).json()

        if response['Status'] == 'Ok.':
            self.controller.show_frame(ChatList)
            self.controller.frames[ChatList].username = self.__username_entry.get()
        else:
            self.__username_entry.config(fg='red')


class ChatList(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.username = None

        label = tk.Label(self, text="ChatList", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(Login))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: (controller.show_frame(ChatPage), print(self.username)))
        button2.pack()


class ChatPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(Login))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(ChatList))
        button2.pack()


if __name__ == '__main__':
    app = Gapp()
    app.mainloop()
