import tkinter as tk


def main():
    #utilities
    #Variables


    #Functions
    def changeBtnTxt(btn, ):
        if btn.cget("text") == "Encender":
            btn.config(text="Apagar")
        else:
            btn.config(text="Encender")

    #Widgets creation
    window = tk.Tk()
    greetings = tk.Label(window, text="Hello, tkinter")
    button = tk.Button(
                        window,
                        text="Encender",
                        command=lambda : changeBtnTxt(button)
                    )

    #instantiate widgets
    greetings.pack()
    button.pack()
    button.bind(window, )

    #init main loop
    window.mainloop()




if __name__ == "__main__":
    main()