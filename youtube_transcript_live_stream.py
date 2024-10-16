from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Path to ChromeDriver
driver_path = r'C:\Users\richa\Documents\chromedriver-win64\chromedriver.exe'
service = Service(driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# Open the YouTube video page
driver.get('https://www.youtube.com/watch?v=oGBmEK_FwXQ')

# Wait until the video page loads and then click the play button
try:
    # Wait for the play button to be clickable
    print("Waiting for the play button...")
    play_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ytp-large-play-button.ytp-button"))
    )
    play_button.click()
    print("Play button clicked. Video is playing.")

except TimeoutException:
    print("Play button not found or already playing.")

# Loop to continuously retrieve captions
retrieved_lines = set()  # Use a set to store unique lines of captions

try:
    while True:
        # Extract captions that are directly on the screen (if available)
        try:
            print("Looking for captions directly on the screen...")
            captions_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.ytp-caption-segment"))
            )
            with open(r'C:\Users\richa\Desktop\YouTube Video\youtube_captions_live.txt', 'a', encoding='utf-8') as f:
                for caption in captions_elements:
                    if caption.text not in retrieved_lines:
                        f.write(caption.text + '\n')
                        retrieved_lines.add(caption.text)

            # Print the latest caption for monitoring
            if captions_elements:
                print(f"Latest Caption: {captions_elements[-1].text}")

        except TimeoutException:
            print("No captions found on the screen at the moment...")

        # Wait before retrieving again
        time.sleep(5)

except KeyboardInterrupt:
    # Graceful shutdown on Ctrl+C
    print("Stopping caption retrieval...")

finally:
    driver.quit()
