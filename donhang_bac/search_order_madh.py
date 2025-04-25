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

    password_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.example.datdoanonline:id/password')))
    password_field.clear()
    password_field.send_keys('admin')

    driver.find_element(AppiumBy.ID, 'com.example.datdoanonline:id/loginButton').click()
    print("✅ Đã đăng nhập thành công!")

def open_order_page(driver, wait):
    print("🔹 Vào trang đơn hàng...")
    order_icon = wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'com.example.datdoanonline:id/img_DonHang')))
    order_icon.click()
    time.sleep(2)
    print("✅ Đã vào trang đơn hàng!")
#truyền biến đầu vào 1 mã đơn của 1 đơn hàng ngẫu nhiên
def test_search_order_by_id():
    driver = setup_driver()
    wait = WebDriverWait(driver, 15)
    try:
        login_admin(driver, wait)
        open_order_page(driver, wait)
#đầu vào DH1
        test_order_id = "DH1"
        print(f"🔹 Tìm kiếm đơn hàng với mã: {test_order_id}")
        search_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.example.datdoanonline:id/searchEditText')))
        search_field.clear()
        search_field.send_keys(test_order_id)

        search_button = wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'com.example.datdoanonline:id/searchButton')))
        search_button.click()
        time.sleep(3)
        driver.save_screenshot("search_results.png")

        found_order = None
        try:
            found_order = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, f'//android.widget.TextView[contains(@text, "Mã đơn: {test_order_id}")]')))
            print(f"✅ Đã tìm thấy đơn hàng: {found_order.text}")
        except TimeoutException:
            print("⚠️ Không tìm thấy bằng XPath, thử phương pháp khác...")
            elements = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            for element in elements:
                if test_order_id.lower() in element.text.lower():
                    print(f"✅ Đã tìm thấy trong danh sách: {element.text}")
                    found_order = element
                    break
            if not found_order:
                raise Exception("Không tìm thấy đơn hàng")

        print("🔹 Phân tích kết quả tìm kiếm...")
        # đầu ra thông tin đơn hàng
        order_details = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        order_info = {}
        for element in order_details:
            text = element.text
            if ":" in text:
                key, value = text.split(":", 1)
                order_info[key.strip()] = value.strip()
        print("📋 Thông tin đơn hàng:")
        for k, v in order_info.items():
            print(f"  - {k}: {v}")

        if "Mã đơn" in order_info and order_info["Mã đơn"].upper() == test_order_id.upper():
            print(f"✅ Mã đơn trùng khớp: {test_order_id}")
        else:
            print("❌ Mã đơn không trùng khớp")

        print("✅ Hoàn thành kiểm thử tìm kiếm mã đúng!")
        
    except Exception as e:
        print(f"❌ Lỗi kiểm thử: {str(e)}")
        driver.save_screenshot("test_failure_id.png")
    finally:
        driver.quit()
        print("✅ Đã đóng ứng dụng")

#testcase 2 : truyền biến đầu vào 1 giá trị bất kỳ
def test_search_order_invalid_id():
    driver = setup_driver()
    wait = WebDriverWait(driver, 15)
    try:
        login_admin(driver, wait)
        open_order_page(driver, wait)
# đầu vào một giá trị bất kỳ
        invalid_order_id = "abcd"
        print(f"🔹 Tìm kiếm với mã không tồn tại: {invalid_order_id}")
        search_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.example.datdoanonline:id/searchEditText')))
        search_field.clear()
        search_field.send_keys(invalid_order_id)

        search_button = wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'com.example.datdoanonline:id/searchButton')))
        search_button.click()

        print("🔹 Chờ Toast thông báo...")
        toast_locator = (AppiumBy.XPATH, "//android.widget.Toast[@text='Không tìm thấy đơn hàng phù hợp']")
        time.sleep(3)
        try:
            # đầu ra 
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(toast_locator))
            print("✅ Đã hiển thị Toast: Không tìm thấy đơn hàng phù hợp")
        except TimeoutException:
            print("❌ Không tìm thấy Toast. Chức năng có thể bị lỗi.")
            driver.save_screenshot("toast_not_found.png")
            raise

        print("✅ Hoàn thành kiểm thử tìm kiếm sai mã!")
    except Exception as e:
        print(f"❌ Lỗi kiểm thử: {str(e)}")
        driver.save_screenshot("test_failure_invalid_id.png")
    finally:
        driver.quit()
        print("✅ Đã đóng ứng dụng")

if __name__ == "__main__":
    test_search_order_by_id()
    test_search_order_invalid_id()
