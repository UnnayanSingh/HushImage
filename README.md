# HushImage – Secure Image Steganography (GUI)

**HushImage** is a secure and interactive GUI application built with Python that allows users to **hide encrypted messages inside images** using steganography.  
It features user authentication, AES encryption, history logging with MySQL, and export options in PDF/CSV.

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
...

## ⚙️ Requirements

Inside `requirements.txt`:

mysql-connector-python
cryptography
pillow
stegano
reportlab

---

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
###3. Set Up MySQL Database
```sql
CREATE DATABASE hushimage_app;

```

```**Update your MySQL credentials in config.py:
conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="your_password",
  database="hushimage_app"
)

```

### 4. Run the App
```bash
python main.py

```

### Architecture Diagram
## 🏛️ Architecture
User → GUI (Tkinter) → Steganography (stegano.lsb) → AES Encryption (cryptography) → MySQL Database (history logs)

### Security Notes
## 🔐 Security Notes
- Images are encrypted using Fernet (AES-128).  
- Hidden data should not exceed image capacity (larger images allow more data).  
- Always use strong passwords for message encryption.  
- This project is for educational purposes and not intended for production-level secrecy.
  
### Contact / Author
## 👨‍💻 Author
**Unnayan Singh**  
- GitHub: [UnnayanSingh](https://github.com/UnnayanSingh)  
- LinkedIn: https://www.linkedin.com/in/unnayan-singh-2b9062289  
- Email: unnayansingh2005@gmail.com  
