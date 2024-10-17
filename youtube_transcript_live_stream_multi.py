from multiprocessing import Process
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Function to start Selenium to scrape a video
def run_scraper(youtube_url):
    # Path to ChromeDriver
    driver_path = r'C:\Users\richa\Documents\chromedriver-win64\chromedriver.exe'
    service = Service(driver_path)

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service)

    # Open the YouTube video page
    driver.get(youtube_url)

    # Wait for the play button and click it
    try:
        play_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ytp-large-play-button.ytp-button"))
        )
        play_button.click()
    except TimeoutException:
        print("Play button not found or already playing.")

    # Loop to continuously retrieve captions
    retrieved_lines = set()
    try:
        while True:
            try:
                captions_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.ytp-caption-segment"))
                )
                with open(rf'C:\Users\richa\Desktop\YouTube Video\{youtube_url.split("=")[-1]}_captions_live.txt', 'a', encoding='utf-8') as f:
                    for caption in captions_elements:
                        if caption.text not in retrieved_lines:
                            f.write(caption.text + '\n')
                            retrieved_lines.add(caption.text)

                if captions_elements:
                    print(f"Latest Caption: {captions_elements[-1].text}")

            except TimeoutException:
                print("No captions found on the screen at the moment...")

            time.sleep(5)

    except KeyboardInterrupt:
        print("Stopping caption retrieval...")

    finally:
        driver.quit()

# List of YouTube video URLs to scrape
# Yahoo Finance : https://www.youtube.com/watch?v=OAHHA27td-A
# TraderTVLive : https://www.youtube.com/@TraderTVLive/streams
# Bloomberg Television : https://www.youtube.com/watch?v=iyOq8DhaMYw

youtube_urls = [
    "https://www.youtube.com/watch?v=OAHHA27td-A",
    "https://www.youtube.com/watch?v=oGBmEK_FwXQ",
    "https://www.youtube.com/watch?v=iyOq8DhaMYw"
]

# Create and start multiple processes
if __name__ == '__main__':
    processes = []
    for url in youtube_urls:
        p = Process(target=run_scraper, args=(url,))
        p.start()
        processes.append(p)

    # Wait for all processes to complete
    for p in processes:
        p.join()

#Using Multiprocessing in Python
#You can use Python’s multiprocessing module to run multiple Selenium instances concurrently from a single script.