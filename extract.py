import os
import json
import tkinter as tk
from tkinter import OptionMenu, StringVar, Canvas
import cairosvg # نیاز به نصب: pip install cairosvg
from PIL import Image, ImageTk 

# آدرس پوشه برای استخراج داده ها را وارد کنید
folder_path = "E:\\project\\my_web\\assets\\cart-vizit\\image\\svg"

# تابع خواندن محتویات پوشه
def read_folder_contents(folder_path):
    folder_structure = {}
    all_files = []

    for root, dirs, files in os.walk(folder_path):
        relative_path = os.path.relpath(root, folder_path)
        if relative_path == ".":
            relative_path = ""
        
        folder_structure[relative_path] = {"directories": dirs, "files": files}
        for f in files:
            full_path = os.path.join(root, f)
            all_files.append(full_path)
    return folder_structure, all_files

contents, file_list = read_folder_contents(folder_path)

# --- رابط کاربری ساده ---
window = tk.Tk()
window.title("نمایش فایل‌های پوشه (SVG Support)")
window.geometry("800x600")

selected_file = tk.StringVar(window)
selected_file.set("انتخاب فایل")

# ایجاد لیست کشویی از فایل‌ها
dropdown = tk.OptionMenu(window, selected_file, *file_list)
dropdown.pack(pady=10)

# بوم برای نمایش تصویر
canvas = tk.Canvas(window, width=780, height=480, bg="white")
canvas.pack(pady=10, padx=10)

# تابع نمایش تصویر بعد از انتخاب فایل
def show_image(*args):
    path = selected_file.get()
    if not os.path.exists(path):
        canvas.delete("all")
        return
    
    canvas.delete("all") # پاک کردن محتوای قبلی
    
    try:
        # اگر فایل SVG است، تبدیل به PNG موقت شود
        if path.lower().endswith('.svg'):
            # تبدیل SVG به PNG با cairosvg
            png_data = cairosvg.svg2png(url=path, output_width=780, output_height=480)
            
            # باز کردن PNG تبدیل شده با Pillow
            img_pil = Image.open(io.BytesIO(png_data))
        else:
            # برای سایر فرمت‌ها (PNG, JPG)
            img_pil = Image.open(path)

        # تغییر اندازه و تبدیل به فرمت قابل استفاده در Tkinter
        img_pil = img_pil.resize((780, 480))
        img_tk = ImageTk.PhotoImage(img_pil)
        
        # نمایش تصویر روی بوم
        canvas.create_image(0, 0, anchor="nw", image=img_tk)
        canvas.image = img_tk  # نگهداری مرجع برای جلوگیری از پاک شدن توسط GC
        
    except Exception as e:
        # نمایش پیام خطا در صورت عدم موفقیت
        canvas.create_text(390, 240, text=f"خطا در نمایش: {e}", fill="red", font=("Arial", 16))
        print(f"Error processing {path}: {e}")

# اتصال رویداد تغییر مقدار به تابع
selected_file.trace_add("write", show_image)

# اگر مسیر پوشه خالی بود، یک پیغام نمایش داده شود
if not file_list:
    selected_file.set("هیچ فایلی در مسیر یافت نشد")
    dropdown.config(state="disabled")

window.mainloop()
