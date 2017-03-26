from bs4 import BeautifulSoup
from selenium import webdriver
import time

#使用selenium
# driver = webdriver.PhantomJS(executable_path=r"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe")
# driver.maximize_window()
driver=webdriver.Chrome() #这里使用可视化的浏览器
#设置浏览器窗口的位置和大小
driver.set_window_position(20, 40)
driver.set_window_size(1100,700)
list=['xxxxx','xxxxxx','xxxx','xxxx','xxx','xxxx','xx','xxxx',
      'xxxxxx'] #存放账号的列表
account=''
passwd=''
#登录QQ空间
def get_shuoshuo(qq,i):

    print('账号:',qq)
    driver.get('http://user.qzone.qq.com/'+qq+'/311'.format(qq))
    time.sleep(5)
    #判断是否有登录框
    try:
        driver.find_element_by_id('login_div')
        a = True
    except:
        a = False
    if a == True:
        driver.switch_to.frame('login_frame') #转换frame
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()#选择用户名框
        driver.find_element_by_id('u').send_keys(account) #输入账号
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys(passwd)  #输入密码
        driver.find_element_by_id('login_button').click()  #模拟点击登录按钮
        time.sleep(13)  #登录需要时间，因此这里等待13秒
    driver.implicitly_wait(13)  #这里是挑战后的页面，跳转也需要时间
    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon')    #判断是否有权限，有权限就退出
        b = True
    except:
        b = False
        print('需要权限')
        get_shuoshuo(list[i+1],i+1)


    if b == True:
        driver.switch_to.frame('app_canvas_frame')    #转到新的frame
        content = driver.find_elements_by_css_selector('.content')  #找到主页
        stime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')   #时间的类名
        for con,sti in zip(content,stime):
            data = {
                'time':sti.text,
                'shuos':con.text
            }
            print(data)
        # pages = driver.page_source
        # soup = BeautifulSoup(pages,'html.parser')


    cookie = driver.get_cookies()  #获取到cookie,以后可直接使用cookie登录
    cookie_dict = []
    for c in cookie:
        ck = "{0}={1};".format(c['name'],c['value'])
        cookie_dict.append(ck)
    i = ''
    for c in cookie_dict:
        i += c
    print('Cookies:',i)
    print("==========完成================")

    # driver.close()
    # driver.quit()

if __name__ == '__main__':
    account = input("输入你的账号")
    passwd = input("请输入你的密码")
    for i in range(len(list)):
        get_shuoshuo(list[i],i)