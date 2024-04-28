from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# 使用xpath等待并查找单个元素
def wait_elem_xpath(driver:webdriver.Chrome, xpath:str):
    """ Wait for element to load in a page"""
    try:
        return WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        print("Network Timeout!")

# 使用xpath等待并查找多个元素
def wait_elems_xpath(driver:webdriver.Chrome, xpath:str):
    """ Wait for element to load in a page"""
    try:
        return WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,xpath)))
    except TimeoutException:
        print("Network Timeout!")

# 使用xpath检查元素是否存在于页面
def check_ele_xpath(driver:webdriver.Chrome,xpath:str) -> bool:
    """ Check if the page has fixed elements """
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,xpath)))
        return True
    except Exception as e:
        print(e)
        return False

