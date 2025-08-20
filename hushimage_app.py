import tkinter as tk
from tkinter import filedialog, messagebox
import mysql.connector
import hashlib
import os
import sys
import csv
import time
from PIL import Image, ImageTk
from stegano import lsb
from cryptography.fernet import Fernet
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# --- MySQL Setup ---
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",  # Replace with your sql_password
    database="steganography_app" # Replace with your database name
)
cursor = conn.cursor()

# --- Create Tables if Needed ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    encrypted_msg TEXT,
    image_path VARCHAR(500),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")
conn.commit()

# --- Utilities ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_key(password):
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def get_unique_filename(base_name="hidden", extension=".png"):
    count = 1
    while True:
        filename = f"{base_name}{count}{extension}"
        if not os.path.exists(filename):
            return filename
        count += 1

# --- Signup Function ---
def signup():
    username = entry_user.get()
    password = entry_pass.get()
    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                       (username, hash_password(password)))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")

# --- Login Function ---
def login():
    username = entry_user.get()
    password = entry_pass.get()
    hashed = hash_password(password)
    cursor.execute("SELECT id FROM users WHERE username=%s AND password_hash=%s", (username, hashed))
    result = cursor.fetchone()
    if result:
        root.destroy()
        open_steganography_gui(result[0], username)
    else:
        messagebox.showerror("Error", "Invalid credentials.")

