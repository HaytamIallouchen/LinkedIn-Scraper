# import web driver, datetime, tqdm and own settings
from datetime import datetime
from tqdm import tqdm
import settings
import LinkedInController as LinkedIn

# create new linkedin controller
linkedin = LinkedIn.LinkedInController()

# login into linkedin
try:
    linkedin.login(settings.mail, settings.password)
except:
    print(f"{datetime.now()} Login failed, please check your username and password, or capcha detected...")

# set page limits
page = settings.page_start
page_max = settings.page_end
current_page = page

# get the data from the given page

lis = linkedin.filter_page(page)

# create a list to store the data of each page
scrapedData = []

print(f"{datetime.now()} Accessessing {str(page_max)} pages\n")
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

            # get full name
            try:
                full_name = li.find_element("xpath", './div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]').text
                
                # handle the names if more than one name
                first_name = full_name.split(' ')[0] if len(full_name.split(' ')) > 0 else ''
                middle_names = full_name.split(' ')[1:-1] if len(full_name.split(' ')) >= 2 else ''
                last_name = full_name.split(' ')[-1] if first_name != '' else ''
            # if name not found, next iteration
            except:
                continue
                
            # get job title, location, and img url if exist in li
            try:
                job_title = li.find_element('xpath', './div/div/div[2]/div[1]/div[2]/div[1]').text
            except:
                job_title = 'No job title'
            try:
                location = li.find_element('xpath', './div/div/div[2]/div[1]/div[2]/div[2]').text
            except:
                location = 'No location'
            try:
                img_url = li.find_element('xpath', './div/div/div[1]/div/a/div/div/div/img').get_attribute('src')
            except:
                img_url = 'No picture'

            # create a dictionary to store the data of the person and add to list
            person_object = {
                'first_name': first_name,
                'middle_names': middle_names,
                'last_name': last_name,
                'job_title': job_title,
                'location': location,
                'url': href,
                'img_url': img_url,
            }
            pageData.append(person_object)

        # next page
        current_page += 1
        lis = linkedin.filter_page(current_page)
        scrapedData.extend(pageData)
else:
    print(f"{datetime.now()} No results found")

# print the data enumerated
for i, person in enumerate(scrapedData):
    print(f"\n🛠' {str((i + 1))}. --------------------------------------------------------🛠\n {person}")
