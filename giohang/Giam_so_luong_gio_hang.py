#Sửa số lượng sản phẩm trong giỏ hàng
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cấu hình Appium với Android UIAutomator2
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "emulator-5554"
options.app_package = "com.example.datdoanonline"
options.app_activity = "com.example.datdoanonline.Activity.Login_Activity"
options.automation_name = "UiAutomator2"
options.no_reset = True  # Giữ trạng thái ứng dụng

# Kết nối đến Appium Server
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)
wait = WebDriverWait(driver, 10)  # Chờ tối đa 10 giây

print("🔹 Bắt đầu kiểm thử...")

# Bước 1: Đăng nhập vào ứng dụng
wait.until(EC.presence_of_element_located((By.ID, "com.example.datdoanonline:id/username"))).send_keys("user1")
wait.until(EC.presence_of_element_located((By.ID, "com.example.datdoanonline:id/password"))).send_keys("user1")
wait.until(EC.element_to_be_clickable((By.ID, "com.example.datdoanonline:id/loginButton"))).click()
print("✅ Bước 1: Đăng nhập thành công!")

# Bước 2: Kiểm tra giỏ hàng
wait.until(EC.element_to_be_clickable((By.ID, "com.example.datdoanonline:id/icon_giohang"))).click()
print("✅ Bước 2: Đã mở giỏ hàng!")

# Bước 3: Giảm số lượng sản phẩm lên 3 lần
for i in range(3):
    btn_plus = wait.until(EC.element_to_be_clickable((By.ID, "com.example.datdoanonline:id/items_tru")))
    btn_plus.click()
    print(f"✅ Bước 3.{i+1}: Đã nhấn giảm số lượng {i+1} lần.")

print("✅ Bước 3: Đã giảm số lượng sản phẩm lên 3!")


# Kiểm tra sản phẩm đã thêm vào giỏ hàng
cart_items = driver.find_elements(By.XPATH, "//android.widget.ListView[@resource-id='com.example.datdoanonline:id/listview_items']/android.view.ViewGroup/android.widget.LinearLayout")
if len(cart_items) > 0:
    print("🎉✅ Kiểm thử thành công: Sản phẩm đã được thêm vào giỏ hàng!")
else:
    print("❌ Kiểm thử thất bại: Không tìm thấy sản phẩm trong giỏ hàng.")

# Đóng ứng dụng
# driver.quit()
print("🔚 Kiểm thử hoàn tất!")
