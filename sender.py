import socket
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class SenderGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Secret File Transfer - Sender")

        self.label_title = ttk.Label(master, text="Secret File Transfer - Sender", font=("Helvetica", 16, "bold"))
        self.label_title.pack(pady=10)

        self.label_receiver_ip = ttk.Label(master, text="Receiver's IP:")
        self.label_receiver_ip.pack()

        self.entry_receiver_ip = ttk.Entry(master)
        self.entry_receiver_ip.pack()

        self.label_receiver_port = ttk.Label(master, text="Receiver's Port:")
        self.label_receiver_port.pack()

        self.entry_receiver_port = ttk.Entry(master)
        self.entry_receiver_port.pack()

        self.label_authentication_code = ttk.Label(master, text="Authentication Code:")
        self.label_authentication_code.pack()

        self.entry_authentication_code = ttk.Entry(master, show="*")
        self.entry_authentication_code.pack()

        self.button_browse = ttk.Button(master, text="Browse", command=self.browse_file)
        self.button_browse.pack(pady=10)

        self.button_send_file = ttk.Button(master, text="Send File", command=self.send_file)
        self.button_send_file.pack(pady=10)

    def browse_file(self):
        self.file_path = filedialog.askopenfilename()

    def send_file(self):
        receiver_ip = self.entry_receiver_ip.get()
        receiver_port = int(self.entry_receiver_port.get())
        authentication_code = self.entry_authentication_code.get()

        try:
            sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sender_socket.connect((receiver_ip, receiver_port))
            sender_socket.send(authentication_code.encode())

            sender_socket.send(self.file_path.encode())

            with open(self.file_path, "rb") as file:
                file_data = file.read()
                sender_socket.sendall(file_data)

            sender_socket.close()
            messagebox.showinfo("File Sent", "File sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send file: {e}")

def main():
    root = tk.Tk()
    sender_gui = SenderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
