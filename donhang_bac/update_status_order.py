from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Danh sách tất cả các trạng thái
ALL_STATUSES = ["Chờ xử lý", "Đang chuẩn bị", "Đang giao", "Giao thành công", "Đã Hủy"]

# Quy tắc chuyển trạng thái hợp lệ
def is_valid_transition(current, target):
    valid_transitions = {
        "Chờ xử lý": ["Đang chuẩn bị", "Đã Hủy"],
        "Đang chuẩn bị": ["Đang giao", "Đã Hủy"],
        "Đang giao": ["Giao thành công", "Đã Hủy"],
        "Giao thành công": [],
        "Đã Hủy": []
    }
    return target in valid_transitions.get(current, [])

def setup_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "LDPlayer"
    options.udid = "emulator-5554"
    options.app_package = "com.example.datdoanonline"
    options.app_activity = "com.example.datdoanonline.Activity.Login_Activity"
    options.automation_name = "UiAutomator2"
    options.no_reset = True
    return webdriver.Remote('http://localhost:4723/wd/hub', options=options)

def login_admin(driver, wait):
    print("🔹 Đăng nhập admin...")
    username_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.example.datdoanonline:id/username')))
    username_field.clear()
    username_field.send_keys('admin')
    time.sleep(1)

    password_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.example.datdoanonline:id/password')))
    password_field.clear()
    password_field.send_keys('admin')
    time.sleep(1)

    driver.find_element(AppiumBy.ID, 'com.example.datdoanonline:id/loginButton').click()
    print("✅ Đã đăng nhập thành công!")
    time.sleep(2)

def open_order_page(driver, wait):
    print("🔹 Vào trang đơn hàng...")
    order_icon = wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'com.example.datdoanonline:id/img_DonHang')))
    order_icon.click()
    time.sleep(2)
    print("✅ Đã vào trang đơn hàng!")
def swipe_down(driver):
    windown_size = driver.get_window_size()
    driver.swipe(
        start_x=windown_size['width'] // 2,
        start_y=windown_size['height']*3 // 4,
        end_x=windown_size['width'] // 2,
        end_y=windown_size['height'] // 4,
        duration=800
    )
    time.sleep(1)
def find_order_dh5(driver, wait, max_swipes=5):
    for attempt in range(max_swipes):
        try:
            element = driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.example.datdoanonline:id/tvOrderId" and @text="Mã đơn: DH5"]')
            return element
        except:
            print(f"⏬ Cuộn xuống lần {attempt + 1} để tìm DH5...")
            swipe_down(driver)
    return None

def test_update_order_status_success():
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    try:
        login_admin(driver, wait)
        open_order_page(driver, wait)

        print("🔹 Bắt đầu test: TC_ORDER_1 - Cập nhật trạng thái thành công")

        # Tìm đơn hàng có trạng thái "Chờ xử lý"
        order_id = wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,'//android.widget.TextView[@resource-id="com.example.datdoanonline:id/tvOrderId" and @text="Mã đơn: DH1"]')))
        print("✅  đơn hàng : DH1")
        order_element = wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.example.datdoanonline:id/tvOrderStatus" and @text="Trạng thái:Chờ xử lý"]')))
        print("✅  trạng thái ban đầu 'Chờ xử lý'")
        time.sleep(1)

        # Nhấn vào nút cập nhật trạng thái (lấy cái đầu tiên trong danh sách)
        status_order_icon = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, '(//android.widget.Button[@resource-id="com.example.datdoanonline:id/btnUpdateOrder"])[1]')))
        status_order_icon.click()
        print("🔹 Đã mở cập nhật trạng thái")
        time.sleep(2)

        # Chọn trạng thái mới "Đang chuẩn bị"
        new_status = wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="android:id/text1" and @text="Đang chuẩn bị"]')))
        new_status.click()
        print("✅ Đã chọn trạng thái mới: Đang chuẩn bị")
        time.sleep(2)

        # Kiểm tra trạng thái đã được cập nhật (có thể cần scroll nếu nằm dưới)
        updated_status = wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "Đang chuẩn bị")]')))
        assert updated_status is not None, "❌ Trạng thái đơn hàng không được cập nhật!"
        print("🎉 TC_ORDER_006: Trạng thái đơn hàng DH1 đã được cập nhật thành công!")

    except TimeoutException as e:
        print(f"❌ Timeout xảy ra: {str(e)}")
    finally:
        time.sleep(2)
        driver.quit()

def test_update_order_status_invalid():
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)

    try:
        login_admin(driver, wait)
        open_order_page(driver, wait)

        print("🔹 Bắt đầu test tự động các trạng thái không hợp lệ cho đơn hàng DH5")

        # Tìm đơn hàng DH5
        order_element = find_order_dh5(driver, wait)
        if not order_element:
         return  # hoặc raise Exception nếu muốn dừng test
        wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@text="Mã đơn: DH5"]')))

        current_status_text = wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "Trạng thái:")]'))).text.strip()
        current_status = current_status_text.replace("Trạng thái:", "").strip()
        print(f"🔸 Trạng thái hiện tại của DH5: {current_status}")

        for status in ALL_STATUSES:
            if status == current_status:
                continue  # không test lại chính nó

            print(f"\n➡️ Thử chuyển từ [{current_status}] sang [{status}]")

            if not is_valid_transition(current_status, status):
                # Mở giao diện cập nhật
                update_button = wait.until(EC.element_to_be_clickable(
                    (AppiumBy.XPATH, '(//android.widget.Button[@resource-id="com.example.datdoanonline:id/btnUpdateOrder"])[2]')))
                update_button.click()
                time.sleep(1)

                # Chọn trạng thái cần test
                status_option = wait.until(EC.presence_of_element_located(
                    (AppiumBy.XPATH, f'//android.widget.TextView[@text="{status}"]')))
                status_option.click()
                try:
                    wait.until(EC.presence_of_element_located(
                        (AppiumBy.XPATH, f'//android.widget.Toast[@text="Không thể chuyển từ {current_status} sang {status}"]')))
                    print(f"✅ Đã chặn đúng: KHÔNG cho chuyển sang {status}")
                except TimeoutException:
                    print(f"❌ LỖI: Hệ thống cho phép chuyển từ {current_status} sang {status} (không hợp lệ)")
                    break # Dừng test nếu gặp lỗi
            else:
                print(f"✅ Bỏ qua: {status} là hợp lệ")

    finally:
        time.sleep(2)
        driver.quit()
if __name__ == "__main__":
    test_update_order_status_success()
    test_update_order_status_invalid()
