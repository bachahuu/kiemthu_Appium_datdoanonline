from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import time

# Cấu hình Appium
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "LDPlayer"
options.udid = "emulator-5554"
options.app_package = "com.example.datdoanonline"
options.app_activity = "com.example.datdoanonline.Activity.Login_Activity"
options.automation_name = "UiAutomator2"
options.no_reset = True

# Khởi tạo WebDriver
driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(10)

def swipe_down():
    windown_size = driver.get_window_size()
    driver.swipe(
        start_x=windown_size['width'] // 2,
        start_y=windown_size['height']*3 // 4,
        end_x=windown_size['width'] // 2,
        end_y=windown_size['height'] // 4,
        duration=800
    )
    time.sleep(1)

try:
    print("🔹 Đang đăng nhập...")

    # 1. Nhập thông tin đăng nhập
    username_field = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.example.datdoanonline:id/username'))
    )
    username_field.send_keys('user1')

    password_field = driver.find_element(AppiumBy.ID, 'com.example.datdoanonline:id/password')
    password_field.send_keys('user1')

    login_button = driver.find_element(AppiumBy.ID, 'com.example.datdoanonline:id/loginButton')
    login_button.click()
    print("✅ Đăng nhập thành công!")

    # 2. Chờ vào trang chủ và chọn image để vào trang thực đơn
    wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.ImageView[@resource-id="com.example.datdoanonline:id/img_thucdon"])[2]'))).click()
    print("✅ Bước 2: Đã chuyển sang trang thực đơn!")

    # 3. Chọn sản phẩm đầu tiên từ danh sách thực đơn
    wait.until(EC.element_to_be_clickable((By.XPATH, '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.example.datdoanonline:id/recyclerViewFood"]/android.widget.FrameLayout[1]/android.widget.LinearLayout'))).click()
    print("✅ Bước 3: Đã chọn sản phẩm đầu tiên trong thực đơn!")

    # 4. Thêm vào giỏ hàng
    wait.until(EC.element_to_be_clickable((By.ID, "com.example.datdoanonline:id/btn_themvaogiohang"))).click()
    print("✅ Bước 4: Sản phẩm đã được thêm vào giỏ hàng!")

    # 5. Nhấn vào nút giỏ hàng
    print("🔹 Điều hướng đến giỏ hàng...")
    cart_icon = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.example.datdoanonline:id/icon_giohang'))
    )
    cart_icon.click()
    print("✅ Mở giỏ hàng thành công!")

    # 6. Nhấn vào nút thanh toán
    print("🔹 Đang nhấn nút thanh toán...")
    payment_button = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.example.datdoanonline:id/btn_thanhtoan'))
    )
    payment_button.click()
    print("✅ Chuyển đến màn hình thanh toán!")

    # 7. Nhập thông tin giao hàng với cuộn tự động
    try:
        print("🔹 Nhập thông tin giao hàng...")
        address_field = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.example.datdoanonline:id/diachi_giaohang'))
        )
        address_field.clear()
        address_field.send_keys('113F ngõ 113 phố Cự Lộc')

        ho_feild = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.example.datdoanonline:id/ho'))
        )
        ho_feild.clear()
        ho_feild.send_keys('Hà')
        ten_feild = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.example.datdoanonline:id/ten'))
        )
        ten_feild.clear()
        ten_feild.send_keys('Bắc')

        phone_field = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.example.datdoanonline:id/sdt_kh'))
        )
        phone_field.clear()
        phone_field.send_keys('0964092903')
        time.sleep(2)

        print("✅ Nhập thông tin giao hàng thành công!")

    except Exception as e:
        print(f"❌ Lỗi khi nhập thông tin giao hàng: {str(e)}")

    # 8. Chọn mã giảm giá
    print("🔹 Đang chọn mã giảm giá...")
    for i in range(3):
        swipe_down()
        try:
            discount_code = wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Spinner[@resource-id="com.example.datdoanonline:id/spinner_magiamgia"]'))
            )
            if discount_code.is_displayed():
                break
        except:
         continue
        else:
            raise Exception("Không tìm thấy mã giảm giá!")
        
    discount_code.click()

    discount_code_option = wait.until(
        EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.CheckedTextView[@resource-id='android:id/text1' and @text='MGG2024B-Hoạt động']"))
    )
    discount_code_option.click()
    print("✅ Mã giảm giá đã được chọn!")

    # 9. Xác nhận đặt hàng
    print("🔹 Đang xác nhận đơn hàng...")
    confirm_button = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.example.datdoanonline:id/insert_don_hang'))
    )
    confirm_button.click()
    print("✅ Đã nhấn nút xác nhận đơn hàng!")

    # 10. Kiểm tra xác nhận thanh toán thành công
    print("🔹 Kiểm tra kết quả thanh toán...")
    success_message = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.RelativeLayout'))
    )

    assert success_message.is_displayed(), "Thanh toán không thành công!"
    print("🎉 Thanh toán thành công!")

    # 11. Nhấn nút Home để về trang chủ
    print("🔹 Đang quay về trang chủ...")
    home_button = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.example.datdoanonline:id/icon_home'))
    )
    home_button.click()
    print("✅ Đã về trang chủ!")

    # 12. Nhấn nút cài đặt để vào trang thông tin cá nhân
    print("🔹 Đang mở trang thông tin cá nhân...")
    settings_button = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.example.datdoanonline:id/img_thongtin'))
    )
    settings_button.click()
    print("✅ Đã mở trang thông tin cá nhân!")

    # 13. Nhấn nút đăng xuất
    print("🔹 Đang đăng xuất...")
    logout_button = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.example.datdoanonline:id/btn_dangXuat'))
    )
    logout_button.click()
    print("✅ Đã đăng xuất thành công!")

    # 14. Đăng nhập bằng tài khoản admin
    print("🔹 Đang đăng nhập bằng tài khoản admin...")
    username_field = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.example.datdoanonline:id/username'))
    )
    username_field.send_keys('admin')

    password_field = driver.find_element(AppiumBy.ID, 'com.example.datdoanonline:id/password')
    password_field.send_keys('admin')

    login_button = driver.find_element(AppiumBy.ID, 'com.example.datdoanonline:id/loginButton')
    login_button.click()
    print("✅ Đăng nhập admin thành công!")

    # 15. Kiểm tra màn hình giao diện admin
    print("🔹 Kiểm tra màn hình admin...")
    wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.LinearLayout'))
    )
    print("✅ Đã vào giao diện admin!")
    time.sleep(2)

    # 16. Nhấn vào biểu tượng đơn hàng
    print("🔹 Đang chuyển sang giao diện đơn hàng...")
    order_icon = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.example.datdoanonline:id/img_DonHang'))
    )
    order_icon.click()
    
    # 17. Kiểm tra màn hình quản lý đơn hàng
    wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.LinearLayout'))
    )
    print("✅ Đã vào giao diện quản lý đơn hàng!")
    
    # 18. Tìm kiếm đơn hàng bằng thông tin khách hàng đã nhập
    print("🔹 Đang tìm kiếm đơn hàng bằng thông tin khách hàng...")
    contact_info = "HàBắc-0964092903"
    customer_address = "113F ngõ 113 phố Cự Lộc"
    search_field = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.example.datdoanonline:id/searchEditText'))
    )
    search_field.clear()
    search_field.send_keys("0964092903")
    driver.find_element(AppiumBy.ID, 'com.example.datdoanonline:id/searchButton').click()
    time.sleep(2)
    
    # Kiểm tra kết quả tìm kiếm
    try:
        print("🔹 Đang xác minh thông tin đơn hàng...")
        
        contact_info_element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.example.datdoanonline:id/tvContactInfo"]'))
        )
        actual_contact = contact_info_element.text
        assert "HàBắc" in actual_contact and "0964092903" in actual_contact, f"Thông tin liên lạc không khớp: {actual_contact}"
        
        address_element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.example.datdoanonline:id/tvShippingAddress"]'))
        )
        actual_address = address_element.text
        if ":" in actual_address:
            actual_address_value = actual_address.split(":", 1)[1].strip()
            assert customer_address == actual_address_value, f"Địa chỉ không khớp: '{actual_address_value}' khác với '{customer_address}'"
        else:
            assert customer_address in actual_address, f"Địa chỉ không khớp: {actual_address}"
        
        expected_date = "2025-04-10"
        order_date_element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.example.datdoanonline:id/tvOrderDate"]'))
        )
        actual_date_text = order_date_element.text
        
        if ":" in actual_date_text:
            actual_date_value = actual_date_text.split(":", 1)[1].strip()
            assert expected_date == actual_date_value, f"Ngày đặt hàng không khớp: '{actual_date_value}' khác với '{expected_date}'"
        else:
            assert expected_date in actual_date_text, f"Ngày đặt hàng không khớp: {actual_date_text}"
        
        print("✅ Đã xác minh đơn hàng mới với thông tin chính xác!")
        driver.save_screenshot("verified_order.png")
        print("📸 Đã lưu ảnh chụp màn hình đơn hàng")
        
    except Exception as e:
        print(f"❌ Không tìm thấy đơn hàng: {str(e)}")
        driver.save_screenshot("order_not_found.png")
        raise

except Exception as e:
    print(f"❌ Test thất bại: {str(e)}")
    driver.save_screenshot("test_failure.png")

finally:
    print("🔹 Script đã hoàn tất, giữ ứng dụng mở ở trang cuối cùng.")
    driver.quit()
    print("✅ Đã đóng WebDriver!")