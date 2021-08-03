import requests, sys, read_csv

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

from won_to_cate import *

def fun_dothe_mac(driver, indx , code , price , cateType):
    #try:
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
    driver.switch_to_window(driver.window_handles[1])
    driver.get_window_position(driver.window_handles[1])
    driver.implicitly_wait(10)

    #대카테 선택  https://scribblinganything.tistory.com/149   << 로딩 개기 참조 코드
    sleep(2)
    #bigcatebtn = driver.find_elements_by_css_selector('#eCategoryTbody > tr > td:nth-child(1) > div > ul > li[category_num ="1962"]')

    bigcatebtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#eCategoryTbody > tr > td:nth-child(1) > div > ul > li[category_num ="1962"]')))
    print(bigcatebtn)
    #bigcatebtn[0].click()

    print('test location 1')
    sleep(10)

    print('befere add btn 1 ')
    #추가 선택
    add_btn1 = driver.find_elements_by_css_selector('#eCategorySelect')
    add_btn1[0].click()

    print('test location 2')
    sleep(10)

    #중카테 선택
    middle_query = "#eCategoryTbody > tr > td:nth-child(2) > div > ul > li[category_num ='"+price+"']"
    middlecatebtn = driver.find_elements_by_css_selector(middle_query)
    #middlecatebtn[0].click()
    print(middlecatebtn[0])

    print('test location 3')
    sleep(10)
    
    #추가 선택
    add_btn2 = driver.find_elements_by_css_selector('#eCategorySelect')
    add_btn2[0].click()

    print('test location 4')
    sleep(10)

    #소카테 선택
    small_query = f'#eCategoryTbody > tr > td:nth-child(3) > div > ul > li[category_num = {cateType}]'
    smallcatebtn = driver.find_elements_by_css_selector(small_query)
    smallcatebtn[0].click()

    print('test location 5')
    sleep(10)
    
    #추가 선택
    add_btn3 = driver.find_elements_by_css_selector('#eCategorySelect')
    add_btn3[0].click()

    print('test location 6')
    sleep(10)

    #수정 버튼 클릭
    applybtn = driver.find_elements_by_css_selector('#eProductModify')
    applybtn[0].click()
    driver.implicitly_wait(10)

    #2차 확인 팝업 해결
    popup = Alert(driver)
    popup.accept()
    sleep(1)

    #현재 창 다시 메인으로 변경
    driver.switch_to_window(driver.window_handles[0])
    driver.get_window_position(driver.window_handles[0])
    
    #로그에 기록
    read_csv.setState(indx, 'True')
    
    print('stop for now')
    sleep(5000)
        
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
    print('sleep for 30')
    sleep(30)

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
    logbtn = driver.find_elements_by_css_selector('.membership  .admin')
    logbtn[0].click()
    driver.implicitly_wait(10)
    logoutbtn = driver.find_elements_by_css_selector('.adminLayer .btnMember a')
    logoutbtn[0].click()

def init_chrome():
    print('chrome init')
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
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
        value = read_csv.get_data(i)
        print(value)
        price =  csvex.turnwon(value[1])
        cate =  csvex.turncate(value[2])
        #fun_dothe_mac(driver, i, value[0] , value[1] , value[2])
        fun_dothe_mac(driver, i, value[0] , price , cate)

    print('work is done')
    fun_logout(driver)

    print('at the dead end of the code exiting in 3sec')
    
    sleep(3)
    exit()
################################


def main():
    init_chrome()
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

if __name__ == "__main__":
    read_csv.read_file()
    main()