# --- Forgot Password Feature ---
def forgot_password():
    def reset():
        uname = username_entry.get()
        new_pass = new_pass_entry.get()

        if not uname or not new_pass:
            messagebox.showerror("Error", "All fields are required!")
            return

        cursor.execute("SELECT id FROM users WHERE username=%s", (uname,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "Username does not exist.")
            return

        hashed = hash_password(new_pass)
        cursor.execute("UPDATE users SET password_hash=%s WHERE username=%s", (hashed, uname))
        conn.commit()
        messagebox.showinfo("Success", "Password reset successfully!")
        reset_win.destroy()

    reset_win = tk.Toplevel(root)
    reset_win.title("HushImage - Reset Password")
    reset_win.geometry("300x200")

    tk.Label(reset_win, text="Enter Username:").pack(pady=5)
    username_entry = tk.Entry(reset_win)
    username_entry.pack()

    tk.Label(reset_win, text="Enter New Password:").pack(pady=5)
    new_pass_entry = tk.Entry(reset_win, show="*")
    new_pass_entry.pack()

    tk.Button(reset_win, text="Reset Password", command=reset).pack(pady=10)

# --- Main Steganography Window ---
def open_steganography_gui(user_id, username):
    app = tk.Tk()
    app.title("HushImage - Dashboard")
    app.geometry("800x650")
    app.configure(bg="#2f4155")

    img_label = tk.Label(app)
    img_label.place(x=10, y=150)

    def logout():
        app.destroy()
        start_login_window()

    def show_dashboard():
        cursor.execute("SELECT COUNT(*) FROM messages WHERE user_id=%s", (user_id,))
        total = cursor.fetchone()[0]

        if total == 0:
            last_image = "N/A"
            last_time = "N/A"
        else:
            cursor.execute("SELECT image_path, timestamp FROM messages WHERE user_id=%s ORDER BY timestamp DESC LIMIT 1", (user_id,))
            row = cursor.fetchone()
            last_image = os.path.basename(row[0])
            last_time = row[1]

        dash_text = f"\n📦 Total Messages: {total}\n🖼 Last Image: {last_image}\n🕒 Last Used: {last_time}"
        dashboard_label.config(text=f"Welcome, {username}!{dash_text}")

    def show_image():
        nonlocal img_path
        img_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg")])
        img = Image.open(img_path)
        img.thumbnail((250, 250))
        img = ImageTk.PhotoImage(img)
        img_label.configure(image=img)
        img_label.image = img

    def hide_message():
        msg = text_input.get("1.0", tk.END).strip()
        pwd = entry_pwd.get().strip()
        if not img_path or not msg or not pwd:
            messagebox.showerror("Error", "Please select image, message and enter password.")
            return
        key = generate_key(pwd)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(msg.encode())
        secret = lsb.hide(img_path, encrypted.decode())

        save_path = get_unique_filename("hidden", ".png")
        secret.save(save_path)

        cursor.execute("INSERT INTO messages (user_id, encrypted_msg, image_path) VALUES (%s, %s, %s)",
                       (user_id, encrypted.decode(), save_path))
        conn.commit()
        text_input.delete("1.0", tk.END)
        text_input.insert(tk.END, "\u2705 Message hidden successfully.")
        messagebox.showinfo("Success", f"Message saved to {save_path}")
        show_dashboard()

    def show_message():
        pwd = entry_pwd.get().strip()
        if not img_path or not pwd:
            messagebox.showerror("Error", "Please select image and enter password.")
            return
        try:
            hidden = lsb.reveal(img_path)
            key = generate_key(pwd)
            fernet = Fernet(key)
            decrypted = fernet.decrypt(hidden.encode()).decode()
            text_input.delete("1.0", tk.END)
            text_input.insert(tk.END, decrypted)
        except:
            messagebox.showerror("Error", "Wrong password or no hidden message.")

    def export_history_to_csv(records):
        filename = f"history_{int(time.time())}.csv"
        if not records:
            messagebox.showinfo("Info", "No message history to export.")
            return
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Image File", "Timestamp"])
            for row in records:
                writer.writerow([os.path.basename(row[0]), row[1]])
        messagebox.showinfo("Export Complete", f"History exported to {filename}")

    def export_history_to_pdf(records):
        if not records:
            messagebox.showinfo("Info", "No message history to export.")
            return

        filename = f"message_history_{int(time.time())}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, f"Message History Report - {username}")

        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Total Messages: {len(records)}")

        y = height - 110
        c.drawString(50, y, "Image File")
        c.drawString(300, y, "Timestamp")
        c.line(50, y-2, 550, y-2)

        y -= 20
        for row in records:
            if y < 50:
                c.showPage()
                y = height - 50
            c.drawString(50, y, os.path.basename(row[0]))
            c.drawString(300, y, str(row[1]))
            y -= 20

        c.save()
        messagebox.showinfo("Export Complete", f"PDF saved as: {filename}")

    def show_selected_image(records, lb):
        selection = lb.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select an item from the list.")
            return
        index = selection[0]
        try:
            image_path = records[index][0]
            if os.path.exists(image_path):
                os.startfile(image_path)
            else:
                messagebox.showerror("Error", f"Image not found: {image_path}")
        except:
            messagebox.showerror("Error", "Unable to open image.")

    def show_message_history():
        history_win = tk.Toplevel(app)
        history_win.title("HushImage - Message History")
        history_win.geometry("600x450")
        history_win.configure(bg="#2f4155")

        tk.Label(history_win, text="Your Encrypted Message History", font=("Arial", 14), fg="white", bg="#2f4155").pack(pady=10)

        history_frame = tk.Frame(history_win, bg="white", relief="groove", bd=2)
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, font=("Courier", 10), width=90)
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        cursor.execute("SELECT image_path, timestamp FROM messages WHERE user_id = %s ORDER BY timestamp DESC", (user_id,))
        history_records = cursor.fetchall()

        if not history_records:
            listbox.insert(tk.END, "No hidden messages yet.")
        else:
            for row in history_records:
                listbox.insert(tk.END, f"Image: {os.path.basename(row[0])} | Time: {row[1]}")

        tk.Button(history_win, text="View Selected Image", command=lambda: show_selected_image(history_records, listbox)).pack(pady=5)
        tk.Button(history_win, text="Export to CSV", command=lambda: export_history_to_csv(history_records)).pack(pady=5)
        tk.Button(history_win, text="Export to PDF", command=lambda: export_history_to_pdf(history_records)).pack(pady=5)

    img_path = ""

    dashboard_label = tk.Label(app, text=f"Welcome, {username}!", bg="#2f4155", fg="white", font=("Arial", 14))
    dashboard_label.pack(pady=10)
    show_dashboard()

    tk.Button(app, text="Select Image", command=show_image).pack(pady=5)

    tk.Label(app, text="Enter Password:", bg="#2f4155", fg="white").pack()
    entry_pwd = tk.Entry(app, show="*")
    entry_pwd.pack(pady=2)

    tk.Label(app, text="Enter Message:", bg="#2f4155", fg="white").pack()
    text_input = tk.Text(app, height=5, width=50)
    text_input.pack(pady=5)

    tk.Button(app, text="Hide Message", command=hide_message).pack(pady=5)
    tk.Button(app, text="Show Message", command=show_message).pack(pady=5)
    tk.Button(app, text="My Hidden Messages", command=show_message_history).pack(pady=5)
    tk.Button(app, text="Logout", command=logout, bg="red", fg="white").pack(pady=10)

    app.mainloop()

# --- Login Window ---
def start_login_window():
    global entry_user, entry_pass, root
    root = tk.Tk()
    root.title("HushImage - Login / Signup")
    root.geometry("350x300")

    tk.Label(root, text="Username").pack(pady=5)
    entry_user = tk.Entry(root)
    entry_user.pack()

    tk.Label(root, text="Password").pack(pady=5)
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    tk.Button(root, text="Login", width=15, command=login).pack(pady=10)
    tk.Button(root, text="Signup", width=15, command=signup).pack(pady=5)
    tk.Button(root, text="Forgot Password?", width=20, command=forgot_password).pack(pady=5)

    root.mainloop()

# Start the app
start_login_window()
