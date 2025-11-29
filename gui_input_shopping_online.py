import tkinter as tk
from tkinter import ttk 
from main import shopping_online_run

def print_input_value():
    location = e1.get()
    keyword = e2.get()
    page = e3.get()
    
    # Hiệu ứng nhỏ: Đổi text nút bấm khi xử lý
    print_button.config(text="Đang xử lý...", state="disabled")
    root.update() # Cập nhật giao diện ngay lập tức
    
    root.destroy()
    shopping_online_run(location, keyword, page)

def center_window(window, width, height):
    """Hàm giúp căn giữa cửa sổ trên màn hình"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')


root = tk.Tk()
root.title("Shopping Scraper Tool")
# Thiết lập kích thước và căn giữa
window_width = 500
window_height = 350
center_window(root, window_width, window_height)
root.configure(bg="#f0f2f5") # Màu nền xám nhạt hiện đại

# --- STYLE (Định dạng) ---
style = ttk.Style()
style.theme_use('clam') # Dùng theme 'clam' để dễ tùy chỉnh màu hơn


main_frame = tk.Frame(root, bg="white", padx=30, pady=30)
main_frame.pack(expand=True, fill="both", padx=20, pady=20)
# Tạo hiệu ứng đổ bóng nhẹ bằng cách vẽ border (tùy chọn)
main_frame.configure(highlightbackground="#d1d5db", highlightthickness=1)

# --- TIÊU ĐỀ ---
lbl_title = tk.Label(main_frame, text="CẤU HÌNH THU THẬP", 
                     font=("Segoe UI", 16, "bold"), bg="white", fg="#1a202c")
lbl_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))


label_font = ("Segoe UI", 10)
entry_font = ("Segoe UI", 10)

# Row 1: Location
tk.Label(main_frame, text='Location:', font=label_font, bg="white", anchor='w').grid(row=1, column=0, sticky='w', pady=10)
e1 = tk.Entry(main_frame, font=entry_font, bg="#f9fafb", relief="flat", highlightthickness=1, highlightbackground="#d1d5db")
e1.grid(row=1, column=1, sticky='ew', padx=(10, 0), ipady=5)
e1.insert(0, "lazada") 

# Row 2: Keyword
tk.Label(main_frame, text='Keyword:', font=label_font, bg="white", anchor='w').grid(row=2, column=0, sticky='w', pady=10)
e2 = tk.Entry(main_frame, font=entry_font, bg="#f9fafb", relief="flat", highlightthickness=1, highlightbackground="#d1d5db")
e2.grid(row=2, column=1, sticky='ew', padx=(10, 0), ipady=5)
e2.focus() 

# Row 3: Page
tk.Label(main_frame, text='Page Limit:', font=label_font, bg="white", anchor='w').grid(row=3, column=0, sticky='w', pady=10)
e3 = tk.Entry(main_frame, font=entry_font, bg="#f9fafb", relief="flat", highlightthickness=1, highlightbackground="#d1d5db")
e3.grid(row=3, column=1, sticky='ew', padx=(10, 0), ipady=5)
e3.insert(0, "5") 

# Căn chỉnh cột 1 (cột input) để nó giãn ra
main_frame.columnconfigure(1, weight=1)


btn_style = {"font": ("Segoe UI", 11, "bold"), "bg": "#2563eb", "fg": "white", "activebackground": "#1d4ed8", "activeforeground": "white", "relief": "flat", "cursor": "hand2"}

print_button = tk.Button(main_frame, text="BẮT ĐẦU QUÉT DỮ LIỆU", command=print_input_value, **btn_style)
print_button.grid(row=4, column=0, columnspan=2, pady=(30, 0), sticky='ew', ipady=5)

# Start loop
root.mainloop()