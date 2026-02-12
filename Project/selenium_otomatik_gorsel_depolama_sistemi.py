'''DİKKAT: Aşşağıda görmüş olduğunuz kod sadece bir alternatif olmak ile beraber projede 
Kesin olarak kullanılacağı belli değildir. Ancak muhtemelen programda github api kullanılacak'''

from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
from random import randint as rdX

user_name = 'nazfelaksuresi8a4'
repo_name = 'Gorsel_yukleme_deposu'

max_row_index,rowindex = 0,0
elements = []

url_base = f'https://github.com/{user_name}/{repo_name}'

options = ChromeOptions()
#options.add_argument('--headless')

chrome = Chrome(options=options)
chrome.get(url_base)

chrome_second = Chrome(options=options)

chrome.implicitly_wait(4)

while True:
    try:
        elementX = chrome.find_element(By.XPATH,f'//*[@id="folder-row-{rowindex}"]/td[2]/div/div/div/div/a')
        elements.append(elementX.text)
        rowindex += 1

    except:
        max_row_index = rowindex
        break

for element_name in elements:
    second_url_base = f'https://github.com/{user_name}/{repo_name}/blob/main/{element_name}'
    chrome_second.get(second_url_base)
    elementY = chrome_second.find_element(By.XPATH,f'//*[@id="repo-content-pjax-container"]/react-app/div/div/div[1]/div/div/div[2]/div/div/div[3]/div[2]/div/div[3]/section/div/img')
    elementY.screenshot(f'image_file_x{rdX(0,2048**12)}.png')

