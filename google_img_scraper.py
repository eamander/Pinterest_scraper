
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from random import normalvariate
from time import sleep
import os
import requests
from requests.exceptions import SSLError, ConnectionError
import sys
import json

'''
Here's my S.O.P. for getting the original images:
1: Get a list of the pictures that are present.
2: Extract the paths to the originals
2.1: Get the names of the files too
3: Save each unique picture
'''


class GoogleImgScraper(object):
    def __init__(self, chromedriver_path='C:/Program Files/Web Drivers/chromedriver.exe'):
        try:
            self.driver = webdriver.Chrome()  # os.path.join(os.curdir, 'chromedriver.exe'
        except WebDriverException:
            self.driver = webdriver.Chrome(executable_path=chromedriver_path)
        self.driver.get("https://www.google.com/imghp?hl=en&tab=wi&authuser=0")
        self.path = ''
        self.scraped_list = []

        self.driver.implicitly_wait(30)

    def set_destination_folder(self, path):
        self.path = path
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.scraped_list = os.listdir(self.path)

    def scrape_pictures(self, query, n_pgdn=500, name_with_query=False):

        search_input = self.driver.find_element_by_class_name('gsfi')
        search_input.send_keys(query)

        # We have to reacquire the element after the page changes at all
        search_input = self.driver.find_element_by_class_name('gsfi')
        search_input.send_keys(Keys.RETURN)

        sleep(2)  # this is just a hack to get the page to load properly
        # cur_pgdn = 0
        for i in range(n_pgdn):
            if name_with_query:
                self.scrape_cur_view(query)
            else:
                self.scrape_cur_view()

            body = self.driver.find_element_by_css_selector('body')
            for j in range(10):
                body.send_keys(Keys.PAGE_DOWN)
                sleep(0.4)
            sleep(.3)  # this give the page time to actually SCROLL!
            # cur_pgdn += 1

    def scrape_cur_view(self, names=None):
        pics_list = self.driver.find_elements_by_class_name('rg_meta')
        pic_url_list = []
        pic_name_index = 0
        # To update this, find a better way to pick off a good file name
        for pic_elem in pics_list:
            try:
                elem_text = pic_elem.get_property('innerText')
                elem_json = json.loads(elem_text)
                pic_url = elem_json['ou']
                pic_url_list.append(pic_url)
            except KeyError:
                pass
        for pic_url in pic_url_list:
            if names is not None:
                pic_name = names + "_{}.jpg".format(pic_name_index)
                pic_name_index += 1
            else:
                pic_name = pic_url.split('/')[-1].split('%')[-1].split('&')[-1]
                if '?' in pic_name:
                    split = pic_name.split('?')
                    if len(split[0]) > len(split[-1]):
                        pic_name = split[0]
                    else:
                        pic_name = split[1]
                if 'jpg' not in pic_name:
                    pic_name = pic_name + '.jpg'
            if pic_name not in self.scraped_list:
                try:
                    pic = requests.get(pic_url)
                    file = open(os.path.join(self.path, pic_name), 'wb')
                    file.write(pic.content)
                    file.close()
                    self.scraped_list.append(pic_name)
                    sleep(abs(normalvariate(abs(normalvariate(.5, 0.2)), abs(normalvariate(0.4, 0.1)))))
                except (SSLError, ConnectionError):
                    pic_name_index -= 1
            else:
                flag = True
                count = 0
                pic_name_orig = pic_name
                while flag:
                    pic = requests.get(pic_url)
                    if os.path.exists(os.path.join(self.path, pic_name)):
                        file = open(os.path.join(self.path, pic_name), 'rb')
                        file_content = file.read()
                        if pic.content == file_content:
                            flag = False
                        else:
                            pic_name = pic_name_orig[:-4] + '_{}'.format(count) + '.jpg'
                            count += 1
                    else:
                        pic = requests.get(pic_url)
                        file = open(os.path.join(self.path, pic_name), 'wb')
                        file.write(pic.content)
                        file.close()
                        self.scraped_list.append(pic_name)
                        sleep(abs(normalvariate(abs(normalvariate(.5, 0.2)), abs(normalvariate(0.4, 0.1)))))
                        flag = False


def main(argv):

    raise NotImplementedError

    try:
        my_scraper = PinterestScraper(login_name=argv[1], login_pass=argv[2], chromedriver_path=argv[5])
    except IndexError:
        my_scraper = PinterestScraper(login_name=argv[1], login_pass=argv[2])
    try:
        my_scraper.set_destination_folder(argv[4])
    except IndexError:
        my_scraper.set_destination_folder(os.path.join(os.curdir, "scraped_images"))

    sleep(3)
    my_scraper.login()
    sleep(3.2)

    my_scraper.scrape_pictures(argv[3])

'''
if __name__ == "__main__":
    main(sys.argv)
'''
