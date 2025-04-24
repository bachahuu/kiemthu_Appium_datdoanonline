from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

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
def swipe_down_2(driver):
    window_size = driver.get_window_size()
    driver.swipe(
        start_x=window_size['width'] // 2,
        start_y=int(window_size['height'] * 0.7),
        end_x=window_size['width'] // 2,
        end_y=int(window_size['height'] * 0.3),
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
def swipe_up(driver):
    window_size = driver.get_window_size()
    driver.swipe(
        start_x=window_size['width'] // 2,
        start_y=int(window_size['height'] * 0.3),
        end_x=window_size['width'] // 2,
        end_y=int(window_size['height'] * 0.7),
        duration=800
    )
    time.sleep(1)

def get_all_visible_order_ids(driver):
    elements = driver.find_elements(AppiumBy.ID, 'com.example.datdoanonline:id/tvOrderId')
    return [el.text for el in elements]

def check_order_deleted_scroll_down_then_up(driver, wait, order_code="DH5", max_swipes=20):
    xpath = f'//android.widget.TextView[@resource-id="com.example.datdoanonline:id/tvOrderId" and @text="Mã đơn: {order_code}"]'

    print("🔽 Cuộn xuống kiểm tra...")
    last_ids = []
    for i in range(max_swipes):
        try:
            driver.find_element(AppiumBy.XPATH, xpath)
            print(f"❌ Tìm thấy {order_code} khi cuộn xuống lần {i + 1}")
            return False
        except:
            current_ids = get_all_visible_order_ids(driver)
            if current_ids == last_ids:
                print("⛔ Đã cuộn đến đáy danh sách.")
                break
            last_ids = current_ids
            swipe_down_2(driver)

    print("🔼 Cuộn ngược lên kiểm tra...")
    last_ids = []
    for i in range(max_swipes):
        try:
            driver.find_element(AppiumBy.XPATH, xpath)
            print(f"❌ Tìm thấy {order_code} khi cuộn lên lần {i + 1}")
            return False
        except:
            current_ids = get_all_visible_order_ids(driver)
            if current_ids == last_ids:
                print("⛔ Đã cuộn về đầu danh sách.")
                break
            last_ids = current_ids
            swipe_up(driver)

    print(f"✅ Không tìm thấy {order_code} sau khi cuộn hết xuống và lên.")
    return True


def test_delete_order_success():
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    try:
        login_admin(driver, wait)
        open_order_page(driver, wait)

        print("🔹 Bắt đầu test: TC_ORDER_1 : xoá đơn hàng ở trạng thái : 'Đã Huỷ'  ")
        order_element = find_order_dh5(driver, wait)
        if not order_element:
         return  # hoặc raise Exception nếu muốn dừng test
        # Tìm đơn hàng có trạng thái "Chờ xử lý"
        order_id = wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,'//android.widget.TextView[@resource-id="com.example.datdoanonline:id/tvOrderId" and @text="Mã đơn: DH5"]')))
        print("✅  đơn hàng : DH5")
        order_element = wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.example.datdoanonline:id/tvOrderStatus" and @text="Trạng thái:Đã Hủy"]')))
        print("✅  trạng thái ban đầu 'Đã Hủy'")
        time.sleep(1)

        # Nhấn vào nút xoá
        delete_order_button = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, '(//android.widget.Button[@resource-id="com.example.datdoanonline:id/btnDeleteOrder"])[2]')))
        delete_order_button.click()
        print("🔹 Đã nhấn nút xoá")
        time.sleep(2)
        # xác nhận xoá
        delete_order = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, '//android.widget.Button[@resource-id="android:id/button1"]')))
        delete_order.click()
        print("🔹 Đã nhấn nút xoá")
        time.sleep(2)
       # Kiểm tra lại xem đơn hàng còn không
        print("🔍 Kiểm tra đơn hàng DH5 sau khi xoá bằng cách cuộn xuống rồi cuộn lên...")
        is_deleted = check_order_deleted_scroll_down_then_up(driver, wait, order_code="DH5")
        assert is_deleted, "❌ Đơn hàng DH5 vẫn còn sau khi xoá!"
        print("🎉 TC_ORDER_006: Đơn hàng DH5 đã được xoá thành công!")
    except TimeoutException as e:
        print(f"❌ Timeout xảy ra: {str(e)}")
    finally:
        time.sleep(2)
        driver.quit()
        #testcase2: Không cho xóa đơn hàng đã giao
