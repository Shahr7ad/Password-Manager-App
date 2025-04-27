import customtkinter as ctk
import json
from cryptography.fernet import Fernet

# کلید تست برای رمزگذاری
key = b'gZk4kHdFzKq0bM9D5GvjxKxOpR0m-d0QJDcM4vlNDq4='
cipher = Fernet(key)

# تنظیمات کلی
ctk.set_appearance_mode("light")  # حالت روشن
ctk.set_default_color_theme("blue")  # تم رنگ آبی ملایم

app = ctk.CTk()
app.title("Modern Password Manager")
app.geometry("400x550")
app.resizable(False, False)

# توابع
def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if website and username and password:
        data = {
            "website": website,
            "username": username,
            "password": password
        }
        encrypted_data = cipher.encrypt(json.dumps(data).encode())

        with open("passwords.txt", "ab") as f:
            f.write(encrypted_data + b"\n")

        website_entry.delete(0, "end")
        username_entry.delete(0, "end")
        password_entry.delete(0, "end")

        ctk.CTkMessagebox(title="Success", message="✅ Password Saved Successfully!", icon="check")

def view_passwords():
    try:
        with open("passwords.txt", "rb") as f:
            lines = f.readlines()
            result = ""
            for line in lines:
                decrypted = cipher.decrypt(line.strip()).decode()
                item = json.loads(decrypted)
                result += f"Website: {item['website']}\nUsername: {item['username']}\nPassword: {item['password']}\n\n"
            result_window = ctk.CTkToplevel(app)
            result_window.title("Saved Passwords")
            result_window.geometry("350x400")
            textbox = ctk.CTkTextbox(master=result_window, width=300, height=350)
            textbox.pack(padx=10, pady=10)
            textbox.insert("end", result)
    except Exception as e:
        print("Error:", e)

# ظاهر رابط کاربری (UI)

frame = ctk.CTkFrame(master=app, width=360, height=500, corner_radius=25, fg_color="#f9f9f9")
frame.place(relx=0.5, rely=0.5, anchor="center")

title_label = ctk.CTkLabel(master=frame, text="Password Manager", font=("Poppins", 24, "bold"))
title_label.pack(pady=(20, 10))

website_entry = ctk.CTkEntry(master=frame, width=300, height=40, placeholder_text="Website...", fg_color="#ffffff")
website_entry.pack(pady=10)

username_entry = ctk.CTkEntry(master=frame, width=300, height=40, placeholder_text="Username/Email...", fg_color="#ffffff")
username_entry.pack(pady=10)

password_entry = ctk.CTkEntry(master=frame, width=300, height=40, placeholder_text="Password...", fg_color="#ffffff")
password_entry.pack(pady=10)

save_btn = ctk.CTkButton(master=frame, text="Save Password", command=save_password, width=300, height=45, corner_radius=15, fg_color="#4CAF50", hover_color="#45a049")
save_btn.pack(pady=15)

view_btn = ctk.CTkButton(master=frame, text="View Saved Passwords", command=view_passwords, width=300, height=45, corner_radius=15, fg_color="#2196F3", hover_color="#1e88e5")
view_btn.pack(pady=5)

# اجرای برنامه
app.mainloop()
