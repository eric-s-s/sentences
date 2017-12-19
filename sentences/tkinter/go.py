import tkinter as tk

from sentences.text_to_pdf import main


def do_main():
    main_frame = tk.Tk()
    button = tk.Button(master=main_frame, text='go', command=main)
    button.pack()
    main_frame.mainloop()


if __name__ == '__main__':
    do_main()

