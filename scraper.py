from selenium import webdriver
import time
import os
from bs4 import BeautifulSoup
import csv
from selenium.webdriver.common.by import By
print("Test Execution Started")
options = webdriver.ChromeOptions()
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
# options.add_argument("--headless")  # Enable headless mode for Docker
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("--remote-debugging-port=9222")  # Add this line
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Remote(
    command_executor='http://localhost:4444',  # Remove /wd/hub
    options=options
)

#maximize the window size
driver.maximize_window()
time.sleep(10)
driver.get('https://www.facebook.com/login/')


# # Login to Facebook
driver.find_element(By.XPATH, '//*[@id="email"]').send_keys("+959795991873")
driver.find_element(By.XPATH, '//*[@id="pass"]').send_keys("12345ys")
driver.find_element(By.XPATH, '//*[@id="loginbutton"]').click()
time.sleep(3)
driver.get("https://www.facebook.com/VOABurmese/")
time.sleep(3)
print("finished")

# Create directory for saving data
dir = './scraped_data/'
if not os.path.exists(dir):
    os.makedirs(dir)

data = []
total_text_saved = 0

def extract_new_posts():
    global data
    global total_text_saved
    new_data = []  
    
    # Scroll multiple times to load more posts
    for _ in range(1):  # Adjust the number of scrolls based on how many posts you want to load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

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

