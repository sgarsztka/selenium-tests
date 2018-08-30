from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import unittest
import psycopg2
import HtmlTestRunner

from concurrent.futures import ThreadPoolExecutor

class Dashboard(unittest.TestCase):

    def setUp(self):
        path = "C:/geckodriver.exe"
        self.driver = webdriver.Firefox(executable_path = path)

    def test_site_name(self):
        print("Test site_name")
        wait = WebDriverWait(self.driver, 5)
        self.driver.get("http://xxx.xxx.xxx.xxx:8000/admin/login/?next=/admin/")
        self.assertIn("Log in | Django site admin",self.driver.title)
        print(unittest.TestCase.id(self))


    def test_login(self):
        print("Test login")
        self.driver.get("http://xxx.xxx.xxx.xxx:8000/admin/login/?next=/admin/")
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
        username = self.driver.find_element_by_name("username")
        password = self.driver.find_element_by_name("password")
        wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
        username.send_keys("admin")
        password.send_keys("xxx")
        login_button = self.driver.find_elements_by_class_name("submit-row")
        login_button[0].click()
        self.assertIn("Site administration", self.driver.page_source)
        print(unittest.TestCase.id(self))

    def test_add_user(self):
        print("Test Add_user")
        self.driver.get("http://xxx.xxx.xxx.xxx:8000/admin/login/?next=/admin/")
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
        username = self.driver.find_element_by_name("username")
        password = self.driver.find_element_by_name("password")
        wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
        username.send_keys("admin")
        password.send_keys("xxx")
        login_button = self.driver.find_elements_by_class_name("submit-row")
        login_button[0].click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[1]/div/table/tbody/tr[2]/th/a')))
        add_button = self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/table/tbody/tr[2]/td[1]/a')
        add_button.click()
        wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
        add_username_form = self.driver.find_element_by_name('username')
        add_password1_form = self.driver.find_element_by_name('password1')
        add_password2_form = self.driver.find_element_by_name('password2')

        add_username_form.send_keys("test_user")
        add_password1_form.send_keys("test")
        add_password2_form.send_keys("test")
        user_save_button = self.driver.find_element_by_name('_save')
        user_save_button.click()
        s = "Please correct the error"
        wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
        # self.assertNotIn("Please correct the error", self.driver.page_source )
        print(unittest.TestCase.id(self))
        if (s in self.driver.page_source):
            print("User already exists - deleting old user")
            self.driver.execute_script("window.history.go(-2)")
            wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[1]/div/table/tbody/tr[2]/th/a')))
            users_link = self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div/table/tbody/tr[2]/th/a')
            users_link.click()
            test_user_checkbox = self.driver.find_element_by_xpath('/html/body/div/div[3]/div/div/form/div[2]/table/tbody/tr[2]/td[1]/input')
            test_user_checkbox.click()
            self.driver.find_element_by_xpath('/html/body/div/div[3]/div/div/form/div[1]/label/select/option[2]').click()
            go_button = self.driver.find_element_by_xpath('/html/body/div/div[3]/div/div/form/div[1]/button')
            go_button.click()
            d = "Summary"
            assert d in self.driver.page_source
            wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[3]/form/div/input[4]')))
            consent_button = self.driver.find_element_by_xpath('/html/body/div/div[3]/form/div/input[4]')
            consent_button.click()
            print(unittest.TestCase.id(self))


    def test_add_task(self):
        wait = WebDriverWait(self.driver, 5)
        Dashboard.test_login(self)
        wait.until(EC.visibility_of_element_located((By.XPATH, ('/html/body/div/div[2]/div[1]/div[2]/table/tbody/tr/th/a'))))
        tasks_button = self.driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[2]/table/tbody/tr/th/a')
        tasks_button.click()
        wait.until(EC.visibility_of_element_located((By.XPATH,('/html/body/div/div[3]/div/ul/li/a'))))
        add_task = self.driver.find_element_by_xpath(('/html/body/div/div[3]/div/ul/li/a'))
        add_task.click()
        wait.until(EC.visibility_of_element_located((By.NAME,'summary_task')))
        summary_task_form = self.driver.find_element_by_name('summary_task')
        summary_task_form.send_keys("Automated summary task check for long string")
        component_list = self.driver.find_element_by_xpath('/html/body/div/div[3]/div/form/div/fieldset[2]/div[1]/div/select/option[2]')
        component_list.click()
        server_list = self.driver.find_element_by_xpath('/html/body/div/div[3]/div/form/div/fieldset[2]/div[2]/div/select/option[3]')
        server_list.click()
        revision_form = self.driver.find_element_by_name('revision')
        revision_form.send_keys("test revision")
        language = self.driver.find_element_by_xpath('/html/body/div/div[3]/div/form/div/fieldset[2]/div[4]/div/select/option[6]')
        language.click()
        link_archive_form = self.driver.find_element_by_name('link_archive_tests')
        link_archive_form.send_keys("/home/delivery/module-1.42.0-20180801.tar.gz")
        task_save_button = self.driver.find_element_by_name('_save')
        task_save_button.click()
        print(unittest.TestCase.id(self))

    def test_db_entry(self):
        conn = psycopg2.connect(host="xxx.xxx.xxx.xxx",database="module", user="postgres", password="xxx")
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        cur.execute('SELECT * FROM tasks')
        tasks = cur.fetchall()
        print(db_version)
        print("Tasks count in db: ", cur.rowcount)
        for row in tasks:
            print(row)
        print(unittest.TestCase.id(self))
        conn.close()

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
    Runner().parallel_execution(Dashboard)
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='Dashboard'))
