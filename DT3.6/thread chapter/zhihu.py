from selenium import  webdriver

driver = webdriver.Firefox()

driver.get('https://www.zhihu.com/signin')
user = driver.find_element_by_name('username')
user.clear()
user.send_keys('18910598793')
passwd = driver.find_element_by_name('password')
passwd.clear()
passwd.send_keys('xingyue123.')
#user.clear()

print(driver.find_element_by_tag_name('button').text)
