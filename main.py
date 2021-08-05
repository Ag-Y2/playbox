import requests, sys, read_csv

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep

from won_to_cate import *


class MyWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.setupUI()

  def setupUI(self):
    self.setGeometry(300, 200, 500, 300)
    self.setWindowTitle("  v0.1")
    self.setWindowIcon(QIcon('icon.png'))

    self.lineEdit_startdate = QLineEdit()
    self.lineEdit_startdate.setPlaceholderText('1')
    self.lineEdit_enddate = QLineEdit()
    self.lineEdit_enddate.setPlaceholderText('2')

    self.lineEdit = QLineEdit()
    self.lineEdit.setPlaceholderText('3')

    self.pushButton0 = QPushButton("run")
    self.pushButton0.clicked.connect(main)


    # Right Layout
    rightLayout = QVBoxLayout()
    rightLayout.addWidget(self.lineEdit_startdate)
    rightLayout.addWidget(self.lineEdit_enddate)
    rightLayout.addWidget(self.lineEdit)
    rightLayout.addWidget(self.pushButton0)

    rightLayout.addStretch(1)

    layout = QHBoxLayout()

    layout.addLayout(rightLayout)

    layout.setStretchFactor(rightLayout, 0)

    self.setLayout(layout)
#############    

def fun_dothe_mac(driver, indx , code , price , cateType):
    print('in fun mac')
    driver.switch_to.window(driver.window_handles[0])
    driver.get_window_position(driver.window_handles[0])
    try:
        #상품코드 선택
        selectbtn = driver.find_elements_by_css_selector('.fSelect.eSearch')
        select = Select(selectbtn[0])
        select.select_by_visible_text('상품코드')
        #상품 정보 입력
        searchbox = driver.find_elements_by_css_selector('.fText.eSearchText')
        searchbox[0].clear()
        searchbox[0].send_keys(code)

        #상품 검색 버튼
        searchbtn = driver.find_elements_by_css_selector('#eBtnSearch')
        searchbtn[0].click()
        driver.implicitly_wait(10)

        #상품 클릭
        product_list = driver.find_elements_by_css_selector('#product-list .txtLink.eProductDetail.ec-product-list-productname')
        product_list[0].click()

        #현재창 변경 메인 --> 에디터 
        driver.switch_to.window(driver.window_handles[1])
        driver.get_window_position(driver.window_handles[1])
        driver.implicitly_wait(10)

        #대카테 선택  https://scribblinganything.tistory.com/149   << 로딩 개기 참조 코드
        #bigcatebtn = driver.find_elements_by_css_selector('#eCategoryTbody > tr > td:nth-child(1) > div > ul > li:nth-child(31)')
        #bigcatebtn = driver.find_element(By.XPATH, '//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[31]')
        #bigcatebtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#eCategoryTbody > tr > td:nth-child(1) > div > ul > li[category_num ="1962"]')))
        #print(bigcatebtn)
        sleep(2)

        script_bigcate_click = '''
        var bigcate = document.querySelector('#eCategoryTbody > tr > td:nth-child(1) > div > ul > li[category_num ="1962"]');
        bigcate.click();
        var addbtn = document.querySelector('#eCategorySelect');
        addbtn.click();

        '''
        

        driver.execute_script(script_bigcate_click)

        '''
        print('in except1')
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            driver.get_window_position(driver.window_handles[0])
            fun_dothe_mac(driver, indx , code , price , cateType)
        '''
            

        sleep(2)

        script_middlecate_click = '''
        var midcate = document.querySelector("#eCategoryTbody > tr > td:nth-child(2) > div > ul > li[category_num ='{}']");
        midcate.click();
        var addbtn = document.querySelector('#eCategorySelect');
        addbtn.click();

        '''.format(price)

        driver.execute_script(script_middlecate_click)

        sleep(2)

        script_smallcate_click = '''
        var smcate = document.querySelectorAll('#eCategoryTbody > tr > td:nth-child(3) > div > ul > li');
        var smcate_tar = "";
        for(var i = 0; i < smcate.length; i++){{
            
            if(smcate[i].innerText == "{0}"){{
                smcate_tar = i;
                i = smcate.length;
            }}
        }}

        smcate[smcate_tar].click();
        var addbtn = document.querySelector('#eCategorySelect');
        addbtn.click();

        '''.format(cateType)

        driver.execute_script(script_smallcate_click)

        sleep(2)

        #수정 버튼 클릭
        applybtn = driver.find_elements_by_css_selector('#eProductModify')
        applybtn[0].click()
        driver.implicitly_wait(10)

        #2차 확인 팝업 해결
        popup = Alert(driver)
        popup.accept()
        driver.implicitly_wait(10)

        #현재 창 다시 메인으로 변경
        driver.switch_to.window(driver.window_handles[0])
        driver.get_window_position(driver.window_handles[0])
        
        #로그에 기록
        read_csv.setState(indx, 'True' ,price , cateType)
    except:
        read_csv.setState(indx, 'False' ,price , cateType)
        
        
        
    #except Exception as e:
    #    print('error occurred ::', e )
    #    read_csv.setState(indx, 'False')


