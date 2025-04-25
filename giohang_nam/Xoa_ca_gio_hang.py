from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Cấu hình Appium
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "emulator-5554"
options.app_package = "com.example.datdoanonline"
options.app_activity = "com.example.datdoanonline.Activity.Login_Activity"
options.automation_name = "UiAutomator2"
options.no_reset = True

try:
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
    wait = WebDriverWait(driver, 20)
    print("✅ Kết nối Appium thành công!")
except Exception as e:
    print(f"❌ Không thể kết nối tới Appium Server: {e}")
    exit(1)

print("🔹 Bắt đầu kiểm thử...")

# Bước 1: Đăng nhập
try:
    wait.until(EC.presence_of_element_located((By.ID, "com.example.datdoanonline:id/username"))).send_keys("user1")
    wait.until(EC.presence_of_element_located((By.ID, "com.example.datdoanonline:id/password"))).send_keys("user1")
    wait.until(EC.element_to_be_clickable((By.ID, "com.example.datdoanonline:id/loginButton"))).click()
    print("✅ Bước 1: Đăng nhập thành công!")
except Exception as e:
    print(f"❌ Lỗi khi đăng nhập: {e}")
    driver.quit()
    exit(1)

# Bước 2: Mở giỏ hàng
try:
    wait.until(EC.element_to_be_clickable((By.ID, "com.example.datdoanonline:id/icon_giohang"))).click()
    print("✅ Bước 2: Đã mở giỏ hàng!")
except Exception as e:
    print(f"❌ Lỗi khi mở giỏ hàng: {e}")
    driver.quit()
    exit(1)

# Bước 3: Xóa từng sản phẩm trong giỏ hàng
try:
    print("🔍 Đang chờ ListView giỏ hàng...")
    wait.until(EC.presence_of_element_located((By.ID, "com.example.datdoanonline:id/listview_items")))
    print("✅ Đã tìm thấy ListView giỏ hàng!")
    
    while True:
        # Kiểm tra xem có phần tử số lượng nào không
        quantity_elements = driver.find_elements(By.ID, "com.example.datdoanonline:id/item_soluong")
        print(f"🔍 Số lượng phần tử item_soluong tìm thấy: {len(quantity_elements)}")
        
        if not quantity_elements:
            print("✅ Giỏ hàng đã rỗng!")
            break
            
        try:
            print("🔍 Đang tìm các phần tử của sản phẩm...")
            # Tìm lại các phần tử mỗi lần lặp để tránh StaleElementReferenceException
            quantity_element = wait.until(EC.presence_of_element_located((By.ID, "com.example.datdoanonline:id/item_soluong")))
            item_name_element = driver.find_element(By.ID, "com.example.datdoanonline:id/item_name")
            item_name = item_name_element.text if item_name_element else "Không xác định"
            
            current_quantity = int(quantity_element.text)
            print(f"🔍 Đang xóa '{item_name}' với số lượng {current_quantity}")
            
            while current_quantity > 0:
                # Tìm lại nút trừ trước mỗi lần nhấn
                minus_button = wait.until(EC.element_to_be_clickable((By.ID, "com.example.datdoanonline:id/items_tru")))
                minus_button.click()
                current_quantity -= 1
                print(f"🔻 Giảm số lượng '{item_name}' xuống còn {current_quantity}")
                time.sleep(1)  # Đợi UI cập nhật
            
            print(f"✅ Đã xóa '{item_name}' khỏi giỏ hàng!")
            time.sleep(2)  # Đợi danh sách cập nhật sau khi xóa
        
        except Exception as e:
            print(f"❌ Lỗi khi xóa sản phẩm: {e}")
            break

except Exception as e:
    print(f"❌ Lỗi trong quá trình xử lý giỏ hàng:")
    # print(f"❌ Lỗi trong quá trình xử lý giỏ hàng:{e}")
    if "NoSuchElementError" in str(e):
        print("✅ Giỏ hàng đã rỗng ngay từ đầu!")
    else:
        print("🔍 Nguồn trang hiện tại:")
        print(driver.page_source)

print("✅ Bước 3: Hoàn tất quá trình xóa sản phẩm trong giỏ hàng!")
driver.quit()
print("🔚 Kiểm thử hoàn tất!")