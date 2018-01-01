
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from random import normalvariate
from time import sleep
import os
import requests
import sys

'''
Here's my S.O.P. for getting the original images:
1: Get a list of the pictures that are present.
2: Extract the paths to the originals
2.1: Get the names of the files too
3: Save each unique picture
'''

# orig_lst = []
# for i in pics_list[1:]:  # The first pic is always your profile pic
#     # Do other things here instead
#     orig_lst.append(i.get_attribute('srcset').split()[-2])


class PinterestScraper(object):
    def __init__(self, login_name, login_pass, chromedriver_path='C:/Program Files/Web Drivers/chromedriver.exe'):
        self.login_name = login_name
        self.login_pass = login_pass
        try:
            self.driver = webdriver.Chrome()  # os.path.join(os.curdir, 'chromedriver.exe'
        except WebDriverException:
            self.driver = webdriver.Chrome(executable_path=chromedriver_path)
        self.driver.get("https://www.pinterest.com")
        self.path = ''
        self.scraped_list = []

        self.driver.implicitly_wait(30)

    def login(self):
        try:
            login_elem = self.driver.find_element_by_class_name('lightGrey')
            login_elem.send_keys(Keys.ENTER)
            sleep(abs(normalvariate(3, 0.2)))
            email_elem = self.driver.find_element_by_name('id')
            email_elem.send_keys(self.login_name)
            sleep(abs(normalvariate(3, 0.2)))
            pw_elem = self.driver.find_element_by_name('password')
            pw_elem.send_keys(self.login_pass)
            sleep(abs(normalvariate(3, 0.2)))
            login_elem = self.driver.find_element_by_class_name('SignupButton')
            login_elem.send_keys(Keys.RETURN)
        except NoSuchElementException:
            sleep(abs(normalvariate(3, 0.2)))
            email_elem = self.driver.find_element_by_name('id')
            email_elem.send_keys(self.login_name)
            sleep(abs(normalvariate(3, 0.2)))
            pw_elem = self.driver.find_element_by_name('password')
            pw_elem.send_keys(self.login_pass)
            sleep(abs(normalvariate(3, 0.2)))
            login_elem = self.driver.find_element_by_class_name('SignupButton')
            login_elem.send_keys(Keys.ENTER)

    def set_destination_folder(self, path):
        self.path = path
        self.scraped_list = os.listdir(self.path)

    def scrape_pictures(self, query, n_pgdn=500):

        if ' ' in query:
            query.replace(' ', '  ')  # Pinterest likes to bring up a history
                                      # instead of letting you type your first space
        search_input = self.driver.find_element_by_class_name('searchInput')
        search_input.send_keys(query)

        # We have to reacquire the element after the page changes at all
        search_input = self.driver.find_element_by_class_name('searchInput')
        search_input.send_keys(Keys.RETURN)

        sleep(3)  # this is just a hack to get the page to load properly
        # cur_pgdn = 0
        for i in range(n_pgdn):
            pics_list = self.driver.find_elements_by_class_name('_mi')
            pics_list = pics_list[1:]
            pic_url_list = [pic_elem.get_attribute('srcset').split(' ')[-2] for pic_elem in pics_list]
            for pic_url in pic_url_list:
                pic_name = pic_url.split('/')[-1]
                if pic_name not in self.scraped_list:
                    pic = requests.get(pic_url)
                    file = open(os.path.join(self.path, pic_name), 'wb')
                    file.write(pic.content)
                    file.close()
                    self.scraped_list.append(pic_name)
                    sleep(abs(normalvariate(abs(normalvariate(1.2, 0.2)), abs(normalvariate(0.4, 0.1)))))
                # This way we save an image about every 1.2 seconds. That's plenty of images in not much time.
                # I chose to do this variable sleep time just because I saw someone else doing the same thing.
                # I do not know if Pinterest is looking for automated activity, so it might be unnecessary.
            body = self.driver.find_element_by_css_selector('body')
            for j in range(2):
                body.send_keys(Keys.PAGE_DOWN)
            sleep(2)  # this give the page time to actually SCROLL!
            # cur_pgdn += 1


def main():
    try:
        my_scraper = PinterestScraper(login_name=sys.argv[1], login_pass=sys.argv[2], chromedriver_path=sys.argv[5])
    except IndexError:
        my_scraper = PinterestScraper(login_name=sys.argv[1], login_pass=sys.argv[2])
    try:
        my_scraper.set_destination_folder(sys.argv[4])
    except IndexError:
        my_scraper.set_destination_folder(os.path.join(os.curdir, "scraped_images"))

    sleep(3)
    my_scraper.login()
    sleep(3.2)

    my_scraper.scrape_pictures(sys.argv[3])


if __name__ is "__main__":
    main()
