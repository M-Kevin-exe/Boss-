import json,pyautogui,re
from selenium.webdriver.common.by import By
from selenium import webdriver
from FindEle_tools import wait_elem_xpath
from FindEle_tools import wait_elems_xpath
from FindEle_tools import check_ele_xpath
from time import sleep

'''
使用谷歌浏览器和谷歌自动化驱动。

！输入自己的手机号，在登录界面手动验证发送验证码，《验证码需要在控制台输入》。
如果不登陆需要注释行self.login_boss()

可以事先规定好value_code和city_code变量
city_code变量可以直接注释input
value_code公司规模是一个list，事先写好该list需要把它下面的while循环的T改为F

登陆后程序会根据筛选的拼接url跳转到Boss的推荐职位。

需事先在推荐职位页面添加 求职期望
如果不添加需要把第行self.change_content()注释掉
'''
# 手机号
PHONE_NUMBER = 12345678910
# 关键词对标题和标签进行匹配，有一个内容包含关键词就采用
KEYWORD = ["PYTHON","测试","自动化","爬虫","IT"]
# 期望工作地址 只能写 市 
ADDRESS = ["广州","珠海","深圳"]
# 登陆后可以调大该参数，可以加载更多岗位
SCROLLNUM = 3

# 推荐职位 页面的UI位置，目的是将鼠标光标悬停在岗位list上进行向下滑动，加载更多数据
UIX=560
UIY=640

TJ0=[]
TJ1=[]
TJ2=[]
TJ3=[]

SENDED=[]

options_chrome = webdriver.ChromeOptions()
options_chrome.headless = False
options_chrome.add_argument("log-level=3")



