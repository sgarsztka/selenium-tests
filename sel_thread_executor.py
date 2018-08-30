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
        file = open('Note_8.csv', 'w')
        wait = WebDriverWait(self.driver, 5)
        self.driver.get("https://www.ceneo.pl/")
        elem = self.driver.find_element_by_name("search-query")
        elem.send_keys("Samsung Galaxy Note 8 SM-N950 Midnight Black")
        elem.send_keys(Keys.RETURN)
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[2]/div/section/div[2]/div/div/div[2]/div[2]/div[1]/a')))
        price_button = self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div[2]/div/section/div[2]/div/div/div[2]/div[2]/div[1]/a')
        price_button.click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div/div/div[2]/div[5]/div[2]/section[3]/table/tbody/tr[1]/td[5]/a/span/span')))
        all_prices = []
        all_prices = self.driver.find_elements_by_class_name('price')
        print(len(all_prices))
        for i in range(0, len(all_prices)):
            # print(all_prices[i].text)
            file.write(all_prices[i].text+"\n")
        file.close()

# ########################################################################################################

    def test_name2(self):
        wait = WebDriverWait(self.driver, 5)
        self.driver.get("https://www.ceneo.pl/")
        self.assertIn("Ceneo", self.driver.title)

    def test_findable_element2(self):
        wait = WebDriverWait(self.driver, 5)
        self.driver.get("https://www.ceneo.pl/")
        elem = self.driver.find_element_by_name("search-query")
        elem.send_keys("Ram")
        elem.send_keys(Keys.RETURN)
        s = "nie znaleziono"
        assert s not in self.driver.page_source

    def test_unfindable_element2(self):
        wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://www.ceneo.pl/")
        elem = self.driver.find_element_by_name("search-query")
        elem.send_keys("fshkjfdshkfshkjh")
        elem.send_keys(Keys.RETURN)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "not-found")))
        s = "nie znaleziono"
        assert s in self.driver.page_source

    def test_check_price2(self):
        file = open('s8_prices.csv', 'w')
        wait = WebDriverWait(self.driver, 5)
        self.driver.get("https://www.ceneo.pl/")
        elem = self.driver.find_element_by_name("search-query")
        elem.send_keys("samsung s8")
        elem.send_keys(Keys.RETURN)
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[2]/div/section/div[2]/div/div/div[2]/div[2]/div[1]')))
        price_button = self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div[2]/div/section/div[2]/div[1]/div/div[2]/div[2]/div[1]/a')
        price_button.click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div/div/div[2]/div[5]/div[2]/section[3]/table/tbody/tr[1]/td[5]/a/span/span')))
        all_prices = []
        all_prices = self.driver.find_elements_by_class_name('price')
        for i in range(0, len(all_prices)):
            # print(all_prices[i].text)
            file.write(all_prices[i].text+"\n")
        file.close()
#################################################################################################################

    def tearDown(self):
        self.driver.close()

class Runner():

    def parallel_execution(self, *name):

        suite = unittest.TestSuite()

        for object in name:
            for method in dir(object):
                if (method.startswith('test')):
                    suite.addTest(object(method))

        with ThreadPoolExecutor(max_workers=3) as executor:
            list_of_suites = list(suite)
            for test in range(len(list_of_suites)):
                test_name = str(list_of_suites[test])
                executor.submit(unittest.TextTestRunner().run, list_of_suites[test])

if __name__ == '__main__':
    Runner().parallel_execution(Ceneo)
