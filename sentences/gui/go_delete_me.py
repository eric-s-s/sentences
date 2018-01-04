import tkinter as tk
import os

from sentences.text_to_pdf_delete_me import main
from sentences import DATA_PATH


def do_main():
    main_frame = tk.Tk()
    main_frame.iconbitmap(os.path.join(DATA_PATH, 'Picture_3a.ico'))
    button = tk.Button(master=main_frame, text='go', command=main)
    button.pack()
    main_frame.mainloop()


if __name__ == '__main__':
    do_main()