# 完成boss制品的登录操作
class Boss_login_web():
    def __init__(self,driver) -> None:
        self.driver = driver
        self.main()

    # login boss web
    def login_boss(self):
        login_url = "https://www.zhipin.com/web/user/"
        self.driver.get(url=login_url)
        wait_elem_xpath(self.driver,'//input[@type="tel"]').send_keys(PHONE_NUMBER)
        wait_elem_xpath(self.driver,'//div[@ka="send_sms_code_click"]/span').click()
        encode = input("请输入验证码：")
        wait_elem_xpath(self.driver,'//input[@ka="signup-sms"]').send_keys(encode)
        wait_elem_xpath(self.driver,'//input[@class="agree-policy"]').click()
        wait_elem_xpath(self.driver,'//button[@ka="signup_submit_button_click"]').click()
        sleep(10)
        self.check_login()

    # 打开目标网页
    def open_web(self,target_url):
        self.driver.get(target_url)
        return

    # 检查是否登录
    def check_login(self):
        login_xpath = '//a[@ka="header-login"]'
        isLogin = check_ele_xpath(self.driver,login_xpath)
        if isLogin:
            self.login_boss()
            return
        else:
            return

    # url 拼接
    def get_url(self):
        city = self.get_city_code()
        scale = self.get_scale_code()
        job_recommend_url = f"https://www.zhipin.com/web/geek/job-recommend?city={city}&scale={scale}"
        return job_recommend_url

    # 获取筛选城市code
    def get_city_code(self):
        city_json_path = "./city.json"
        with open(city_json_path,'r',encoding="utf-8") as f:
            citys_json = json.load(f)
            f.close()
        
        citys_json = citys_json["zpData"]["cityList"]
        city_name = input("请输入地级市：")
        # city_name = "广州"
        city_code = ""
        for city_json in citys_json:
            for sub_city_json in city_json["subLevelModelList"]:
                if sub_city_json["name"] == city_name:
                    city_code = sub_city_json["code"]
                    break
                else:
                    continue
        
        if city_code:
            return city_code
        else:
            print(f"没有{city_name},请输入正确的地级市。")
            self.get_city_code()

    # 获取筛选公司规模code
    def get_scale_code(self):
        scale_code = {
            "301":"0-20",
            "302":"20-99",
            "303":"100-499",
            "304":"500-999",
            "305": "1000-9999",
            "306":"10000以上",
        }
        value_txt=[]
        value_code=[]
        # value_code=["303","304","305","306"]
        while True:
            print(f"\n\n已选择的内容 {value_txt}")
            scale_tag = input("请输入序号选择公司规模：\n1:0-20人\n2:20-99人\n3:100-499人\n3:100-499人\n4:500-999人\n5:1000-9999人\n6:10000人以上\n7:不限\n(输入0选择完成):")
            if scale_tag == "1":
                if scale_code[f"30{scale_tag}"] not in value_txt:
                    value_txt.append(scale_code[f"30{scale_tag}"])  
                    value_code.append(f"30{scale_tag}") 
                else:
                    value_txt.remove(scale_code[f"30{scale_tag}"])
                    value_code.remove(f"30{scale_tag}") 
            if scale_tag == "2":
                if scale_code[f"30{scale_tag}"] not in value_txt:
                    value_txt.append(scale_code[f"30{scale_tag}"])   
                    value_code.append(f"30{scale_tag}") 
                else:
                    value_txt.remove(scale_code[f"30{scale_tag}"])
                    value_code.remove(f"30{scale_tag}") 
            if scale_tag == "3":
                if scale_code[f"30{scale_tag}"] not in value_txt:
                    value_txt.append(scale_code[f"30{scale_tag}"])   
                    value_code.append(f"30{scale_tag}") 
                else:
                    value_txt.remove(scale_code[f"30{scale_tag}"])
                    value_code.remove(f"30{scale_tag}") 
            if scale_tag == "4":
                if scale_code[f"30{scale_tag}"] not in value_txt:
                    value_txt.append(scale_code[f"30{scale_tag}"])   
                    value_code.append(f"30{scale_tag}") 
                else:
                    value_txt.remove(scale_code[f"30{scale_tag}"])
                    value_code.remove(f"30{scale_tag}") 
            if scale_tag == "5":
                if scale_code[f"30{scale_tag}"] not in value_txt:
                    value_txt.append(scale_code[f"30{scale_tag}"])   
                    value_code.append(f"30{scale_tag}") 
                else:
                    value_txt.remove(scale_code[f"30{scale_tag}"])
                    value_code.remove(f"30{scale_tag}") 
            if scale_tag == "6":
                if scale_code[f"30{scale_tag}"] not in value_txt:
                    value_txt.append(scale_code[f"30{scale_tag}"])   
                    value_code.append(f"30{scale_tag}") 
                else:
                    value_txt.remove(scale_code[f"30{scale_tag}"])
                    value_code.remove(f"30{scale_tag}") 
            if scale_tag == "7":
                value_txt=[]
                value_code=[]
            if scale_tag == "0":
                break
        return ",".join(value_code)

    def main(self):
        target_url = self.get_url()
        self.login_boss()
        self.open_web(target_url)

# 获取links
class Boss_get_links():
    def __init__(self,driver) -> None:
        self.driver = driver
        self.main()

    # 向下将鼠标移动到指定位置并向下滑动加载数据 
    def scroll_ul(self):
        pyautogui.moveTo(UIX,UIY)
        for i in range(SCROLLNUM):
            print(i)
            pyautogui.scroll(-1000)
            sleep(2)
        return 

    # 获取到UI标签下的岗位
    def get_li(self,TJ:int):
        global TJ0,TJ1,TJ2,TJ3
        self.scroll_ul()
        tem_TJ = []
        ul_xpath = '//ul[@class="rec-job-list"]/li'
        li_eles = wait_elems_xpath(self.driver,ul_xpath)
        print(li_eles)
        print(len(li_eles))
        for li_ele in li_eles:
            tem_ele = li_ele.find_element(By.XPATH,'./*//a[@class="job-name"]')
            title = tem_ele.text
            href = tem_ele.get_attribute("href")
            tem_TJ.append({
                "title":title,
                "href":href
            })
            print(f"{title}:{href}")
        
        if TJ == 0:
            TJ0 = tem_TJ
        if TJ == 1:
            TJ1 = tem_TJ
        if TJ == 2:
            TJ2 = tem_TJ
        if TJ == 3:
            TJ3 = tem_TJ
        return 

    # 更改求职期望的list
    def change_content(self):
        content_xpath = '//span[@class="text-content"]'
        contents_ele = wait_elems_xpath(self.driver,content_xpath)
        if contents_ele:
            for i in range(len(contents_ele)):
                contents_ele[i].click()
                self.get_li(i+1)
        return


    def main(self):
        self.get_li(0)
        self.change_content()


