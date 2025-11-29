from bs4 import BeautifulSoup
from bs4.element import ResultSet

def get_product_names(soup: BeautifulSoup) -> ResultSet:
    selector = '._17mcb .Bm3ON .buTCk .RfADt a'
    name_items = soup.select(selector=selector)
    return name_items

def get_price_items(soup: BeautifulSoup) -> ResultSet:
    selector = '._17mcb .Bm3ON .buTCk .aBrP0 .ooOxS'
    price_items = soup.select(selector=selector)
    return price_items

def get_historical_sold(soup: BeautifulSoup) -> ResultSet:
    selector = '._17mcb .Bm3ON .buTCk ._6uN7R'
    sold_items = soup.select(selector=selector)
    return sold_items

def get_product_origin(soup: BeautifulSoup) -> ResultSet:
    selector = '._17mcb .Bm3ON .buTCk ._6uN7R .oa6ri'
    product_origin = soup.select(selector=selector)
    return product_origin

def get_sold_item_at_index(index: int, sold_items: ResultSet) -> str:
    if index >= len(sold_items):
        return "0"
        
    sold_item = sold_items[index].select('._1cEkb')
    if len(sold_item) < 1:
        return str(0)
    return sold_item[0].text

# --- Lấy URL sản phẩm ---
def get_url_product(soup: BeautifulSoup):
    selector = '._17mcb .Bm3ON .buTCk .RfADt a'
    a_tags = soup.select(selector)
    
    urls = []
    for a in a_tags:
        url = a.get('href', '')
        if url.startswith('/'):
            url = 'https://www.lazada.vn' + url
        urls.append(url)
    return urls



# --- Lấy tất cả thông tin sản phẩm (Đã bỏ Rating) ---
def get_product_info(soup: BeautifulSoup):
    name_items = get_product_names(soup)
    price_items = get_price_items(soup)
    sold_items = get_historical_sold(soup)
    product_origin = get_product_origin(soup)
    urls = get_url_product(soup)

    for index in range(len(name_items)):
        sold_item = get_sold_item_at_index(index, sold_items)
        
        # Lấy URL an toàn
        url = urls[index] if index < len(urls) else 'N/A'
        
        # Lấy giá an toàn
        price = price_items[index].text if index < len(price_items) else 'N/A'
        
        # Lấy xuất xứ an toàn
        origin = product_origin[index].text if index < len(product_origin) else 'N/A'

       
        product_info = "{0} | {1} | {2} | {3} | {4}\n".format(
            name_items[index].get('title', 'N/A'), 
            price, 
            sold_item, 
            origin,
            url
        )
        yield product_info