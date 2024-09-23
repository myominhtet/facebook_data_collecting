
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv
from argparse import ArgumentParser
import re

parser = ArgumentParser()

def is_valid_url(url):
    # Regular expression to validate URLs
    url_regex = r"^(http|https)://[^\s/$.?#].[^\s]*$"
    return re.match(url_regex, url) is not None

if __name__ == "__main__":
    parser.add_argument("--username", type=str, help="Username for authentication")
    parser.add_argument("--password", type=str, help="Password for authentication")
    parser.add_argument("--link", type=str, help="Link to the page or profile")
    
    parser.add_argument("--page", action="store_true", help="Scrape as a page")
    parser.add_argument("--profile", action="store_true", help="Scrape as a profile")
    
    args = parser.parse_args()

    if not any([args.page, args.profile]):
        parser.error("Please specify --page or --profile")

    if not is_valid_url(args.link):
        parser.error("Invalid link format. Please provide a valid URL.")

    # Your scraping logic goes here
    print("Username:", args.username)
    print("Password:", args.password)
    print("Link:", args.link)
    print("Page:", args.page)
    print("Profile:", args.profile)

# Chrome WebDriver Setup
# chrome_options = Options()
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--window-size=1920x1080")
# from selenium.webdriver.chrome.service import Service

# chrome_service = Service('/bin/chromedriver')  # Path to ChromeDriver
# driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
chrome_options = webdriver.ChromeOptions()
chrome_service = Service("/usr/local/bin/chromedriver")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-notifications")
chrome_options.binary_location = "/usr/bin/google-chrome-stable" 
# Initialize the driver with timeout values
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.set_page_load_timeout(30)  # Set page load timeout in seconds
driver.implicitly_wait(10)  # Implicitly wait for elements to be found

# Facebook Login
driver.get('https://www.facebook.com/login/')

time.sleep(1)

# Create directory for saving data
dir = './scraped_data/'
if not os.path.exists(dir):
    os.makedirs(dir)

# Login to Facebook
driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(args.username)
driver.find_element(By.XPATH, '//*[@id="pass"]').send_keys(args.password)
driver.find_element(By.XPATH, '//*[@id="loginbutton"]').click()
time.sleep(3)
# Handle Notifications
# try:
#     allow_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//*[text()="Allow"]'))
#     )
#     allow_button.click()
# except Exception as e:
#     print("No notification block appeared or an error occurred:", e)

# Navigate to the specified page or profile link
driver.get(args.link)
time.sleep(3)

# Text scraping for Facebook Page
data = []
total_text_saved = 0

def extract_new_posts():
    global data
    global total_text_saved
    new_data = []  # To store new posts found during this execution

    # Scroll to load more posts
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for posts to load

    # Find all posts on the page
    posts = driver.find_elements(By.CSS_SELECTOR, ".xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.x126k92a") # Update this selector as needed

    # Loop through the posts and extract text
    for post in posts:
        try:
            # Click "See more" if it exists
            see_more_buttons = post.find_elements(By.XPATH, './/div[@role="button" and contains(text(), "See more")]')
            for button in see_more_buttons:
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)  # Wait for the content to expand

            # Extract the text after expanding the post
            post_html = post.get_attribute('outerHTML')
            soup = BeautifulSoup(post_html, 'html.parser')
            div_elements = soup.find_all('div')

            # Extract raw text from the div elements
            extracted_text = [div.get_text() for div in div_elements]
            for text in extracted_text:
                if text not in data:
                    data.append(text)
                    new_data.append(text)  # Store new text in this session
                    total_text_saved += 1
                    print("Text added:", text)

        except Exception as e:
            print(f"An error occurred while processing the post: {e}")

    return new_data  # Return new posts found




# Main loop for real-time monitoring
while True:
    new_data = extract_new_posts()

    # Append the raw data to the CSV file without overwriting previous entries
    with open(dir + 'voaburmese.csv', 'a', newline='', encoding='utf-8') as F:
        writer = csv.writer(F)

        # Write the header only if the file is empty or being created
        if os.stat(dir + 'voaburmese.csv').st_size == 0:
            writer.writerow(['text'])

        # Write new data if there is any
        for item in new_data:
            writer.writerow([item])
    
    print(f"Total text saved so far: {total_text_saved}")
    print("Use Ctrl+C to stop the program")
    
    time.sleep(10)

