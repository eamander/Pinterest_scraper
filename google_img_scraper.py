
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
from PIL import Image
import io

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
        self.scraped_list_content = []
        self.scraped_list_fullpath = []

        self.driver.implicitly_wait(30)

    def set_destination_folder(self, path):
        self.path = path
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.scraped_list = os.listdir(self.path)

    def set_check_folders(self, list_path=[]):
        self.scraped_list_fullpath = [*map(lambda f: os.path.join(self.path, f), self.scraped_list)]

        for path in list_path:
            if os.path.exists(path):
                self.scraped_list_fullpath.extend([*map(lambda f: os.path.join(path, f), os.listdir(path))])
            else:
                UserWarning("Directory not found at path {}".format(path))

    def compare_picture(self, pic,  check_old_images=False):
        if not check_old_images:
            return True
        else:
            if pic in self.scraped_list_content:
                return False
            else:
                return True

    def open_existing_pics(self):
        self.scraped_list_content = []
        for path in self.scraped_list_fullpath:
            img = Image.open(path)
            self.scraped_list_content.append(img)

    def scrape_pictures(self, query, n_pgdn=500, name_with_query=False, check_old_images=False):

        if check_old_images and not self.scraped_list_content:
            self.open_existing_pics()

        search_input = self.driver.find_element_by_class_name('gsfi')
        search_input.send_keys(query)

        # We have to reacquire the element after the page changes at all
        search_input = self.driver.find_element_by_class_name('gsfi')
        search_input.send_keys(Keys.RETURN)

        sleep(2)  # this is just a hack to get the page to load properly
        # cur_pgdn = 0
        for i in range(n_pgdn):
            if name_with_query:
                self.scrape_cur_view(query, check_old_images=check_old_images)
            else:
                self.scrape_cur_view(check_old_images=check_old_images)

            body = self.driver.find_element_by_css_selector('body')
            for j in range(10):
                body.send_keys(Keys.PAGE_DOWN)
                sleep(0.4)
            sleep(.3)  # this give the page time to actually SCROLL!
            # cur_pgdn += 1

    def scrape_cur_view(self, names=None, check_old_images=False):
        pics_list = self.driver.find_elements_by_class_name('rg_meta')
        pic_url_list = []
        if names is not None:  # This makes sure all new pics show up after old pics.
            indices = [int(n.split('_')[1].split('.')) for n in self.scraped_list]
            indices.sort(reverse=True)
            pic_name_index = indices[0]
        else:
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
            try:
                pic = requests.get(pic_url)
                pic = Image.open(io.BytesIO(pic.content))
            except (SSLError, ConnectionError, OSError):
                pic_name_index -= 1
                pic = False
            if pic:
                add_pic = self.compare_picture(pic, check_old_images)  # Just see if we should add the picture.
                # Then, if we should add it, look for a place to add it.
            else:
                add_pic = False
            if add_pic:  # Here, just look for a valid name.
                while os.path.exists(os.path.join(self.path, pic_name)):  # Find the next good file name
                    pic_name = pic_name.split("_")[0] + "_{}".format(pic_name_index) + ".jpg"
                    pic_name_index += 1
                try:
                    pic.save(os.path.join(self.path, pic_name))
                    self.scraped_list.append(pic_name)
                    self.scraped_list_content.append(pic)
                except OSError:
                    pic_name_index -= 1
                sleep(abs(normalvariate(abs(normalvariate(.25, 0.1)), abs(normalvariate(0.3, 0.1)))))
            # else:  # Here we check to see if the image in question is one we already have.
            #     flag = True  # We shouldn't need to do this if we are good at determining if we should add a pic above
            #     count = 0
            #     pic_name_orig = pic_name
            #     while flag:
            #         if os.path.exists(os.path.join(self.path, pic_name)):
            #             file = open(os.path.join(self.path, pic_name), 'rb')
            #             file_content = file.read()
            #             if pic.content == file_content:
            #                 flag = False
            #             else:
            #                 pic_name = pic_name_orig[:-4] + '_{}'.format(count) + '.jpg'
            #                 count += 1
            #         else:
            #             pic = requests.get(pic_url)
            #             file = open(os.path.join(self.path, pic_name), 'wb')
            #             file.write(pic.content)
            #             file.close()
            #             self.scraped_list.append(pic_name)
            #             sleep(abs(normalvariate(abs(normalvariate(.5, 0.2)), abs(normalvariate(0.4, 0.1)))))
            #             flag = False


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
