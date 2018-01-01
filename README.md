# Pinterest_scraper
A simple Python image scraper for Pinterest using Selenium and requests. The goal is to enable simple, automated collection of Pinterest images for a given search term. I chose Selenium because Pinterest uses infinite scrolling. Selenium lets us simply hit 'page down' and grab the next set of images.

## Getting Started
You will need a few things on your system to get this working:

1. Python 3.4+
2. Selenium 3.8.0 and requests 2.18.4 (I'm sure earlier versions work too, but I have not tested)
3. Chrome web driver (currently I've got it coded exclusively for Chrome, that's an easy fix of course)

### Python 3.4+
Many tutorials exist on installing Python, e.g. [Anaconda3] (https://conda.io/docs/user-guide/install/download.html).

### Selenium 
Here's the easiest way:
From [pypi.python.org] (https://pypi.python.org/pypi/selenium).
> If you have pip on your system, you can simply install or upgrade the Python bindings:
```
pip install -U selenium==3.8.0
```

### Requests
Just as with Selenium
```
pip intall requests==2.18.4
```

### Chrome web driver
A comprehensive installation guide for ChromeDriver is available here:
[SeleniumHQ github](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver)

## Running the scraper
Using an existing Python distribution, navigate to the folder in which you would like to store a subfolder containing your scraped images.

There are 3 mandatory positional arguments, and two optional positional arguments:
1. Login name
2. Login pass
3. Search term to be scraped
4. Destination folder for scraped images [.\scraped_images]
5. Chromedriver path [C:/Program Files/Web Drivers/chromedriver.exe]

Since this was a quick and dirty solution to Pinterest scraping, you've got to have the destination folder argument (4) if you want to use the chromedriver path agument (5).
```
python pinterest_scraper.py [1] [2] [3] [4] [5]
```

You should then be on your way to collecting images! 

## Prospects for improvement
Right now, there is no way to terminate the search besides closing the browser it opens or closing the command line instance (or really any other form of crashing the program). Adding a thread to listen for a quit command, or opening a simple interface with a "quit" button would be handy.

There is also room for improving the scraper's speed by tuning the pauses between actions.
