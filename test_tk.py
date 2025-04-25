from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import unittest
import time

class SearchFunctionTest(unittest.TestCase):
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
        self.select_menu()

    def login(self, username, password):
        self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/username").send_keys(username)
        self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/password").send_keys(password)
        self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/loginButton").click()
        time.sleep(3)

    def select_menu(self):
        self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/img_ThucDon").click()
        time.sleep(2)

    # ========== TEST CASES ==========

    def test_valid_search(self):
        print("\n[TEST] Tìm kiếm hợp lệ: 'Cheese Pizza'")
        self.search_for("Cheese Pizza")
        result = self.is_search_result_displayed()
        print("Expected result: Hiển thị danh sách kết quả chứa 'Cheese Pizza'")
        print(f"Actual result: {'Có kết quả' if result else 'Không có kết quả'}")
        self.assertTrue(result, "Kết quả tìm kiếm không hiển thị")

    def test_invalid_search(self):
        print("\n[TEST] Tìm kiếm không hợp lệ: 'abcdefgh'")
        self.search_for("abcdefgh")
        result = self.is_no_result_message_displayed()
        print("Expected result: Hiển thị thông báo 'Không tìm thấy kết quả phù hợp'")
        print(f"Actual result: {'Có thông báo' if result else 'Không có thông báo'}")
        self.assertTrue(result, "Thông báo không tìm thấy không hiển thị")

    def test_special_characters_search(self):
        print("\n[TEST] Tìm kiếm với ký tự đặc biệt '@#$%^&*'")
        self.search_for("@#$%^&*")
        result = self.is_no_result_message_displayed()
        print("Expected result: Hiển thị thông báo 'Không tìm thấy kết quả phù hợp'")
        print(f"Actual result: {'Có thông báo' if result else 'Không có thông báo'}")
        self.assertTrue(result, "Ứng dụng không xử lý ký tự đặc biệt đúng")

    def test_empty_search(self):
        print("\n[TEST] Tìm kiếm rỗng")
        self.search_for("")
        result = self.is_empty_search_message_displayed()
        print("Expected result: Hiển thị cảnh báo 'Vui lòng nhập từ khóa tìm kiếm'")
        print(f"Actual result: {'Có cảnh báo' if result else 'Không có cảnh báo'}")
        self.assertTrue(result, "Ứng dụng không yêu cầu nhập từ khóa")

    def test_whitespace_search(self):
        print("\n[TEST] Tìm kiếm với khoảng trắng: '   Cheese Pizza   '")
        self.search_for("   Cheese Pizza   ")
        result = self.is_search_result_displayed()
        print("Expected result: Tìm thấy kết quả như với tìm kiếm bình thường")
        print(f"Actual result: {'Có kết quả' if result else 'Không có kết quả'}")
        self.assertTrue(result, "Ứng dụng không xử lý khoảng trắng đúng")

    def test_search_suggestions(self):
        print("\n[TEST] Gợi ý tìm kiếm: Nhập 'Che'")
        self.type_in_search("Che")
        result = self.is_suggestion_displayed()
        print("Expected result: Hiển thị danh sách gợi ý liên quan đến 'Che'")
        print(f"Actual result: {'Có gợi ý' if result else 'Không có gợi ý'}")
        self.assertTrue(result, "Ứng dụng không hiển thị gợi ý")

    def test_case_insensitive_search(self):
        print("\n[TEST] Tìm kiếm không phân biệt hoa/thường")
        self.search_for("CHEESE PIZZA")
        result_upper = self.is_search_result_displayed()
        self.search_for("cheese pizza")
        result_lower = self.is_search_result_displayed()
        print("Expected result: Cả 2 kết quả đều giống nhau")
        print(f"Actual result: {'Giống nhau' if result_upper == result_lower else 'Khác nhau'}")
        self.assertEqual(result_upper, result_lower, "Tìm kiếm phân biệt chữ hoa/thường")

    def test_misspelled_search(self):
        print("\n[TEST] Tìm kiếm sai chính tả nhẹ: 'Cheez Pizza'")
        self.search_for("Cheez Pizza")
        result = self.is_suggestion_displayed()
        print("Expected result: Hiển thị gợi ý như 'Bạn có muốn tìm Cheese Pizza?'")
        print(f"Actual result: {'Có gợi ý' if result else 'Không có gợi ý'}")
        self.assertTrue(result, "Ứng dụng không gợi ý khi nhập sai chính tả nhẹ")

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    # ========== HÀM HỖ TRỢ ==========

    def search_for(self, query):
        search_box = self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/txt_search_food")
        search_box.clear()
        search_box.send_keys(query)
        self.driver.press_keycode(66)  # Nhấn ENTER
        time.sleep(2)

    def type_in_search(self, query):
        search_box = self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/txt_search_food")
        search_box.clear()
        search_box.send_keys(query)
        time.sleep(1)

    def is_search_result_displayed(self):
        try:
            items = self.driver.find_elements(AppiumBy.ID, "com.example.datdoanonline:id/recyclerViewfood")
            return len(items) > 0
        except:
            return False

    def is_no_result_message_displayed(self):
        try:
            msg = self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/txt_no_result")
            return msg.is_displayed() and "không tìm thấy" in msg.text.lower()
        except:
            return False

    def is_empty_search_message_displayed(self):
        try:
            msg = self.driver.find_element(AppiumBy.ID, "com.example.datdoanonline:id/txt_empty_search")
            return msg.is_displayed() and "vui lòng nhập" in msg.text.lower()
        except:
            return False

    def is_suggestion_displayed(self):
        try:
            suggestions = self.driver.find_elements(AppiumBy.ID, "com.example.datdoanonline:id/suggestion_item")
            return len(suggestions) > 0
        except:
            return False

if __name__ == '__main__':
    unittest.main()
