from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
from concurrent.futures import ThreadPoolExecutor


class Ceneo(unittest.TestCase):
    def setUp(self):
        path = "C:/geckodriver.exe"
        self.driver = webdriver.Firefox(executable_path = path)

    def test_name(self):
        wait = WebDriverWait(self.driver, 5)
        self.driver.get("https://www.ceneo.pl/")
        self.assertIn("Ceneo", self.driver.title)

    def test_findable_element(self):
        wait = WebDriverWait(self.driver, 5)
        self.driver.get("https://www.ceneo.pl/")
        elem = self.driver.find_element_by_name("search-query")
        elem.send_keys("Ram")
        elem.send_keys(Keys.RETURN)
        s = "nie znaleziono"
        assert s not in self.driver.page_source

    def test_unfindable_element(self):
        wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://www.ceneo.pl/")
        elem = self.driver.find_element_by_name("search-query")
        elem.send_keys("fshkjfdshkfshkjh")
        elem.send_keys(Keys.RETURN)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "not-found")))
        s = "nie znaleziono"
        assert s in self.driver.page_source

    def test_check_price(self):
        file = open('prices.csv', 'w')
        wait = WebDriverWait(self.driver, 5)
        self.driver.get("https://www.ceneo.pl/")
        elem = self.driver.find_element_by_name("search-query")
        elem.send_keys("G.Skill 16GB (2x8GB) DDR4 Ripjaws 5 Black (F4-3200C16D-16GVKB)")
        elem.send_keys(Keys.RETURN)
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[2]/div/section/div[2]/div/div/div[2]/div[2]/div[1]')))
        price_button = self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div[2]/div/section/div[2]/div/div/div[2]/div[2]/div[1]')
        price_button.click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div/div/div[2]/div[5]/div[2]/section[3]/table/tbody/tr[1]/td[5]/a/span/span')))
        all_prices = []
        all_prices = self.driver.find_elements_by_class_name('price')
        for i in range(0, len(all_prices)):
            print(all_prices[i].text)
            file.write(all_prices[i].text+"\n")
        file.close()

    def tearDown(self):
        self.driver.close()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(Ceneo('test_name'))
    suite.addTest(Ceneo('test_findable_element'))
    suite.addTest(Ceneo('test_unfindable_element'))
    suite.addTest(Ceneo('test_check_price'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
