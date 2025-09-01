# HushImage – Secure Image Steganography (GUI)
- **HushImage** is a Python application that allows you to hide secret messages inside images in a way that is both simple and secure. It’s designed so anyone can use it, even without any programming knowledge.
- All messages are first encrypted using AES encryption, which means that even if someone manages to access the image, the hidden message remains completely unreadable. The application also supports user
  accounts with signup, login, and password reset functionality, and all passwords are stored securely using hashing techniques.
- The graphical interface (GUI), built with Tkinter, makes it easy to hide or extract messages with just a few clicks—no coding required. Messages are cleverly hidden in the image’s pixels using steganography,     so the image looks unchanged to anyone who sees it.
- Every hidden message is saved in a MySQL database, allowing you to track your message history and export it as a CSV or PDF for safekeeping. HushImage works on Windows, macOS, and Linux, making it accessible     to almost everyone.
- Beyond its practical uses, HushImage is also educational, offering a hands-on way to explore concepts like cryptography, secure data storage, and steganography.

---

## 📌 Features

- 🔐 **User Authentication**
  - Signup/Login with SHA-256 password hashing  
  - Password reset functionality  

- 🔒 **AES Encryption**
  - Messages are encrypted with Fernet (AES-128) before embedding  

- 🖼 **Image Steganography**
  - Uses `stegano.lsb` to hide and retrieve messages inside image pixels  

- 🗃️ **MySQL Logging**
  - Stores encrypted messages with image path and timestamp per user  

- 📑 **Message History**
  - View previously hidden messages  
  - Export history to **CSV** or **PDF**  

- 🧠 **Simple & User-Friendly GUI**
  - Built with **Tkinter** and **Pillow** for image handling  

---

## 🧰 Tech Stack

  | Layer         | Technology                                      |
  |---------------|------------------------------------------------|
  | **Frontend**  | `Tkinter`, `Pillow (PIL)`                       |
  | **Backend**   | `Python`, `stegano`, `cryptography`, `hashlib` |
  | **Database**  | `MySQL` (`mysql.connector`)                     |
  | **Utilities** | `reportlab`, `csv`, `os`, `base64`, `time`      |

---

## 🏗️ Project Structure

```
  HushImage/
  │── main.py              # App entry point
  │── login.py             # Login & signup logic
  │── steganography.py     # Hide/Extract logic
  │── export.py            # Export to PDF/CSV
  │── config.py            # Database configs
  │── requirements.txt     # Dependencies
```
---

## ⚙️ Requirements

Inside `requirements.txt`:
```
mysql-connector-python
cryptography
pillow
stegano
reportlab

```

## 🔧 Setup Instructions
  ### 1. Clone the Repository
```bash
  git clone https://github.com/UnnayanSingh/HushImage.git
  cd HushImage
```

  ### 2. Install Dependencies
```bash
  pip install -r requirements.txt

```
  ### 3. Set Up MySQL Database
```sql
  CREATE DATABASE hushimage_app;
  conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="hushimage_app");

```

### 4. Run the App
```bash
  python main.py

```
---

### 🏛️Architecture Diagram
  ```User → GUI (Tkinter) → Steganography (stegano.lsb) → AES Encryption (cryptography) → MySQL Database (history logs)```

---

## 🔐 Security Notes
- Images are encrypted using Fernet (AES-128).  
- Hidden data should not exceed image capacity (larger images allow more data).  
- Always use strong passwords for message encryption.  
- This project is for educational purposes and not intended for production-level secrecy.

---
  
### Contact Information  
- GitHub: [UnnayanSingh](https://github.com/UnnayanSingh)  
- LinkedIn: https://www.linkedin.com/in/unnayan-singh-2b9062289  
- Email: unnayansingh2005@gmail.com

---
