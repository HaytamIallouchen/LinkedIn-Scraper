# import web driver, datetime, tqdm and own settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from tqdm import tqdm
import settings

# create a new Chrome session
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# login into linkedin
def login(email: str, password: str):
    """
    This function logs into the linkedin account.
    Parameters:
        email: The email of the linkedin account.
        password: The password of the linkedin account.
    """
    # driver.get method() will navigate to a page given by the URL address
    driver.get('https://www.linkedin.com')
    print(datetime.now(), '/n Enter linkedin website\n')

    # locate email form by_class_name and fill in email
    driver.find_element("id", "session_key").send_keys(email)
    print(datetime.now(), ' Find username field and enter in username...\n')

    # locate password form by_class_name and fill in password
    driver.find_element("id", "session_password").send_keys(password)
    print(datetime.now(), ' Find password field and enter in password...\n')

    # locate submit button by_class_id and click it
    driver.find_element("xpath", "//button[@type='submit']").click()
    print(datetime.now(), ' Click login button, logging in...\n')
try:
    login(settings.mail, settings.password)
except:
    print(datetime.now(
    ), ' Login failed, please check your username and password, or capcha detected...')

# set page limits
page = settings.page_start
page_max = settings.page_end
current_page = page

# get the data from the given page


def filter_page(page: int):
    """
    This function filters the page to only show people.
    Parameters:
        page: The page to be filtered.
    Returns:
        lis: The list of people on the page.
    """
    # driver.get method() will navigate to a filtered linkedin users page given by the URL address
    driver.get(settings.filterPersonsUrl + '&page=' + str(page))

    # locate each li tag name and return the list of all the li tags
    lis = driver.find_elements(
        "xpath", '//li[@class="reusable-search__result-container "]')
    return lis


lis = filter_page(page)

# create a list to store the data of each page
scrapedData = []

print(datetime.now(), ' Accessessing ' + str(page_max) + ' pages\n')
# loop through each page
if len(lis) > 0:

    # tqdm is a progress bar, range argument is each page
    for pageIndex in tqdm(range(page_max)):

        # create a list to store the data of each person
        pageData = []

        # iterate through each li
        for i, li in enumerate(lis):

            # get href value from anchor child element of li and push value to list
            a_childelement = li.find_elements("tag name", "a")[0]
            href = a_childelement.get_attribute("href")

            # get full name, job title, and company name from the li
            full_name = li.find_elements(
                "xpath", '//span[@dir="ltr"]')[i].find_elements('tag name', 'span')[0].text
            job_title = li.find_element(
                'xpath', './div/div/div[2]/div[1]/div[2]/div[1]').text
            location = li.find_element(
                'xpath', './div/div/div[2]/div[1]/div[2]/div[2]').text

            # get img url from the list item if exist

            # get img url from the list item if exist
            try:
                img_url = li.find_element(
                    'xpath', './div/div/div[1]/div/a/div/div/div/img').get_attribute('src')
            except:
                img_url = None

            # create a dictionary to store the data of the person and add to list
            person_object = {
                'first_name': full_name.split(' ')[0],
                'last_name': full_name.split(' ')[1],
                'job_title': job_title,
                'location': location,
                'url': href,
                'img_url': img_url if img_url else 'No picture',
            }
            pageData.append(person_object)

        # next page
        current_page += 1
        lis = filter_page(current_page)
        scrapedData.extend(pageData)
else:
    print(datetime.now(), ' No results found')

# print the data
for i, person in enumerate(scrapedData):
    print('\n🛠', str((i + 1)) + '. --------------------------------------------------------🛠\n', person, )
