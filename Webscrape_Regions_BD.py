import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")

# PATH TO CHROMEDRIVER EXECUTABLE
path = 'c:/Users/Anik/Downloads/Compressed/chromedriver/chromedriver.exe'
driver = webdriver.Chrome(executable_path=path, options=chrome_options)
driver.get('http://www.frs-bd.com/')



sleeptime = 1
jsondata = {}
jsondata['districts'] = []


distList = Select(WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlDistrict"))))
distLen = len(distList.options)
for i in range(1,distLen):
    distList = Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlDistrict"))))
    dName = distList.options[i].text
    print(dName)
    jsondata['districts'].append({'district-name': str(dName), 'sub-districts': []})
    distList.select_by_index(i)
    time.sleep(sleeptime)

    subDistList = Select(WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlUpazila"))))
    subDistLen = len(subDistList.options)

    for ii in range(1,subDistLen):
        subDistList = Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlUpazila"))))
        sName = subDistList.options[ii].text
        print('\t',sName)
        jsondata['districts'][i-1]['sub-districts'].append({'sub-district-name': str(sName), 'unions': []})
        subDistList.select_by_index(ii)
        time.sleep(sleeptime)

        unionList = Select(WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlUnion"))))
        unionLen = len(unionList.options)

        for iii in range(1,unionLen):
            unionList = Select(WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlUnion"))))
            uName = unionList.options[iii].text
            print('\t\t',uName)
            unionList.select_by_index(iii)
            time.sleep(sleeptime)
            soilType = ''
            try:
                soilType = Select(WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlSoilPhysiography")))).options[0].text
            except: pass
            jsondata['districts'][i-1]['sub-districts'][ii-1]['unions'].append({'union-name': str(uName), 'soil-type':soilType})


with open('regions.json', 'w', encoding='utf8') as outfile:
    json.dump(jsondata, outfile, indent=4, ensure_ascii=False)

driver.quit()

