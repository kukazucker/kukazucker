from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_page(url) -> None:                          # update file with html page
    driver = webdriver.Safari()
    driver.maximize_window()

    try:
        driver.get(url=url)                         # get page

        with open("page.html", "w") as file:        # save this page into page.html
           file.write(driver.page_source)

    except:
        return False

    finally:
        driver.quit()


def get_categories():                               # get categories without the file
    driver = webdriver.Safari()

    try:
        driver.get(url='https://www.wired.com/coupons/categories')                          # open the page           
        data_category = driver.find_elements(by=By.CLASS_NAME, value='categories__name')    # find a catalog with the categories
        categories = []                                                                     # list of the categories
        for a in data_category:                                                             # add to list a category
            categories.append(a.text.strip())
        return categories                               

    except:
        return False

    finally:
        driver.quit()


def category_link(chapter):                                         # get link of all promocodes in this category
    try:
        r = chapter.lower().split()                                 # lowercase and separated words
        if(chapter.strip().find('&') != -1):                        # if there are & then 
            r.remove('&')                                           # remove this symbol
        r = f'{r[0]}-{r[1]}'                                        # a string of the view first_word-second_word
        return r
    except:
        return False


def get_code(url):                                                  # get promocode and link from a page
    driver = webdriver.Safari()

    try:
        driver.get(url=url)                                         # open page
        promo_n_link = []
        promo_n_link.append(driver.find_element(by=By.CLASS_NAME, value='modal-clickout__code').text.strip())       # promocode
        promo_n_link.append(driver.find_element(by=By.CLASS_NAME, value='btn.modal-clickout__link').get_attribute('href'))  # link
        return promo_n_link

    except:
        return False

    finally:
        driver.quit()

def get_promocodes(category):                                       # main function

    chapter = category_link(category)                               # get the conversion string
    get_page(f'https://www.wired.com/coupons/categories/{chapter}') # update file page.html
    with open('/Users/matthewbroun/Desktop/examples/PromoCodeBot/page.html') as file:       # read this file
        src = file.read()


    try:
        
        soup = BeautifulSoup(src, 'lxml')
        all_coupons = soup.find("div", 'coupons-list').find_all("div", "coupon")            # find all coupon's divs

        codes = []                                                                          # all promocodes
        
        for coupon in all_coupons:
            coupon_data = []                                                                # data of the coupon

            coupon_data.append(coupon.find('h3').get('data-coupon-title'))                  # title
            coupon_data.append(coupon.find('table', 'coupon-info').previous_element.strip())    # description
            promo_n_code = get_code(f"https://www.wired.com/coupons/categories/{chapter}#id-{coupon.get('data-coupon-id')}")    # get promocode and link
            coupon_data.append(promo_n_code[0])                                             # promocode
            coupon_data.append(coupon.find('div', 'coupon__additional').text.strip())       # used 0000 users
            coupon_data.append(promo_n_code[1])                                             # link

            codes.append(coupon_data)                                                       # append this data into codes[]
        
        return codes

    except:
        return False
