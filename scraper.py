from selenium import webdriver
from bs4 import BeautifulSoup as soup
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import config
import time
import requests
import csv
import os

username = config.username
password = config.password

def download_file(url, file_name):
    # Make the directory if it doesn't exist
    os.makedirs('source', exist_ok=True)

    # Combine with directory to get file path
    file_path = os.path.join('source', file_name)

    # Download and save the file in the directory
    with open(file_path, 'wb') as file:
        response = requests.get(url)
        file.write(response.content)

options = webdriver.ChromeOptions()

# options.add_argument('--headless=new')
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("start-maximized")

headers = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImYyOThjZDA3NTlkOGNmN2JjZTZhZWNhODExNmU4ZjYzMDlhNDQwMjAiLCJ0eXAiOiJKV1QifQ.eyJ3b3Jrc3BhY2VfaWQiOiI3MTEwYzIzMWZhOWI0YmZlOThkNjEzZmJlZjhjOGVhNyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS94aS1sYWJzIiwiYXVkIjoieGktbGFicyIsImF1dGhfdGltZSI6MTcxMzQ1NDc0NSwidXNlcl9pZCI6ImZJZ0lUWFhXR2hTOXdzZTZPb0lqbWNNTmxqRjMiLCJzdWIiOiJmSWdJVFhYV0doUzl3c2U2T29Jam1jTU5sakYzIiwiaWF0IjoxNzEzNDU4MzY1LCJleHAiOjE3MTM0NjE5NjUsImVtYWlsIjoic2hpbnkxMGtAc2tpZmYuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsic2hpbnkxMGtAc2tpZmYuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.XX2J_wzrVT8tsASYkOwt1kVxB16HHmGS3aATaL0_zG2DURYi-rjggEBab3782eMXwCXXfyEK6XJek7abX7rSKAeqwbHLh7fJvMBdj3QqizY5TaWmfN2JF95Pp7IFuFXGAn6cQ4Guh7Rul247yq8C_S_H0GTgjxJobcN-P-yGfUReQeMDzwh_PNDiB9MkG2He3MQHJXVzdhSujHjl5bYzvDT-R6aZdVUZa55_JLxr33RCEjQCrrJKWkaJQwkmXOmRpDwYnz3bR0Kyc12JaymgbLQlgGOLhKspqIPf6kp0MZ8pXntm5nOEp6Aj9cDgxco-i2mMOzhzYnpcO4HzSKaIFg'}
url = "https://api.elevenlabs.io/v1/shared-voices?page_size=30&category=professional&gender=male&age=young&language=en&accent=american&use_cases=narrative_story&sort=trending"

response = requests.get(url, headers=headers)
if response.ok:
    voice_data = response.json()
    voice_data = voice_data["voices"]  # Get the first item
else:
    print(f'Request failed with status code: {response.status_code}')

csv_data = [['UserID', 'Name', 'Short Description', 'Long Description', 'Category', 'Gender', 'Age', 'Language', 'Accent', 'Tone', 'Keywords', 'Sample File Name', 'Number of Users', 'Number of Characters of Audio Generated']]


with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:  # modified
    driver.set_window_size(1366, 768)

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    # Navigate to the website
    driver.get('https://elevenlabs.io/')

    try:
        driver.find_element("xpath", '//*[@id="app-root"]/div[4]/div/div/div[2]/div[3]/span').click()

        login_username = driver.find_element("xpath", '//*[@id="sign-in-form"]/div[2]/input')
        login_username.clear()
        login_username.send_keys(username)

        login_password = driver.find_element("xpath", '//*[@id="sign-in-form"]/div[3]/input')
        login_password.clear()
        login_password.send_keys(password)

        driver.find_element("xpath", '//*[@id="sign-in-form"]/div[5]/button').click()
        time.sleep(3)

        driver.find_element("xpath", '//*[@id="authenticated-root"]/div[3]/div[2]/nav/ul/a[2]/div').click()
        time.sleep(3)

        driver.find_element("xpath", '//*[@id="authenticated-root"]/div[5]/div[2]/div/div/div[1]/div/div/button[2]').click()
        time.sleep(1)

        #Filtering
        driver.find_element("xpath", '//*[@id="authenticated-root"]/div[5]/div/div/div/div/div[2]/div/div[1]/div/div[1]/div[2]/div/div[1]').click()
        
        driver.find_element("xpath", '//*[@id="expand-collapse"]').click()
        time.sleep(1)

        #Category
        category_elements = driver.find_elements(By.CSS_SELECTOR, '.w-36')

        category_elements[0].click()
        driver.find_element("xpath", '//div[@aria-label="Professional"]').click()

        #Gender
        category_elements[1].click()
        driver.find_element("xpath", '//div[@aria-label="Male"]').click()

        #Age
        category_elements[2].click()
        driver.find_element("xpath", '//div[@aria-label="Young"]').click()

        #Language
        category_elements[3].click()
        english_option = driver.find_element("xpath", '//div[@aria-label="English"]')
        # scroll the element into view
        driver.execute_script("arguments[0].scrollIntoView();", english_option)
        # click the element
        english_option.click()
        time.sleep(1)

        #Accent
        category_elements = driver.find_elements(By.CSS_SELECTOR, '.w-36')
        category_elements[4].click()
        time.sleep(1)
        driver.find_element("xpath", '//div[@aria-label="American"]').click()
        time.sleep(3)

        voice_libraries = driver.find_elements("xpath", '//*[@id="authenticated-root"]/div[5]/div/div/div/div/div[2]/div/div[2]/div/ul//li')

        for index, voice_library in enumerate(voice_libraries):
            html = voice_library.get_attribute('innerHTML')
            elem_soup = soup(html, "html.parser")

            name_spans = elem_soup.select('div > div > div > div > div:nth-of-type(2) > span')
            name = name_spans[0].get_text()

            short_description_spans = elem_soup.select('div > div > div > div > div:nth-of-type(3) > span > span')
            short_description = short_description_spans[0].get_text()

            long_description_spans = elem_soup.select('div > div > div > div > div:nth-of-type(4) > div > span')
            long_description = long_description_spans[0].get_text()

            # category_spans = elem_soup.select('div > div > div > div > div:nth-of-type(5) > span')
            # category = ""
            # for category_span in category_spans:
            #     category = category + category_span.get_text() + ", "
            # category = category[:-2]
            # print(category)
            userid = voice_data[index]['voice_id']
            category = voice_data[index]['category']
            gender = voice_data[index]['gender']
            age = voice_data[index]['age']
            language = voice_data[index]['language']
            accent = voice_data[index]['accent']
            tone = voice_data[index]['descriptive']
            keywords = "" + gender + ", " + age + ", " + language + ", " + accent + ", " + tone 
            sample_file_name = "voice_preview_" + voice_data[index]['name']
            number_of_users = voice_data[index]['cloned_by_count']
            number_of_characters = voice_data[index]['usage_character_count_1y']

            download_file(voice_data[index]['preview_url'], sample_file_name)

            csv_data.append([userid, name, short_description, long_description, category, gender, age, language, accent, tone, keywords, sample_file_name, number_of_users, number_of_characters])
            
        filename = "voices_library.csv"

        # writing to csv file
        with open(filename, 'w', newline='') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            
            # writing the data onto the CSV file
            csvwriter.writerows(csv_data)

        time.sleep(5)
    except Exception as e:
        print(e)