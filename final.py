from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import glob
from selenium.webdriver.support.ui import WebDriverWait
import lxml
import html5lib
import re
import os
from bs4 import BeautifulSoup as BSoup
from pytesseract import image_to_string
import pytesseract
from PIL import Image
import urllib.request
import ssl
import cv2
from lxml import etree
import urllib
import pandas as pd
from selenium import webdriver             # Import module
#from selenium.webdriver.common.keys import Keys   # For keyboard keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import ui
from datetime import datetime
import string
#from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


def get_captcha_text():#function to detect Captcha
  pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\Aditya\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages\\pytesseract\\tesseract.exe'
  config = ('-l eng --oem 1 --psm 3')
  #im = Image.open('screenshot.png')
  im = cv2.imread('screenshot.png', cv2.IMREAD_COLOR)
  text = pytesseract.image_to_string(im, config=config)
  return text
#Creating Lists as per the conditions
year=["2010","2011","2012","2013","2014","2015","2016","2017","2018","2019"]
area=["30","31"]
alphabet=list(string.ascii_uppercase)
pn=list(range(1,10000))
options = Options()
options.set_headless(True)
#cap = DesiredCapabilities().FIREFOX
#cap["marionette"] = False


for a in area:
    if a=="30":
        name="Mumbai"
        if not os.path.exists(name):
            os.makedirs(name)

        for y in year:
            if not os.path.exists(name+"/"+y):
                os.makedirs(name+"/"+y)

            for alph in alphabet:
                if not os.path.exists(name+"/"+y+"/"+alph):
                    os.makedirs(name+"/"+y+"/"+alph)

                loop=1
                insideloop=1
                ind=1




                for p in pn:
                    while loop==1:

                        while insideloop==1:
                            try:
                                insideloop=0
                                URL = 'https://freesearchigrservice.maharashtra.gov.in/'
                                browser=webdriver.Firefox()
                                browser.get(URL)
                                ##browser.delete_all_cookies()
                                time.sleep(2)
                                district = Select(browser.find_element_by_id('ddlDistrict'))
                                ds=browser.find_element_by_id('ddlDistrict')
                                #ds.click()
                                district.select_by_value(a)
                                ys=browser.find_element_by_name("ddlFromYear")
                                years = Select(browser.find_element_by_name("ddlFromYear"))
                                years.select_by_value(y)
                                time.sleep(5)
                                Vname = browser.find_element_by_name("txtAreaName")
                                Vname.send_keys(alph)
                                ds=browser.find_element_by_id('ddlDistrict')
                                ds.click()
                                time.sleep(2)
                                vs=browser.find_element_by_name("ddlareaname")
                                vs.click()
                                time.sleep(5)
                                Vselect = Select(browser.find_element_by_name("ddlareaname"))
                                listofelements=browser.find_elements_by_xpath('//*[@name="ddlareaname"]/option')
                                if not os.path.exists(name+"/"+y+"/"+alph+"/"+str(p)):
                                    os.makedirs(name+"/"+y+"/"+alph+"/"+str(p))
                                if len(listofelements)<=1:
                                    os.rmdir(name+"/"+y+"/"+alph+"/"+str(p))
                                    p=999999
                                    loop=0
                                    ##browser.delete_all_cookies()

                                    browser.close()
                                    break
                                if ind>=len(listofelements):
                                    loop=loop-1
                                    break
                                village=str(listofelements[ind].text)
                                print(village)
                                if not os.path.exists(name+"/"+y+"/"+alph+"/"+str(p)+"/"+village):
                                    os.makedirs(name+"/"+y+"/"+alph+"/"+str(p)+"/"+village)
                                district = Select(browser.find_element_by_id('ddlDistrict'))
                                ds=browser.find_element_by_id('ddlDistrict')
                                #ds.click()
                                district.select_by_value(a)
                                ys=browser.find_element_by_name("ddlFromYear")
                                years = Select(browser.find_element_by_name("ddlFromYear"))
                                years.select_by_value(str(y))
                                time.sleep(5)
                                browser.find_element_by_name("txtAreaName").clear()
                                Vname = browser.find_element_by_name("txtAreaName")
                                Vname.send_keys(alph)
                                ds=browser.find_element_by_id('ddlDistrict')
                                ds.click()
                                time.sleep(2)
                                vs=browser.find_element_by_name("ddlareaname")
                                vs.click()
                                time.sleep(5)
                                Vselect = Select(browser.find_element_by_name("ddlareaname"))
                                Vselect.select_by_value(village)
                                pnumber = browser.find_element_by_name("txtAttributeValue")
                                pnumber.send_keys(str(p))
                                time.sleep(10)
                                #c=1
                                cl1=1
                                cl2=1
                                while cl1==1:
                                    elem = browser.find_element_by_xpath('//*[@id="imgCaptcha"]')
                                    action_chain = ActionChains(browser)
                                    action_chain.move_to_element(elem)
                                    action_chain.perform()
                                    loc, size = elem.location_once_scrolled_into_view, elem.size
                                    left, top = loc['x'], loc['y']
                                    width, height = size['width'], size['height']
                                    box = (int(left), int(top), int(left + width), int(top + height))
                                    browser.save_screenshot('screenshot.png')
                                    img = Image.open('screenshot.png')
                                    captcha = img.crop(box)
                                    captcha.save('screenshot.png', 'PNG')
                                    #browser.save_screenshot('screenshot.png')
                                    captcha = browser.find_element_by_name("txtImg")
                                    captcha.clear()
                                    captcha_text = get_captcha_text()
                                    #print(captcha_text)
                                    captcha.send_keys(captcha_text)
                                    time.sleep(5)
                                    submit = browser.find_element_by_name("btnSearch")
                                    #print(bool(submit))
                                    submit.click()
                                    time.sleep(10)
                                    while cl2==1:
                                        try:
                                            msg=browser.find_element_by_id("lblimg")
                                            if msg.text == "Entered Correct Captcha":
                                               print("Wrong Captcha Detected")
                                               browser.implicitly_wait(10)
                                               time.sleep(5)
                                               break
                                            else:
                                                cl2=0
                                                cl1=0
                                        except:
                                            cl2=0
                                            cl1=0
                                time.sleep(5)
                                browser.implicitly_wait(15)
                                time.sleep(5)
                                j=1
                                while j==1:
                                    try:
                                        browser.find_element_by_id("lblMsgCTS")
                                        ind=ind+1
                                        os.rmdir(name+"/"+y+"/"+alph+"/"+str(p)+"/"+village)
                                        browser.close()
                                        browser.implicitly_wait(5)
                                        time.sleep(10)
                                        break
                                    except:
                                        bs_obj1 = BSoup(browser.page_source, 'lxml')
                                        table = bs_obj1.find('table', id="RegistrationGrid")
                                        indx=list(bs_obj1.find_all(value='IndexII'))
                                        l=0
                                        idm=2
                                        path=str(name+"/"+y+"/"+alph+"/"+str(p)+"/"+village+"/")
                                        df = pd.read_html(str(table))
                                        df1=pd.DataFrame(df[0])
                                        while l<len(indx):
                                            trm=str(idm)
                                            first_link=browser.find_element_by_xpath("/html/body/form/center/div/div/table/tbody/tr[3]/td/div/table/tbody/tr/td/div[1]/div/table/tbody/tr["+str(trm)+"]/td[10]/input")
                                            first_link.click()
                                            time.sleep(10)
                                            tabs=list(browser.window_handles)
                                            #print(tabs)
                                            browser.switch_to.window(tabs[1])
                                            bs_obj1 = BSoup(browser.page_source,"html.parser").encode()
                                            with open(path+"1 "+str(l)+str(idm)+'.html', 'w', encoding='utf-8') as f:
                                                f.write(bs_obj1.decode().strip())
                                            time.sleep(5)
                                            browser.close()
                                            browser.switch_to.window(tabs[0])
                                            time.sleep(10)
                                            idm=idm+1
                                            l=l+1


                                        df1.to_excel(path+"1.xlsx")
                                        p=df1.values[-1].tolist()
                                        i=2
                                        l=0
                                        idm=2
                                        while(i<=(len(p)-1)):
                                            time.sleep(10)
                                            i=str(i)
                                            browser.find_element_by_link_text(i).click()
                                            browser.implicitly_wait(10)
                                            time.sleep(10)
                                            bs_obj1 = BSoup(browser.page_source, 'lxml')
                                            table = bs_obj1.find('table', id="RegistrationGrid")
                                            index=browser.find_element_by_value("IndexII")
                                            while l<len(indx):
                                                #clck=indx[i]

                                                trm=str(idm)
                                                first_link=browser.find_element_by_xpath("/html/body/form/center/div/div/table/tbody/tr[3]/td/div/table/tbody/tr/td/div[1]/div/table/tbody/tr["+str(trm)+"]/td[10]/input")
                                                first_link.click()
                                                time.sleep(10)
                                                tabs=list(browser.window_handles)
                                                print(tabs)
                                                browser.switch_to.window(tabs[1])
                                                bs_obj1 = BSoup(browser.page_source,"html.parser").encode()
                                                with open(path+"page_"+str(i)+str(l)+str(idm)+'.html', 'w', encoding='utf-8') as f:
                                                    f.write(bs_obj1.decode().strip())
                                                time.sleep(5)
                                                browser.close()
                                                browser.switch_to.window(tabs[0])
                                                time.sleep(10)
                                                idm=idm+1
                                                l=l+1
                                            df2 = pd.read_html(str(table))
                                            df3=pd.DataFrame(df2[0])
                                            #print(i)
                                            df3.to_excel(path+i+".xlsx")
                                            i=int(i)
                                            i=i+1
                                        all_data = pd.DataFrame()
                                        for f in glob.glob(path+'*.xlsx'):
                                           df = pd.read_excel(f)
                                           all_data = all_data.append(df, ignore_index=True)
                                           os.remove(f)
                                        writer = pd.ExcelWriter(village+"_"+pn+'.xlsx')
                                        all_data.to_excel(writer, sheet_name='Sheet1')
                                        writer.save()
                                        print("Data Saved")
                                        ##browser.delete_all_cookies()
                                        browser.close()
                                        browser.implicitly_wait(10)
                                        time.sleep(15)
                                        j=j-1
                                        ind=ind+1

                            except:
                                print("Website too Slow or Browser Closed")
                                browser.close()
                                #os.rmdir(name+"/"+y+"/"+alph+"/"+str(p)+"/"+village)
                                insideloop=1
                                break









    else:
        name="Mumbai sub"
        if not os.path.exists(name):
            os.makedirs(name)

        for y in year:
            if not os.path.exists(name+"/"+y):
                os.makedirs(name+"/"+y)

            for alph in alphabet:
                if not os.path.exists(name+"/"+y+"/"+alph):
                    os.makedirs(name+"/"+y+"/"+alph)


                for p in pn:
                    while loop==1:

                        while insideloop==1:
                            try:
                                insideloop=0
                                URL = 'https://freesearchigrservice.maharashtra.gov.in/'
                                browser=webdriver.Firefox()
                                browser.get(URL)
                                ##browser.delete_all_cookies()
                                time.sleep(2)
                                district = Select(browser.find_element_by_id('ddlDistrict'))
                                ds=browser.find_element_by_id('ddlDistrict')
                                #ds.click()
                                district.select_by_value(a)
                                ys=browser.find_element_by_name("ddlFromYear")
                                years = Select(browser.find_element_by_name("ddlFromYear"))
                                years.select_by_value(y)
                                time.sleep(5)
                                Vname = browser.find_element_by_name("txtAreaName")
                                Vname.send_keys(alph)
                                ds=browser.find_element_by_id('ddlDistrict')
                                ds.click()
                                time.sleep(2)
                                vs=browser.find_element_by_name("ddlareaname")
                                vs.click()
                                time.sleep(5)
                                Vselect = Select(browser.find_element_by_name("ddlareaname"))
                                listofelements=browser.find_elements_by_xpath('//*[@name="ddlareaname"]/option')
                                if not os.path.exists(name+"/"+y+"/"+alph+"/"+str(p)):
                                    os.makedirs(name+"/"+y+"/"+alph+"/"+str(p))
                                if len(listofelements)<=1:
                                    os.rmdir(name+"/"+y+"/"+alph+"/"+str(p))
                                    p=999999
                                    loop=0
                                    ##browser.delete_all_cookies()

                                    browser.close()
                                    break
                                if ind>=len(listofelements):
                                    loop=loop-1
                                    break
                                village=str(listofelements[ind].text)
                                print(village)
                                if not os.path.exists(name+"/"+y+"/"+alph+"/"+str(p)+"/"+village):
                                    os.makedirs(name+"/"+y+"/"+alph+"/"+str(p)+"/"+village)
                                district = Select(browser.find_element_by_id('ddlDistrict'))
                                ds=browser.find_element_by_id('ddlDistrict')
                                #ds.click()
                                district.select_by_value(a)
                                ys=browser.find_element_by_name("ddlFromYear")
                                years = Select(browser.find_element_by_name("ddlFromYear"))
                                years.select_by_value(str(y))
                                time.sleep(5)
                                browser.find_element_by_name("txtAreaName").clear()
                                Vname = browser.find_element_by_name("txtAreaName")
                                Vname.send_keys(alph)
                                ds=browser.find_element_by_id('ddlDistrict')
                                ds.click()
                                time.sleep(2)
                                vs=browser.find_element_by_name("ddlareaname")
                                vs.click()
                                time.sleep(5)
                                Vselect = Select(browser.find_element_by_name("ddlareaname"))
                                Vselect.select_by_value(village)
                                pnumber = browser.find_element_by_name("txtAttributeValue")
                                pnumber.send_keys(str(p))
                                time.sleep(10)
                                #c=1
                                cl1=1
                                cl2=1
                                while cl1==1:
                                    elem = browser.find_element_by_xpath('//*[@id="imgCaptcha"]')
                                    action_chain = ActionChains(browser)
                                    action_chain.move_to_element(elem)
                                    action_chain.perform()
                                    loc, size = elem.location_once_scrolled_into_view, elem.size
                                    left, top = loc['x'], loc['y']
                                    width, height = size['width'], size['height']
                                    box = (int(left), int(top), int(left + width), int(top + height))
                                    browser.save_screenshot('screenshot.png')
                                    img = Image.open('screenshot.png')
                                    captcha = img.crop(box)
                                    captcha.save('screenshot.png', 'PNG')
                                    #browser.save_screenshot('screenshot.png')
                                    captcha = browser.find_element_by_name("txtImg")
                                    captcha.clear()
                                    captcha_text = get_captcha_text()
                                    #print(captcha_text)
                                    captcha.send_keys(captcha_text)
                                    time.sleep(5)
                                    submit = browser.find_element_by_name("btnSearch")
                                    #print(bool(submit))
                                    submit.click()
                                    time.sleep(10)
                                    while cl2==1:
                                        try:
                                            msg=browser.find_element_by_id("lblimg")
                                            if msg.text == "Entered Correct Captcha":
                                               print("Wrong Captcha Detected")
                                               browser.implicitly_wait(10)
                                               time.sleep(5)
                                               break
                                            else:
                                                cl2=0
                                                cl1=0
                                        except:
                                            cl2=0
                                            cl1=0
                                time.sleep(5)
                                browser.implicitly_wait(15)
                                time.sleep(5)
                                j=1
                                while j==1:
                                    try:
                                        browser.find_element_by_id("lblMsgCTS")
                                        ind=ind+1
                                        os.rmdir(name+"/"+y+"/"+alph+"/"+str(p)+"/"+village)
                                        browser.close()
                                        browser.implicitly_wait(5)
                                        time.sleep(10)
                                        break
                                    except:
                                        bs_obj1 = BSoup(browser.page_source, 'lxml')
                                        table = bs_obj1.find('table', id="RegistrationGrid")
                                        indx=list(bs_obj1.find_all(value='IndexII'))
                                        l=0
                                        idm=2
                                        path=str(name+"/"+y+"/"+alph+"/"+str(p)+"/"+village+"/")
                                        df = pd.read_html(str(table))
                                        df1=pd.DataFrame(df[0])
                                        while l<len(indx):
                                            trm=str(idm)
                                            first_link=browser.find_element_by_xpath("/html/body/form/center/div/div/table/tbody/tr[3]/td/div/table/tbody/tr/td/div[1]/div/table/tbody/tr["+str(trm)+"]/td[10]/input")
                                            first_link.click()
                                            time.sleep(10)
                                            tabs=list(browser.window_handles)
                                            #print(tabs)
                                            browser.switch_to.window(tabs[1])
                                            bs_obj1 = BSoup(browser.page_source,"html.parser").encode()
                                            with open(path+"1 "+str(l)+str(idm)+'.html', 'w', encoding='utf-8') as f:
                                                f.write(bs_obj1.decode().strip())
                                            time.sleep(5)
                                            browser.close()
                                            browser.switch_to.window(tabs[0])
                                            time.sleep(10)
                                            idm=idm+1
                                            l=l+1


                                        df1.to_excel(path+"1.xlsx")
                                        p=df1.values[-1].tolist()
                                        i=2
                                        l=0
                                        idm=2
                                        while(i<=(len(p)-1)):
                                            time.sleep(10)
                                            i=str(i)
                                            browser.find_element_by_link_text(i).click()
                                            browser.implicitly_wait(10)
                                            time.sleep(10)
                                            bs_obj1 = BSoup(browser.page_source, 'lxml')
                                            table = bs_obj1.find('table', id="RegistrationGrid")
                                            index=browser.find_element_by_value("IndexII")
                                            while l<len(indx):
                                                #clck=indx[i]

                                                trm=str(idm)
                                                first_link=browser.find_element_by_xpath("/html/body/form/center/div/div/table/tbody/tr[3]/td/div/table/tbody/tr/td/div[1]/div/table/tbody/tr["+str(trm)+"]/td[10]/input")
                                                first_link.click()
                                                time.sleep(10)
                                                tabs=list(browser.window_handles)
                                                print(tabs)
                                                browser.switch_to.window(tabs[1])
                                                bs_obj1 = BSoup(browser.page_source,"html.parser").encode()
                                                with open(path+"page_"+str(i)+str(l)+str(idm)+'.html', 'w', encoding='utf-8') as f:
                                                    f.write(bs_obj1.decode().strip())
                                                time.sleep(5)
                                                browser.close()
                                                browser.switch_to.window(tabs[0])
                                                time.sleep(10)
                                                idm=idm+1
                                                l=l+1
                                            df2 = pd.read_html(str(table))
                                            df3=pd.DataFrame(df2[0])
                                            #print(i)
                                            df3.to_excel(path+i+".xlsx")
                                            i=int(i)
                                            i=i+1
                                        all_data = pd.DataFrame()
                                        for f in glob.glob(path+'*.xlsx'):
                                           df = pd.read_excel(f)
                                           all_data = all_data.append(df, ignore_index=True)
                                           os.remove(f)
                                        writer = pd.ExcelWriter(village+"_"+pn+'.xlsx')
                                        all_data.to_excel(writer, sheet_name='Sheet1')
                                        writer.save()
                                        print("Data Saved")
                                        ##browser.delete_all_cookies()
                                        browser.close()
                                        browser.implicitly_wait(10)
                                        time.sleep(15)
                                        j=j-1
                                        ind=ind+1

                            except:
                                print("Website too Slow or Browser Closed")
                                browser.close()
                                #os.rmdir(name+"/"+y+"/"+alph+"/"+str(p)+"/"+village)
                                insideloop=1
                                break
