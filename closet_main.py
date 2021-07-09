#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import closet_utils as utils
from tkinter import messagebox


class ExtractMessageApp(tk.Frame):
    def __init__(self, original_image: str, master: tk.Frame):
        super().__init__(master)
        self.input_image: str = original_image
        self.master = master
        self.pack(padx=10, pady=10)
        self.create_widgets()

        self.extract_message()

    def create_widgets(self):
        self.label = tk.Label(self, text="Embedded message:")
        self.label.grid(row=2, column=0)

        self.scrolled_text = ScrolledText(self)
        self.scrolled_text.grid(row=3, column=0, columnspan=5)

        self.done_button = tk.Button(self, text="Done")
        self.done_button.grid(row=4, column=0)
        self.done_button["command"] = self.destroy

    def extract_message(self):
        message, exit_code = utils.extract_text(self.input_image)

        if exit_code != 0:
            messagebox.showerror(
                title="Could not extract message",
                message=
                f"Unable to extract message. Failed with code: {exit_code}.")

            self.destroy()

        self.scrolled_text.insert(tk.INSERT, message)
        self.scrolled_text["state"] = tk.DISABLED


class AddMessageApp(tk.Frame):
    def __init__(self, original_image: str, master: tk.Frame):
        super().__init__(master)
        self.input_image: str = original_image
        self.master = master
        self.pack(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        self.embedded_label = tk.Label(self, text="Closet image:")
        self.embedded_label.grid(row=1, column=0)

        self.embedded_entry = tk.Entry(self)
        self.embedded_entry.grid(row=1, column=1, columnspan=3)

        self.embedded_button = tk.Button(self, text="Open File")
        self.embedded_button.grid(row=1, column=4)
        self.embedded_button["command"] = self.select_embedded

        self.label = tk.Label(self, text="Your message:")
        self.label.grid(row=2, column=0)

        self.scrolled_text = ScrolledText(self)
        self.scrolled_text.grid(row=3, column=0, columnspan=5)

        self.done_button = tk.Button(self, text="Done")
        self.done_button.grid(row=4, column=0)
        self.done_button["command"] = self.add_message

    def select_embedded(self):
        path: str = filedialog.asksaveasfilename(
            filetypes=[("supported image files", (".png", "*.jpg", "*.jpeg"))])
        self.embedded_entry.delete(0, 'end')
        self.embedded_entry.insert(0, path)

    def add_message(self):
        self.output_image: str = self.embedded_entry.get()
        if len(self.output_image) == 0:
            messagebox.showerror(
                title="No image selected",
                message="You need to select where to save your closet image!")
            return

        message: str = self.scrolled_text.get("1.0", tk.END)

        exit_code: int = utils.embed_text(self.input_image, self.output_image,
                                          message)

        if exit_code != 0:
            messagebox.showerror(
                title="Could not add message",
                message=f"Unable to add message. Failed with code: {exit_code}."
            )
        else:
            messagebox.showinfo(title="Success",
                                message="Succesfully added message.")

        self.destroy()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        self.img_label = tk.Label(self, text="Input image:")
        self.img_label.grid(row=0, column=0)

        self.img_entry = tk.Entry(self)
        self.img_entry.grid(row=0, column=1, columnspan=3)

        self.img_button = tk.Button(self, text="Open File")
        self.img_button.grid(row=0, column=4)
        self.img_button["command"] = self.select_img

        self.add_button = tk.Button(self, text="Add Message")
        self.add_button.grid(row=2, column=1)
        self.add_button["command"] = self.add_message

        self.extract_button = tk.Button(self, text="Extract Message")
        self.extract_button.grid(row=2, column=3)
        self.extract_button["command"] = self.extract_message

    def select_img(self):
        path: str = filedialog.askopenfilename(
            filetypes=[("supported image files", (".png", "*.jpg", "*.jpeg"))])
        self.img_entry.delete(0, 'end')
        self.img_entry.insert(0, path)

    def add_message(self):
        if len(self.img_entry.get()) == 0:
            messagebox.showerror(title="No image selected",
                                 message="You need to select an input image!")
            return

        add_message = AddMessageApp(self.img_entry.get(), self.master)
        add_message.mainloop()

    def extract_message(self):
        if len(self.img_entry.get()) == 0:
            messagebox.showerror(title="No image selected",
                                 message="You need to select an input image!")
            return

        extract_message = ExtractMessageApp(self.img_entry.get(), self.master)
        extract_message.mainloop()


root = tk.Tk()
root.title("Closet Connect")
app = Application(master=root)
app.mainloop()
