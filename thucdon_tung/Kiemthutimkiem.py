from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')  # Sửa lỗi Unicode trên Windows

# Cấu hình Appium
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "LDPlayer"
options.udid = "emulator-5554"
options.app_package = "com.example.datdoanonline"
options.app_activity = "com.example.datdoanonline.Activity.Login_Activity"
options.automation_name = "UiAutomator2"

# Khởi tạo Appium driver
driver = webdriver.Remote("http://localhost:4723/wd/hub", options=options)

time.sleep(5)  # Chờ ứng dụng tải xong

try:
    wait = WebDriverWait(driver, 20)  # Tăng thời gian chờ
    
    # Đăng nhập với tài khoản admin
    username_field = wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.example.datdoanonline:id/username")))
    password_field = wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.example.datdoanonline:id/password")))
    login_button = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.example.datdoanonline:id/loginButton")))
    
    username_field.send_keys("admin")
    password_field.send_keys("admin")
    login_button.click()
    
    time.sleep(5)  # Chờ đăng nhập thành công
    
    # Chuyển đến chức năng thực đơn
    menu_button = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.example.datdoanonline:id/img_ThucDon")))
    menu_button.click()
    
    # Kiểm thử chức năng tìm kiếm sản phẩm
    search_box = wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.example.datdoanonline:id/txt_search_food")))
    search_box.send_keys("Cheese Pizza")
    
    search_button = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.example.datdoanonline:id/txt_search_food")))
    search_button.click()
    
    try:
        results = wait.until(EC.visibility_of_element_located((AppiumBy.ID, "android.widget.ScrollView")))

        # Kiểm tra xem có sản phẩm trong danh sách kết quả không
        products = driver.find_elements(AppiumBy.ID, "com.example.datdoanonline:id/recyclerViewfood")
        if products:
            print("Tìm kiếm sản phẩm thành công!")
        else:
            print("Tìm kiếm không thành công! Không tìm thấy sản phẩm nào.")

    except:
        print("Tìm kiếm không thành công! Không tìm thấy sản phẩm nào.")

    # Giữ ứng dụng mở, không thoát
    print("Ứng dụng vẫn đang chạy. Bạn có thể kiểm tra thủ công trên thiết bị.")
    while True:
        time.sleep(1)  # Giữ chương trình chạy mà không đóng ứng dụng

except Exception as e:
    print(f"Lỗi xảy ra: {e}")
