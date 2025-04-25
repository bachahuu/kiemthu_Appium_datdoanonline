import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cấu hình Appium
desired_caps = {
    "platformName": "Android",
    "appium:deviceName": "LDPlayer",
    "appium:udid": "emulator-5554",
    "appium:appPackage": "com.example.datdoanonline",
    "appium:appActivity": "com.example.datdoanonline.Activity.Login_Activity",
    "appium:automationName": "UiAutomator2",
    "appium:noReset": True,
    "appium:fullReset": False
}

def reset_app(driver):
    driver.terminate_app("com.example.datdoanonline")
    time.sleep(2)
    driver.activate_app("com.example.datdoanonline")
    time.sleep(3)

def kiem_tra_dang_nhap(driver, ten_nguoi_dung, mat_khau, activity_du_kien, loai_tai_khoan, thong_bao_du_kien):
    print(f"\n[TEST] {loai_tai_khoan} - Username: '{ten_nguoi_dung}' | Password: '{mat_khau}'")
    
    driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/username").clear()
    driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/password").clear()
    driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/username").send_keys(ten_nguoi_dung)
    driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/password").send_keys(mat_khau)
    driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/loginButton").click()

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.Toast"))
        )
        toast = driver.find_element(AppiumBy.XPATH, "//android.widget.Toast")
        noi_dung = toast.get_attribute("text")
        if thong_bao_du_kien in noi_dung:
            print(f"✅ Toast đúng: {noi_dung}")
        else:
            print(f"❌ Toast sai. Thực tế: '{noi_dung}' | Kỳ vọng: '{thong_bao_du_kien}'")
    except:
        print("⚠ Không tìm thấy Toast.")

    activity = driver.current_activity
    if activity == activity_du_kien:
        print(f"✅ Activity đúng: {activity}")
    else:
        print(f"❌ Activity sai. Hiện tại: '{activity}' | Kỳ vọng: '{activity_du_kien}'")

    reset_app(driver)

# Danh sách test case đúng như bảng
test_cases = [
    {
        "ten": "user1",
        "matkhau": "user1",
        "activity": ".Activity.Trangchu_Activity",
        "loai": "Đăng nhập thành công với User",
        "toast": "Đăng nhập thành công với quyền User"
    },
    {
        "ten": "wronguser",
        "matkhau": "user1",
        "activity": ".Activity.Login_Activity",
        "loai": "Sai tài khoản",
        "toast": "Tên người dùng hoặc mật khẩu không hợp lệ"
    },
    {
        "ten": "",
        "matkhau": "user1",
        "activity": ".Activity.Login_Activity",
        "loai": "Trường hợp rỗng tài khoản",
        "toast": "Tên người dùng hoặc mật khẩu không hợp lệ"
    },
    {
        "ten": "user1",
        "matkhau": "",
        "activity": ".Activity.Login_Activity",
        "loai": "Trường nhập trống mật khẩu",
        "toast": "Vui lòng nhập đầy đủ thông tin"
    },
    {
        "ten": "wronguser",
        "matkhau": "wronguser",
        "activity": ".Activity.Login_Activity",
        "loai": "Sai cả tài khoản và mật khẩu",
        "toast": "Tên người dùng hoặc mật khẩu không hợp lệ"
    }
]

# Khởi chạy Appium
try:
    print("🔌 Kết nối Appium server...")
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=UiAutomator2Options().load_capabilities(desired_caps))
    print("✅ Kết nối thành công.")
    time.sleep(5)

    for tc in test_cases:
        kiem_tra_dang_nhap(
            driver,
            ten_nguoi_dung=tc["ten"],
            mat_khau=tc["matkhau"],
            activity_du_kien=tc["activity"],
            loai_tai_khoan=tc["loai"],
            thong_bao_du_kien=tc["toast"]
        )

except Exception as e:
    print(f"❌ Lỗi: {str(e)}")
finally:
    if 'driver' in locals():
        driver.quit()
        print("🛑 Đã đóng Appium driver.")