####################################

def fun_set_fild(driver):
    pr_controlbtn = driver.find_elements_by_css_selector('#QA_Gnb_product2')
    pr_controlbtn[0].click()
    driver.implicitly_wait(10)
    ctrbtn1 = driver.find_elements_by_css_selector('#snb .link a')
    ctrbtn1[0].click()
    driver.implicitly_wait(10)
    #######################

def fun_login(driver):
    print('login init')

    id_box =  driver.find_elements_by_css_selector('.mFormBox .column input')
    id_box[0].send_keys('marketb')
    id_box[1].send_keys('eun5476')
    id_box[2].send_keys('young2502!')
    print('sleep for 10')
    sleep(10)

    pr_controlbtn = driver.find_elements_by_css_selector('#QA_Gnb_product2')

    while len(pr_controlbtn) == 0 :
        print('in while loop searching control btn')
        pr_controlbtn =driver.find_elements_by_css_selector('#QA_Gnb_product2')
        sleep(10)

    print('control btn found login complete')

    print('control btn found exit login')
################################
def fun_logout(driver):
    print('logout')
    script_logout = '''
    location.replace("/admin/php/shop1/log_out.php");
    '''

    driver.execute_script(script_logout)

def init_chrome():
    print('chrome init')
    options = webdriver.ChromeOptions()
    #options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.get("https://eclogin.cafe24.com/Shop/?url=Init&login_mode=2&is_multi=F")
    
    #login
    fun_login(driver)
    #set play filed
    fun_set_fild(driver)
    print('stop to check data')
    csvex = csvexchange()
    data_count = read_csv.get_count_data()
    for i in range(0 , data_count) :
        print('begin of for loop')
        value = read_csv.get_data(i)
        price =  csvex.turnwon(value[1])
        cate =  csvex.turncate(value[2])
        #fun_dothe_mac(driver, i, value[0] , value[1] , value[2])
        print('passing pam to fun do the mac')
        fun_dothe_mac(driver, i, value[0] , price , cate)

    print('work is done')
    fun_logout(driver)

    print('at the dead end of the code exiting in 3sec')
    
    sleep(3)
    exit()
################################


def main():
    init_chrome()
    #init_test_def()
    '''
    print('tset')
    data_count = read_csv.get_count_data()
    csvex = csvexchange()
    for i in range(0 , data_count) :
        value = read_csv.get_data(i)
        print(value)
        price =  csvex.turnwon(value[1])
        cate =  csvex.turncate(value[2])
        #price = value[1] + "원"
        print( value[0] , price , cate)
    '''
    

#############

def init_test_def():
    options = webdriver.ChromeOptions()
    #options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.co.kr/")
    driver.implicitly_wait(10)
    txt = "hi there"
    txt1 = " how are you doing"
    txt2 = " it is lovly day "
    script_injection = '''
    javascript:alert('hi')
    
    '''
    #driver.execute_script(script_injection)

    script_injection01 = '''
    for(var i = 0 ; i < 10; i++){{
        console.log('{0}');
        console.log('---');
        console.log('{0}');
        console.log('****');
        if(i == 8){{
            console.log('iiiiiiiiiiiiiiiiiiii');
        }}

    }}
    
    '''.format(txt)
    driver.execute_script(script_injection01)

    csvex = csvexchange()
    data_count = read_csv.get_count_data()
    for i in range(0 , data_count) :
        value = read_csv.get_data(i)
        price =  csvex.turnwon(value[1])
        cate =  csvex.turncate(value[2])
        #fun_dothe_mac(driver, i, value[0] , value[1] , value[2])
        print(i, value[0] , price , cate)
    sleep(3300)

if __name__ == "__main__":
    read_csv.read_file()
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
    #main()