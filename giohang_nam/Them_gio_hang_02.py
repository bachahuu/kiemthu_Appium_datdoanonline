#Thêm 1 sản phẩm vào giỏ hàng tăng thêm số lượng
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

# Bước 2: Chờ vào trang chủ và chọn image để vào trang thực đơn
wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.ImageView[@resource-id="com.example.datdoanonline:id/img_thucdon"])[2]'))).click()
print("✅ Bước 2: Đã chuyển sang trang thực đơn!")

# Bước 3: Chọn món Cheese Pizza (vị trí thứ 2)
item_added_name = "Gà sốt mắm ngọt"
wait.until(EC.element_to_be_clickable((By.XPATH, '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.example.datdoanonline:id/recyclerViewFood"]/android.widget.FrameLayout[1]/android.widget.LinearLayout'))).click()
print(f"✅ Bước 3: Đã chọn món {item_added_name} trong thực đơn!")

# Bước 4: Tăng số lượng sản phẩm lên 3
btn_plus = wait.until(EC.element_to_be_clickable((By.ID, "com.example.datdoanonline:id/btn_plus")))
btn_plus.click()  # Số lượng lên 2
btn_plus.click()  # Số lượng lên 3
print("✅ Bước 4: Tănng số lượng sản phẩm lên 3!")

# Bước 5: Thêm vào giỏ hàng
wait.until(EC.element_to_be_clickable((By.ID, "com.example.datdoanonline:id/btn_themvaogiohang"))).click()
print("✅ Bước 5: Sản phẩm đã được thêm vào giỏ hàng!")

# Bước 6: Kiểm tra giỏ hàng
wait.until(EC.element_to_be_clickable((By.ID, "com.example.datdoanonline:id/icon_giohang"))).click()
print("✅ Bước 6: Đã mở giỏ hàng!")

# Bước 6: Kiểm tra món vừa thêm đã có trong giỏ hàng chưa
xpath_check = f'//android.widget.TextView[@resource-id="com.example.datdoanonline:id/item_name" and @text="{item_added_name}"]'
try:
    item_element = driver.find_element(By.XPATH, xpath_check)
    if item_element.is_displayed():
        print(f"🎉✅ Kiểm thử thành công: Món {item_added_name} đã được thêm vào giỏ hàng!")
    else:
        print(f"❌ Kiểm thử thất bại: Món {item_added_name} không hiển thị trong giỏ hàng.")
except:
    print(f"❌ Kiểm thử thất bại: Không tìm thấy món {item_added_name} trong giỏ hàng.")

# Đóng ứng dụng
# driver.quit()
print("🔚 Kiểm thử hoàn tất!")
