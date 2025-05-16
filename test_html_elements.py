import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest

class TestH5Tag(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def test_h5_tag_content(self):
        driver = self.driver
        driver.get("http://10.48.10.170")  # Replace with correct IP if needed
        time.sleep(3)
        h5_text = driver.find_element(By.TAG_NAME, "h5").text
        self.assertEqual("Lab 3-6 Works!", h5_text)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
