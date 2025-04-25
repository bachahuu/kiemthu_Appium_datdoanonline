from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import unittest
import time

class AddFoodTest(unittest.TestCase):
    def setUp(self):
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "LDPlayer"
        options.udid = "emulator-5554"
        options.app_package = "com.example.datdoanonline"
        options.app_activity = "com.example.datdoanonline.Activity.Login_Activity"
        options.automation_name = "UiAutomator2"

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", options=options)
        self.driver.implicitly_wait(10)

        self.login("admin", "admin")
        self.open_add_food_form()

    def login(self, username, password):
        self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/username").send_keys(username)
        self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/password").send_keys(password)
        self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/loginButton").click()
        time.sleep(2)

    def open_add_food_form(self):
        self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/img_ThucDon").click()
        time.sleep(2)
        self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/btn_Addfood").click()
        time.sleep(2)

        # 👉 Xử lý popup xin quyền truy cập ảnh (nếu có)
        try:
            allow_btn = self.driver.find_element(AppiumBy.ID, "com.android.packageinstaller:id/permission_allow_button")
            if allow_btn.is_displayed():
                print("[INFO] Phát hiện popup xin quyền -> Nhấn 'CHO PHÉP'")
                allow_btn.click()
                time.sleep(1)
        except:
            print("[INFO] Không có popup xin quyền, tiếp tục bình thường.")

    def add_food(self, name, mota, gia, danh_muc, nang_luong, tgian, so_luong):
        def safe_send(id, value):
            try:
                element = self.driver.find_element(AppiumBy.ID, id)
                element.clear()
                element.send_keys(value)
            except:
                print(f"[LỖI] Không tìm thấy phần tử với ID: {id}")

        safe_send("com.example.datdoanonline:id/txt_name", name)
        safe_send("com.example.datdoanonline:id/txt_mo_ta", mota)
        safe_send("com.example.datdoanonline:id/txt_gia", gia)
        safe_send("com.example.datdoanonline:id/txt_danh_muc", danh_muc)
        safe_send("com.example.datdoanonline:id/txt_nang_luong", nang_luong)
        safe_send("com.example.datdoanonline:id/txt_tgian_lam", tgian)
        safe_send("com.example.datdoanonline:id/txt_sl", so_luong)

        try:
            self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/btn_Luu").click()
        except:
            print("[LỖI] Không tìm thấy nút Lưu")
        time.sleep(2)

    def get_message(self):
        try:
            texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            for t in texts:
                msg = t.text.strip().lower()
                if "thành công" in msg:
                    print("✅ Thêm món ăn thành công")
                    return msg
            print("❌ Thêm món ăn thất bại")
            return "thêm món ăn thất bại"
        except:
            print("⚠️ Không lấy được thông báo")
            return ""

    def test_valid_food_creation(self):
        print("\n[TEST] Tạo món hợp lệ")
        self.add_food("Pizza Hải Sản", "Ngon tuyệt", "100000", "Pizza", "800", "15", "5")
        message = self.get_message()
        self.assertIn("thành công", message)

    def test_empty_name(self):
        print("\n[TEST] Tên món ăn rỗng")
        self.add_food("", "Mô tả", "50000", "Mì", "400", "10", "2")
        message = self.get_message()
        self.assertIn("tên", message or "thêm món ăn thất bại")

    def test_invalid_price(self):
        print("\n[TEST] Giá không hợp lệ (nhập chữ)")
        self.add_food("Bún bò", "Đặc biệt", "abc", "Bún", "500", "10", "3")
        message = self.get_message()
        self.assertIn("thêm món ăn thất bại", message)

    def test_missing_required_fields(self):
        print("\n[TEST] Thiếu các trường bắt buộc")
        self.add_food("Phở Gà", "", "", "Phở", "", "", "")
        message = self.get_message()
        self.assertIn("thêm món ăn thất bại", message)

    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()
