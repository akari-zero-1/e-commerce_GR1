import time
import csv  # <--- Mới thêm
from datetime import datetime # <--- Mới thêm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# --- HÀM TÍNH SAO GIỮ NGUYÊN ---
def get_star_rating(review_item):
    try:
        imgs = review_item.select('img.star')
        if not imgs:
            container = review_item.select_one('.container-star')
            if container: imgs = container.find_all('img')
            else: return 0

        score = 0
        filled_star_code = "TB19ZvEgfDH8KJjy1XcXXcpdXXa" 
        for img in imgs:
            if filled_star_code in img.get('src', ''):
                score += 1
        return score
    except: return 0

def run_scraper_pagination():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("start-maximized")

    print("Đang khởi động trình duyệt...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # 1. TẠO TÊN FILE THEO THỜI GIAN
    # Format: YYYYMMDD_HHMMSS (Ví dụ: lazada_reviews_20251025_093015.csv)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"lazada_reviews_{timestamp}.csv"
    
    try:
        url = "https://www.lazada.vn/products/combo-dau-goi-va-dau-xa-tresemme-keratin-smooth-keratinbond-cho-toc-kho-xo-roi-vao-nep-suon-muot-640g-620g-i295700910-s471602630.html"
        driver.get(url)
        
        print("Vui lòng Login/Captcha thủ công nếu cần.")
        print("="*50 + "\n")

        # Cuộn xuống
        try:
            target = driver.find_element(By.CSS_SELECTOR, "#module_product_review")
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", target)
            time.sleep(3)
        except:
            print("Không tìm thấy chỗ cuộn, thử chạy tiếp...")

        # 2. MỞ FILE CSV ĐỂ GHI
        # mode='w': ghi mới, encoding='utf-8-sig': để Excel hiển thị tiếng Việt không lỗi font
        with open(filename, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            
            # Ghi dòng tiêu đề (Header)
            writer.writerow(['Trang', 'Tên User', 'Số Sao', 'Nội Dung Review'])

            # --- VÒNG LẶP CÁC TRANG ---
            current_page = 1
            max_pages = 10000  

            while current_page <= max_pages:
                print(f"\n--- ĐANG CÀO TRANG {current_page} ---")
                
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                review_items = soup.select('#module_product_review .item')
                
                if not review_items:
                    print("Không tìm thấy review nào.")
                    break

                for item in review_items:
                    # Lấy tên
                    user_elem = item.select_one('.item-top .user-info .infos p:nth-of-type(1) span')
                    if not user_elem: user_elem = item.select_one('.middle')
                    user_name = user_elem.text.strip() if user_elem else "Ẩn danh"
                    
                    # Lấy sao
                    rating = get_star_rating(item)
                    
                    # Lấy nội dung
                    content_elem = item.select_one('.item-middle .content')
                    if not content_elem: content_elem = item.select_one('.item-middle')
                    content = content_elem.text.strip().replace('\n', ' ') if content_elem else ""

                    # In ra màn hình để theo dõi
                    print(f"[{current_page}] {user_name:<20} | {rating}* | {content[:30]}...")
                    
                    # 3. GHI DÒNG DỮ LIỆU VÀO FILE CSV
                    writer.writerow([current_page, user_name, rating, content])

                # Xử lý Next trang
                if current_page >= max_pages:
                    print("Đã đạt giới hạn trang.")
                    break
                
                try:
                    next_btn_selector = "li.iweb-pagination-next > button"
                    next_button = driver.find_element(By.CSS_SELECTOR, next_btn_selector)
                    
                    if not next_button.is_enabled():
                        print("Nút Next bị khóa -> Đã hết trang.")
                        break
                    
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(3) 
                    current_page += 1
                    
                except Exception as e:
                    print(f"Không bấm được nút Next (hoặc hết trang). Lỗi: {e}")
                    break
        
        print(f"\n>>> ĐÃ LƯU XONG FILE: {filename}")

    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper_pagination()