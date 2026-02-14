'''DİKKAT: Aşşağıda görmüş olduğunuz kod sadece bir alternatif olmak ile beraber projede 
Kesin olarak kullanılacağı belli değildir. Ancak muhtemelen programda github api kullanılacak'''

from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
from random import randint as rdX

class sogd:
    def __init__(self,user_name,repo_name):
        self.user_name = user_name
        self.repo_name = repo_name
    
    def SOGDX(self):
        max_row_index,rowindex = 0,0
        elements = []

        url_base = f'https://github.com/{self.user_name}/{self.repo_name}'

        options = ChromeOptions()
        options.add_argument('--headless')

        chrome = Chrome(options=options)
        chrome.get(url_base)

        optionsX = ChromeOptions()
        chrome_second = Chrome(options=optionsX)

        chrome.implicitly_wait(4)

        state = 0
        e0fxatp = None

        try:
            chrome.find_element(By.XPATH,'//*[@id="folder-row-0"]/td[2]/div/div/div/div/a')
            state = 1
        
        except Exception as e0fxatpfa:
            e0fxatp = e0fxatpfa
            state = 0

        while True:
            if state == 1:
                try:
                    elementX = chrome.find_element(By.XPATH,f'//*[@id="folder-row-{rowindex}"]/td[2]/div/div/div/div/a')
                    elements.append(elementX.text)
                    rowindex += 1

                except Exception as e0fx:
                    max_row_index = rowindex
                    break

                for element_name in elements:
                    second_url_base = f'https://github.com/{self.user_name}/{self.repo_name}/blob/main/{element_name}'
                    chrome_second.get(second_url_base)
                    elementY = chrome_second.find_element(By.XPATH,f'//*[@id="repo-content-pjax-container"]/react-app/div/div/div[1]/div/div/div[2]/div/div/div[3]/div[2]/div/div[3]/section/div/img')
                    elementY.screenshot(f'DepolamaSistemleri/image_file_x{rdX(0,2048**12)}.png')

            else:
                return (f'SOGD Sistemi şu an için belirtilen XPATH yolunu bulamıyor lütfen bu sistemi kullanmak yerine AGDS sistemini seçin ve onunla devam edin\n\nHata:{e0fxatp}')
    
