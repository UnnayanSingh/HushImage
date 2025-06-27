# 🖼️ Image Steganography App - Desktop GUI

A secure and interactive desktop application built with Python that allows users to hide encrypted messages inside images using steganography. The app includes login/signup, password protection, AES encryption, message history logging in MySQL, and export options in PDF/CSV.

---

## 📌 Features

- 🔐 **User Authentication**
  - Signup/Login with SHA-256 password hashing
  - Forgot password reset functionality

- 🔒 **AES Encryption**
  - Messages are encrypted using Fernet (AES-128) before embedding

- 🖼 **Image Steganography**
  - Uses `stegano.lsb` to hide and retrieve messages inside image pixels

- 🗃️ **MySQL Logging**
  - Stores encrypted messages with image path and timestamp for each user

- 📑 **Message History**
  - View all previously hidden messages
  - Export history to CSV or PDF reports

- 🧠 **Simple and User-Friendly UI**
  - Built with Tkinter and Pillow for image display

---

## 🧰 Tech Stack

| Layer       | Technology                                      |
|-------------|-------------------------------------------------|
| **Frontend**  | `Tkinter`, `Pillow (PIL)`                      |
| **Backend**   | `Python`, `stegano`, `cryptography`, `hashlib` |
| **Database**  | `MySQL` (`mysql.connector`)                    |
| **Utilities** | `reportlab`, `csv`, `os`, `base64`, `time`     |

---

## 🏗️ Project Structure
├── image_steganography_app.py # Main application file
├── logo.jpg # Optional UI/logo image
├── requirements.txt # Python dependencies
└── README.md # This file

---

### `requirements.txt`:
```txt```
mysql-connector-python
cryptography
pillow
stegano
reportlab

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/image-steganography-gui.git
cd image-steganography-gui

### 2. Install Dependencies
```bash
pip install -r requirements.txt

### 3. Set Up MySQL Database
```sql
CREATE DATABASE steganography_app;

Update your MySQL credentials in
`image_steganography_app.py`:
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="steganography_app"
)
#Tables are automatically created on first run.

### 4. Run the App
```bash
python image_steganography_app.py

