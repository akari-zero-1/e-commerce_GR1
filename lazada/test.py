import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_high_quality_url(small_url):
   
    if not small_url:
        return None
        
    
    clean_url = re.sub(r'_\d+x\d+q\d+.*$', '', small_url)
    
    
    if clean_url == small_url: 
         clean_url = small_url.replace('_120x120', '_720x720').replace('_SS2', '')
         
    return clean_url

def run_test_gallery():
    # 1. Cấu hình Selenium
    options = Options()
    # options.add_argument("--headless") # Bỏ comment nếu muốn chạy ẩn
    options.add_argument("--disable-blink-features=AutomationControlled") 
    
    print("Đang khởi động trình duyệt...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # 2. Nhập Link sản phẩm cần test (Thay link của bạn vào đây)
        url = "https://www.lazada.vn//www.lazada.vn/products/pdp-i2092450323.html" 
        
        print(f"Đang truy cập: {url}")
        driver.get(url)
        
        # Đợi chút cho gallery load (Lazada load JS khá nặng)
        time.sleep(5) 
        
        # 3. Lấy Source và Parse bằng BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
       
        gallery_container = soup.select_one('#module_item_gallery_1')
        
        if gallery_container:
           
            img_tags = gallery_container.select('img')
            
            print(f"\nTìm thấy {len(img_tags)} ảnh trong gallery.\n")
            print("-" * 50)
            print(f"{'STT':<5} | {'URL GỐC (HD)':<60}")
            print("-" * 50)
            
            unique_images = set() 

            for i, img in enumerate(img_tags):
                # Lấy link từ src
                src = img.get('src')
                
                # Nếu src là ảnh loading hoặc rỗng, lấy data-src (lazy load)
                if not src or 'data:image' in src:
                    src = img.get('data-src')
                
                if src:
                    # Chuyển đổi sang ảnh nét
                    hd_url = get_high_quality_url(src)
                    
                    # Một số ảnh là icon video (play button), ta có thể lọc bỏ nếu muốn
                    if "overlay-play.png" in hd_url:
                        continue
                        
                    if hd_url not in unique_images:
                        unique_images.add(hd_url)
                        print(f"{i+1:<5} | {hd_url}")
        else:
            print("Không tìm thấy khối Gallery (Kiểm tra lại Selector hoặc Link)")

    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")
    finally:
        # Giữ màn hình để xem kết quả, nhấn Enter để thoát
        input("\nĐã xong. Nhấn Enter để đóng trình duyệt...")
        driver.quit()

if __name__ == "__main__":
    run_test_gallery()