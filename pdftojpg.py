# import module
import time
import os
import threading
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from pdf2image import convert_from_path

root = Tk()
root.title("PDF to JPG converter")
# root.geometry("670x160")
root.minsize(670, 160)
root.maxsize(670, 160)

# Store Pdf with convert_from_path function
# poppler_path = r"C:\Users\sures\Projects\Python\poppler-22.04.0\Library\bin"

class ThreadedTask(threading.Thread):

    def __init__(self, file_name, dest_folder):
        super().__init__()
        self.file_name = file_name
        self.dest_folder = dest_folder

    def run(self):
        try:
            images = convert_from_path(self.file_name)
            name_wo_extn = re.split('\.', os.path.basename(self.file_name))[0]
            for i in range(len(images)):
                # Save pages as images in the pdf
                images[i].save(os.path.join(self.dest_folder, name_wo_extn + '_' + str(i + 1) + '.jpg'), 'JPEG')
            print('Task completed')
            bar['value'] = 100
            root.update()
            messagebox.showinfo("PDF to JPEG",
                                "Selected file converted successfully.\n" + str(len(images)) + " images created.")
        except Exception as e:
            messagebox.showerror("PDF to JPEG", "Error while trying to convert\n" + str(e)[:133])
        finally:
            bar['value'] = 0
            convert_button['state'] = "normal"
            from_button['state'] = 'normal'
            check_box['state'] = 'normal'
            if not cb_var.get():
                dest_button['state'] = 'normal'


def open_file():
    bar['value'] = 0
    loc_entry.config(state="normal")
    loc_entry.delete(0, END)
    loc_entry.insert(0, filedialog.askopenfilename(initialdir="C:\\Users\\sures\\Pictures\\Scans",
                                                   title="Select a PDF file",
                                                   filetypes=(("pdf files", "*.pdf"), ("All files", "*.*"))))
    loc_entry.config(state="disabled")
    if cb_var.get():
        dest_entry.config(state="normal")
        dest_entry.delete(0, END)
        dest_entry.insert(0, os.path.dirname(loc_entry.get()))
        dest_entry.config(state="disabled")

    if loc_entry.get() and dest_entry.get():
        convert_button['state'] = "normal"


def open_dest():
    dest_entry.delete(0, END)
    dest_entry.insert(0, filedialog.askdirectory(initialdir="C:\\Users\\sures\\Pictures\\Scans",
                                                 title="Select destination folder"))

    if loc_entry.get() and dest_entry.get():
        convert_button['state'] = "normal"


def update_dest():
    if cb_var.get():
        dest_entry.config(state="normal")
        dest_entry.delete(0, END)
        dest_entry.insert(0, os.path.dirname(loc_entry.get()))
        dest_entry.config(state="disabled")
        dest_button.config(state="disabled")
    else:
        dest_entry.config(state="normal")
        dest_button.config(state="normal")
        dest_entry.delete(0, END)

    if loc_entry.get() and dest_entry.get():
        convert_button.config(state="normal")
    else:
        convert_button['state'] = "disabled"


def convert_this():
    bar['value'] = 0
    convert_button['state'] = "disabled"
    from_button['state'] = 'disabled'
    dest_button['state'] = 'disabled'
    check_box['state'] = 'disabled'
    if loc_entry.get() and dest_entry.get():
        file_name = loc_entry.get()
        thread1 = ThreadedTask(file_name, dest_entry.get())
        thread1.start()
        update_status(file_name, thread1)


def update_status(file_name, thread):
    file_size = os.path.getsize(file_name)
    per_millisecond = 2660
    total_milliseconds = int(file_size / per_millisecond) - 1000
    percent = 100 / total_milliseconds
    for _ in range(1, total_milliseconds, 1):
        if not thread.is_alive():
            break
        time.sleep(0.001)
        if bar['value'] + percent >= 100:
            break
        bar['value'] += percent
        root.update()


from_button = Button(root, text="Select file", command=open_file, width=20)
from_button.grid(row=0, column=0, columnspan=1, sticky=N + E + S + W, padx=10, pady=8)
loc_entry = Entry(root, text="", width=80)
loc_entry.grid(row=0, column=1, columnspan=5, sticky=N + E + S + W, padx=0, pady=10)

dest_button = Button(root, text="Save To", command=open_dest, width=20)
dest_button.grid(row=1, column=0, columnspan=1, sticky=N + E + S + W, padx=10, pady=8)
dest_entry = Entry(root, text="", width=65)
dest_entry.grid(row=1, column=1, columnspan=5, sticky=N + E + S + W, padx=0, pady=10)

convert_button = Button(root, text="Convert", command=convert_this, width=20)
convert_button.grid(row=2, column=3, columnspan=3, sticky=N + E + S + W, padx=10, pady=8)

cb_var = IntVar(value=1)
update_dest()
check_box = Checkbutton(root, text="Save in same directory", command=update_dest, variable=cb_var)
check_box.grid(row=2, column=0, columnspan=3, sticky=N + E + S + W, padx=10, pady=8)

bar = Progressbar(root, orient=HORIZONTAL)
bar.grid(row=3, column=0, padx=10, sticky=N + E + S + W, columnspan=6)


root.mainloop()
