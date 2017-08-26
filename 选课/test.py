from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://sg.search.yahoo.com/")

searchWhat = driver.find_element_by_id("yschsp")
#获取id叫做 'yschsp' 的元素
searchWhat.clear()
#通过 clear 方法，可以将输入框内的字符清空，比较保险的做法
searchWhat.send_keys("python")
#通过 send_keys方法把 'python' 传递给serchWhat元素，即id叫做 'yschsp' 的元素

searchBtn = driver.find_element_by_class_name("sbb")
#获取id叫做 'sbb' 的元素，但通常不推荐用class找，用selector能更精确的找到
searchBtn.click()
#通过click()方法点击