# 对岗位发信息
class Boss_send_message():
    def __init__(self,driver) -> None:
        self.driver = driver
        self.main()
    
    # 打开获取到的岗位info页面
    def open_company_link(self):
        global TJ0,TJ1,TJ2,TJ3
        TJS = [TJ0,TJ1,TJ2,TJ3]
        if TJS:
            for tem_TJ in TJS:
                if tem_TJ:
                    for TT in tem_TJ:
                        self.company_info(TT["href"])
                        Bool_Address = self.check_address()
                        Bool_Keywords = self.check_keywords()
                        if Bool_Address and Bool_Keywords:
                            print(f"{TT['title']}:{TT['href']}")
                            self.send_message()
                        if not Bool_Address:
                            print(f"{TT['title']}:不在目标地址")
                        if not Bool_Keywords:
                            print(f"{TT['title']}:关键词不符")
                print("完成一个共四个")
    # 进入页面
    def company_info(self,link):
        self.driver.get(link)
        return

    # 检查地址是否为期望地址
    def check_address(self) -> bool:
        address_xpath = '//a[@class="text-desc text-city"]'
        if wait_elem_xpath(self.driver,address_xpath).text in ADDRESS:
            return True
        else:
            return False

    # 检查标题和标签是否存在关键词
    def check_keywords(self) -> bool:
        title_xpath = '//h1'
        send_message_xpath = '//div[@class="btn-container"]/a[2]'
        tag_xpath = '//ul[@class="job-keyword-list"]'
        try:
            send_message_text = wait_elem_xpath(self.driver,send_message_xpath).text
        except:
            return False
        if send_message_text == "立即沟通":
            title_text = wait_elem_xpath(self.driver,title_xpath).text
            tag_text = wait_elem_xpath(self.driver,tag_xpath).text
            for keyword in KEYWORD:
                match1 = re.search(keyword,title_text.upper())
                match2 = re.search(keyword,tag_text.upper())
                if match1 or match2:
                    address_xpath = '//a[@class="text-desc text-city"]'
                    address_text = wait_elem_xpath(self.driver,address_xpath).text
                    SENDED.append({
                        "title":title_text,
                        "address" : address_text,
                        "href":self.driver.current_url
                    })
                    return True
        return False

    # 发送信息
    def send_message(self) -> bool:
        send_message_xpath = '//div[@class="btn-container"]/a[2]'
        wait_elem_xpath(self.driver,send_message_xpath).click()
        login_xpath = '//div[@class="boss-login-dialog-content"]'
        chat_xpath = '//div[@class="dialog-container"]'
        if check_ele_xpath(self.driver,login_xpath):
            Boss_login_web(self.driver).login_boss()
            return False
        elif check_ele_xpath(self.driver,chat_xpath):
            return True
    
    # 最后把所有的已经发送的岗位保存到csv中，所有都执行完才会保存，否则不会保存。可以改进成发一个存一个
    def save_to_csv(self):
        with open("./companys.csv","a") as f:
            for ss in SENDED:
                title = ss["title"]
                address = ss["address"]
                href = ss["href"]
                f.write(f"{title},{address},{href}\n")
            f.close()
        
    def main(self):
        self.open_company_link()
        self.save_to_csv()


if __name__ == "__main__":
    driver = webdriver.Chrome(options = options_chrome)
    driver.maximize_window()
    Boss_login_web(driver)
    Boss_get_links(driver)
    Boss_send_message(driver)
