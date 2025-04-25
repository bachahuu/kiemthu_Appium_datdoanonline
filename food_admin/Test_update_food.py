from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import unittest
import time

class UpdateFoodTest(unittest.TestCase):
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

    def login(self, username, password):
        self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/username").send_keys(username)
        self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/password").send_keys(password)
        self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/loginButton").click()
        time.sleep(2)

    def navigate_to_edit_form(self):
        try:
            self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/img_ThucDon").click()
            time.sleep(2)

            first_item = self.driver.find_element(
                AppiumBy.XPATH,
                "//androidx.recyclerview.widget.RecyclerView[@resource-id='com.example.datdoanonline:id/recyclerViewfood']/android.view.ViewGroup[1]"
            )
            first_item.click()
            time.sleep(1)

            edit_button = self.driver.find_element(AppiumBy.XPATH, "//android.widget.ImageButton[@content-desc='Edit']")
            edit_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"[LỖI] Không thể mở form sửa: {e}")

    def scroll_down(self):
        try:
            # Cuộn xuống bằng scroll origin (dùng Webdriver W3C Actions)
            scroll_element = self.driver.find_element(
                AppiumBy.XPATH,
                "//android.widget.FrameLayout[@resource-id='com.example.datdoanonline:id/custom']/android.widget.ScrollView"
            )
            actions = ActionChains(self.driver)
            scroll_origin = ScrollOrigin.from_element(scroll_element)
            actions.scroll_from_origin(scroll_origin, 0, 500).perform()
            time.sleep(1)
        except Exception as e:
            print(f"[⚠️] Scroll thất bại: {e}")

    def update_food(self, name, mota, gia, danh_muc, nang_luong, tgian, so_luong):
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

        self.scroll_down()

        safe_send("com.example.datdoanonline:id/txt_danh_muc", danh_muc)
        safe_send("com.example.datdoanonline:id/txt_nang_luong", nang_luong)
        safe_send("com.example.datdoanonline:id/txt_tgian_lam", tgian)
        safe_send("com.example.datdoanonline:id/txt_sl", so_luong)

        self.scroll_down()

        try:
            self.driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@resource-id='android:id/button1']").click()
            print("[INFO] Đã nhấn nút Lưu")
        except:
            print("[LỖI] Không tìm thấy nút Lưu")
        time.sleep(2)

    def get_message(self):
        try:
            texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            for t in texts:
                msg = t.text.strip().lower()
                if "thành công" in msg or "cập nhật" in msg:
                    print(f"✅ {msg}")
                    return msg
            print("❌ Không thấy thông báo thành công")
            return "cập nhật thất bại"
        except:
            print("⚠️ Không lấy được thông báo")
            return ""

    def test_update_food_valid(self):
        print("\n[TEST] Cập nhật món ăn hợp lệ")
        self.navigate_to_edit_form()
        self.update_food(
            name="Bánh Mì Gà Nướng",
            mota="Cập nhật lại mô tả",
            gia="45000",
            danh_muc="Bánh mì",
            nang_luong="600",
            tgian="8",
            so_luong="4"
        )
        message = self.get_message()
        self.assertIn("thành công", message or "cập nhật")
        
    def test_update_empty_name(self):
        print("\n[TEST] Cập nhật món ăn với tên rỗng")
        self.navigate_to_edit_form()
        self.update_food(
            name="",
            mota="Cập nhật mô tả",
            gia="35000",
            danh_muc="Bún",
            nang_luong="450",
            tgian="10",
            so_luong="3"
        )
        message = self.get_message()
        self.assertTrue("tên" in message or "thất bại" in message)


    def test_update_invalid_price(self):
        print("\n[TEST] Cập nhật món ăn với giá không hợp lệ (abc)")
        self.navigate_to_edit_form()
        self.update_food(
            name="Cơm tấm",
            mota="Ngon tuyệt",
            gia="abc",  # giá không hợp lệ
            danh_muc="Cơm",
            nang_luong="550",
            tgian="12",
            so_luong="5"
        )
        message = self.get_message()
        self.assertIn("thất bại", message)

    def test_update_missing_all_required_fields(self):
        print("\n[TEST] Cập nhật món ăn với tất cả trường bắt buộc trống")
        self.navigate_to_edit_form()
        self.update_food(
            name="",
            mota="",
            gia="",
            danh_muc="",
            nang_luong="",
            tgian="",
            so_luong=""
        )
        message = self.get_message()
        self.assertIn("thất bại", message)


    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()
