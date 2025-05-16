import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest

class TestH2Tag(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def test_h2_tag_content(self):
        driver = self.driver
        driver.get("http://10.48.10.170")  # Replace with your actual IP if needed
        time.sleep(3)  # Wait for the page to fully load
	h2_text = driver.find_element(By.TAG_NAME, "h2").text
        self.assertEqual("Add Contacts", h2_text)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
