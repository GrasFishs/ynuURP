from selenium import webdriver
import time
from bs4 import BeautifulSoup as BS
import requests
import pymysql

db = pymysql.connect('localhost','root','gotoAnd@123','urp',use_unicode=True, charset="utf8")
cursor = db.cursor()

class Ynu:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://202.203.209.96/v5/#/")
        print("正在解析urp")
        time.sleep(1)
        self.downloadCode()

    def singIn(self, username, password,verification_code):
        #输入用户名，密码
        u = self.driver.find_element_by_id("userCode")
        p = self.driver.find_element_by_id("password")
        u.clear()
        u.send_keys(username)
        p.clear()
        p.send_keys(password)
        verCode = self.driver.find_element_by_css_selector("input[placeholder='验证码(不区分大小写)']")
        verCode.clear()
        verCode.send_keys(verification_code)

    def clickSign(self):
        signInParent = self.driver.find_element_by_css_selector("div.col-xs-12,.text-center")
        signIn = self.driver.find_element_by_css_selector('input.btn-success')
        signInParent.click()
        signIn.click()
        return self.confirmLoginin()

    def confirmLoginin(self):
        try:
            self.driver.find_element_by_css_selector("div.ngdialog-content")
            self.driver.find_element_by_css_selector("div.ngdialog-overlay").click()
            self.downloadCode()
            return False
        except Exception as e:
            print(e)
            return True

    def downloadCode(self):
        self.driver.find_element_by_id("studentLoginBtn").click()
        imgUrl = self.driver.find_element_by_css_selector("img[alt='验证码图片']").get_attribute("src")
        f = open("验证码.png", "wb+")
        f.write(requests.get(imgUrl).content)
        f.close()

    def getInfo(self):
        tableList = []
        self.driver.get("http://202.203.209.96/v5/#/StuBasicInfo")
        time.sleep(1)
        soup = BS(self.driver.page_source,'html.parser')
        trs = soup.find_all("tr")
        for tr in trs:
            tdlist = tr.find_all("td")
            t1 = tdlist[0].text
            t2 = tdlist[1].text
            t3 = tdlist[2].text
            t4 = tdlist[3].text
            tableList.append((t1,t2,t3,t4))
        return tableList

    def getGrade(self):
        l = []
        self.driver.get("http://202.203.209.96/v5/#/StudentResult")
        time.sleep(2)
        soup = BS(self.driver.page_source, 'html.parser')
        rows = soup.select("tbody tr")
        for row in rows:
            l = row.text.replace(" ", "").replace("否","").replace("体育与技术技能类","").replace("人文科学类","")\
                .replace("艺术类","").replace("自然科学类","").replace("社会科学类","").split("\n")
            while '' in l:
                l.remove("")
            sql = "INSERT INTO grade VALUES('%s','%s','%s','%s','%s','%f','%f','%f')"\
                  % (l[0],l[1],l[2],l[3],l[4],float(l[5]),float(l[6]),float(l[7]))
            try:
                cursor.execute("TRUNCATE TABLE GRADE")
                cursor.execute(sql)
                db.commit()
                print("插入成功!")
            except Exception as e:
                print("插入失败")
                print(e)
                db.rollback()
        db.close()



    def getSelectCourse(self):
        self.driver.get("http://202.203.209.96/v5/#/SelectCourse")
        time.sleep(3)
        selectedPage = self.driver.find_element_by_css_selector("li[ng-click='uiFlag.page=2']")
        selectedPage.click()
        time.sleep(1)
        soup = BS(self.driver.page_source,'html.parser')
        courseList = soup.find_all("tr",attrs={"ng-repeat": "x in mySheet.list"})
        for course in courseList:
            courseName = course.select("td.ng-binding")[0].text.replace(" ","").replace("\n","")
            courseTeacher = course.find("h5").text.replace(" ","").replace("\n","")
            print((courseName,courseTeacher))


    def selectCourse(self):
        self.driver.get("http://202.203.209.96/v5/#/SelectCourse")
        time.sleep(5)
        self.driver.find_element_by_css_selector("li[ng-click='uiFlag.page=3']").click()
        time.sleep(1)
        courseCode = self.driver.find_element_by_css_selector("input[placeholder='输入教学班代码直接选课']")
        courseCode.clear()
        courseCode.send_keys("20171A1442")
        self.driver.find_element_by_css_selector("button.btn-success").click()
        time.sleep(2)
        vercode = self.driver.find_element_by_css_selector("input[placeholder='验证码(不区分大小写)']")
        vercode.send_keys(input("输入选课验证码"))
        submit = self.driver.find_element_by_css_selector('button[ng-click="submitCaptcha()"]')
        print(submit.text)
        submit.click()

'''
me = Ynu()
me.singIn("20151120232", "gotoAnd123",input("验证码:"))
me.clickSign()
me.getGrade()
'''


