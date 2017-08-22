import tkinter as tk
from requests import get

LARGE_FONT = ("Verdana", 12)


class Gapp(tk.Tk):
    """GUI client for Gapp chat platform."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Basic configuration of application.
        self.title('Gapp')
        self.geometry('600x400')
        self.resizable(width=False, height=False)

        # If window is closed and user have logged in, we have to send a logout message.
        self.username = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Main frame that other frames is inside it.
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Add all instance of frames to a dictionary for easy switching.
        self.frames = {}
        for page in (Login, ChatList, ChatPage):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start app with Login page.
        self.show_frame(Login)

    def show_frame(self, page):
        """Bring the page to front and make it visible."""
        self.frames[page].tkraise()

    def on_close(self):
        """On closing window (event) send a sign out request to server."""
        if self.username is not None:
            data = get("http://127.0.0.1:5000/sign_out/{}/".format(self.username))
            print(data.text)
            response = data.json()
            if response['Status'] != 'Ok.':
                print(response['Description'])
        self.destroy()


class Login(tk.Frame):
    """First page of Gapp GUI client that ask you a name to register you."""
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # Username label
        tk.Label(self, text="Username", font=LARGE_FONT).pack(pady=10, padx=10)

        # Where to enter our username
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=10, padx=10)

        # Button to register on server
        tk.Button(self, text='Register', command=self.__register_request).pack(pady=10, padx=10)

    def __register_request(self):
        """Send a request to server for checking anyone online with this username."""
        response = get("http://127.0.0.1:5000/sign_in/{}/".format(self.username_entry.get())).json()

        # Username is registered for user, set it in controller to send a sign out request on exit
        # and call set_username of ChatList page to use the registered username.
        if response['Status'] == 'Ok.':
            self.controller.username = self.username_entry.get()
            self.controller.frames[ChatList].set_username(self.username_entry.get())
            self.controller.show_frame(ChatList)
            self.username_entry.config(fg='black')
        # If username was registered before, change color of text to red.
        else:
            self.username_entry.config(fg='red')


class ChatList(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="ChatList", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(Login))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: (controller.show_frame(ChatPage), print(self.username)))
        button2.pack()

    def set_username(self, username):
        pass


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
