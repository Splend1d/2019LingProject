from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import sys
import os
from time import sleep as sleep
import json
import pickle
import pandas as pd
import jieba
# a crawler class that handle all the crawling of webpages


class Crawler():

    def __init__(self):
        chromedriver = 'driver/chromedriver.exe'
        if hasattr(sys, '_MEIPASS'):
            self.driver = os.path.join(sys._MEIPASS, chromedriver)
        else:
            self.driver = chromedriver

        self.browser = webdriver.Chrome(self.driver)
        self.mouse = webdriver.common.action_chains.ActionChains(self.browser)
        # self.browser.get('https://content.steeluniversity.org/simulators/bos/index.html')
        self.browser.get('https://pulipulichen.github.io/HTML5-Text-Analyzer/')
        self.rawdata = []
        self.parseddata = {}
        self.newsid = 1000000

    def crawl(self, source_data):
        self.rawdata = []
        self.browser.find_element_by_xpath('//*[@id="text_input"]').value = source_data
        # textarea.click()
        # textarea.send_keys(source_data)

        sleep(0.2)
        self.browser.find_element_by_xpath('//*[@id="segment_0161207"]/div[1]/div[2]/div[4]/button').click()

        # test if the website has finished analysing
        verify = self.browser.find_element_by_xpath('//*[@id="result_container"]/div/div[2]/div/div[1]/div/table/tbody/tr[1]/td[1]').text
        while(len(verify) < 1):
            verify = self.browser.find_element_by_xpath('//*[@id="result_container"]/div/div[2]/div/div[1]/div/table/tbody/tr[1]/td[1]').text

        for i in range(1, 20):
            try:
                outer_table = self.browser.find_element_by_css_selector('#result_container > div > div:nth-child(2) > div > div:nth-child(' + str(i) + ')')

            except:
                break
            else:
                table_title = outer_table.find_element_by_css_selector('div > div').text
                self.rawdata.append(table_title.split('\n'))

            # for tr in outer_table.find_elements_by_tag_name('tr'):
            #     tds = tr.find_elements_by_tag_name('td')
            #     if tds:
            #         self.datas.append([td.text for td in tds])

    def parse(self, news):
        self.newsid += 1
        partialparse = {}
        for col in self.rawdata:
            main_analyze_name = col[0]
            partialparse[main_analyze_name] = []
            header = False
            for tr in col[1:]:
                if tr == "TABLE":
                    continue
                elif tr == "VALUE":
                    partialparse[main_analyze_name].append({})
                    header = True
                    continue
                elif header:
                    partialparse[main_analyze_name][-1]['KEY'] = tr.split()[0]
                    partialparse[main_analyze_name][-1]['VALUE'] = tr.split()[1]
                    header = False
                else:
                    v = tr.split()[-1]
                    try:
                        v = int(v)
                    except:
                        try:
                            v = float(v)
                        except:
                            pass
                    partialparse[main_analyze_name][-1][' '.join(tr.split()[:-1])] = v
            self.parseddata[self.newsid] = {'news': news, 'info': partialparse}

    def save(self):
        with open('data.json', 'w') as f:
            json.dump(self.parseddata, f)


source = ['newslens']
c = Crawler()
count = 1
for s in source:
    df = pd.read_pickle(s + ".pkl")
    for i in range(len(df.index)):
        news = df['content_str'][i]
        news_tag = ' '.join(jieba.cut(news))
        c.crawl(news_tag)
        c.parse(news)
        c.save()
        sleep(0.5)
        print(count, 'done')
        count += 1
