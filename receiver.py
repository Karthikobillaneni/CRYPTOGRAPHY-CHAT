import socket
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class ReceiverGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Secret File Transfer - Receiver")

        self.label_title = ttk.Label(master, text="Secret File Transfer - Receiver", font=("Helvetica", 16, "bold"))
        self.label_title.pack(pady=10)

        self.label_port = ttk.Label(master, text="Receiver's Port:")
        self.label_port.pack()

        self.entry_port = ttk.Entry(master)
        self.entry_port.pack()

        self.label_authentication_code = ttk.Label(master, text="Set Authentication Code:")
        self.label_authentication_code.pack()

        self.entry_authentication_code = ttk.Entry(master, show="*")
        self.entry_authentication_code.pack()

        self.button_start_listening = ttk.Button(master, text="Start Listening", command=self.start_listening)
        self.button_start_listening.pack(pady=10)

    def start_listening(self):
        port = int(self.entry_port.get())
        authentication_code = self.entry_authentication_code.get()

        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver_socket.bind(("0.0.0.0", port))
        receiver_socket.listen(1)
        print(f"Receiver is waiting for connections on port {port}...")

        conn, addr = receiver_socket.accept()
        print(f"Connection established with {addr}")

        received_code = conn.recv(1024).decode()
        if received_code == authentication_code:
            file_path = conn.recv(1024).decode()

            file_data = b""
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file_data += data

            with open(file_path, "wb") as file:
                file.write(file_data)

            conn.close()
            messagebox.showinfo("File Received", f"File received successfully: {file_path}")
        else:
            conn.close()
            messagebox.showerror("Authentication Error", "Authentication failed!")

def main():
    root = tk.Tk()
    receiver_gui = ReceiverGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