def test_delete_non_canceled_order():
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)

    try:
        login_admin(driver, wait)
        open_order_page(driver, wait)

        print("🔹 Bắt đầu test: TC_ORDER_009 - Không cho xóa đơn hàng chưa hủy")
        
        # Tìm đơn hàng cụ thể có mã DH2
        order_id_element = wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.example.datdoanonline:id/tvOrderId" and @text="Mã đơn: DH2"]')))
        print("✅ Đã tìm đơn hàng: Mã đơn: DH2")
        
        # Kiểm tra trạng thái của đơn hàng
        order_status_element = wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.example.datdoanonline:id/tvOrderStatus" and @text="Trạng thái:Đang chuẩn bị"]')))
        status_text = order_status_element.text.replace("Trạng thái:", "")
        print(f"✅ Trạng thái đơn hàng: {status_text}")
        
        # Nhấn vào nút xóa cho đơn hàng DH2
        delete_order_icon = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, '(//android.widget.Button[@resource-id="com.example.datdoanonline:id/btnDeleteOrder"])[2]')))
        delete_order_icon.click()
        print("🔹 Đã nhấn nút xóa")
            # xác nhận xoá
        delete_order = wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, '//android.widget.Button[@resource-id="android:id/button1"]')))
        delete_order.click()
        print("🔹 Đã nhấn nút xoá")
        time.sleep(2)
        # Kiểm tra toast message
        try:
            # Kiểm tra nếu xuất hiện toast message "Đã xóa đơn hàng" - đây là LỖI vì đơn không phải "Đã hủy"
            toast_deleted = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.Toast[@text="Đã xóa đơn hàng"]')))
            print("❌ LỖI: Hệ thống cho phép xóa đơn hàng 'Đang chuẩn bị' và hiển thị thông báo 'Đã xóa đơn hàng'")
            
            # Kiểm tra xem đơn hàng có còn trong danh sách không
            time.sleep(2)  # Đợi toast biến mất
            try:
                driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.example.datdoanonline:id/tvOrderId" and @text="Mã đơn: DH2"]')
                print("⚠️ Đơn hàng vẫn còn trong danh sách mặc dù đã có thông báo xóa thành công")
            except:
                print("❌ LỖI: Đơn hàng đã bị xóa khỏi danh sách")
            print("❌ TEST FAILED: Hệ thống cho phép xóa đơn hàng chưa hủy")
            
        except:
            # Không có toast message "Đã xóa đơn hàng" - kiểm tra có thông báo lỗi khác không
            try:
                error_toast = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.Toast')))
                print(f"✅ Đúng: Đơn hàng không được xóa, hiển thị thông báo: '{error_toast.text}'")
            except:
                print("✅ Đúng: Đơn hàng không được xóa, không có thông báo")
            
            # Kiểm tra đơn hàng vẫn còn trong danh sách
            try:
                driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.example.datdoanonline:id/tvOrderId" and @text="Mã đơn: DH2"]')
                print("✅ Đúng: Đơn hàng vẫn còn trong danh sách sau khi thử xóa")
                print("✅ TEST PASSED: Hệ thống không cho phép xóa đơn hàng chưa hủy")
            except:
                print("❌ LỖI: Đơn hàng không còn trong danh sách mặc dù không có thông báo xóa thành công")
                print("❌ TEST FAILED: Đơn hàng đã bị xóa mặc dù không phải trạng thái 'Đã hủy'")
        
    except Exception as e:
        print(f"❌ Test case TC_ORDER_009 FAILED: {str(e)}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    test_delete_order_success()
    test_delete_non_canceled_order()
    