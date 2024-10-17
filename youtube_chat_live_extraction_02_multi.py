from multiprocessing import Process
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import datetime
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException

# List of YouTube channels and their corresponding URLs, with an "enabled" flag to control processing
channels = [
    {"name": "Zendoo", "url": "https://www.youtube.com/watch?v=EU9fGLoRuUk", "enabled": True},
    {"name": "STOCKSROCKS", "url": "https://www.youtube.com/watch?v=gcazDew7NTM", "enabled": True},
    {"name": "PrecisionDayTrading", "url": "https://www.youtube.com/watch?v=3F7bUroOquQ", "enabled": False},
    {"name": "TheStockMarket", "url": "https://www.youtube.com/watch?v=6jBMIv98r9c", "enabled": False},
    {"name": "TraderTVLive", "url": "https://www.youtube.com/watch?v=3rnQh8PJz0Q", "enabled": False}
]

# Function to extract live chat from a YouTube video
def extract_chat(channel_name, youtube_url):
    driver_path = r'C:\Users\richa\Documents\chromedriver-win64\chromedriver.exe'
    service = Service(driver_path)

    driver = webdriver.Chrome(service=service)

    driver.get(youtube_url)
    time.sleep(5)

    try:
        driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe#chatframe"))
    except Exception as e:
        print(f"Error switching to iframe for channel '{channel_name}': {e}")
        driver.quit()
        return

    seen_messages = set()
    message_batch = []

    # Open file using the channel name provided
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    with open(rf'C:\Users\richa\Desktop\YouTube Chat\YouTubeChat_{channel_name}_{current_date}.txt', "a", encoding="utf-8") as f:
        while True:
            try:
                chat_messages = driver.find_elements(By.CSS_SELECTOR, "yt-live-chat-text-message-renderer")
                for message in chat_messages:
                    message_id = message.get_attribute("id")
                    if message_id not in seen_messages:
                        seen_messages.add(message_id)
                        author = message.find_element(By.CSS_SELECTOR, "#author-name").text
                        text = message.find_element(By.CSS_SELECTOR, "#message").text
                        timestamp = message.find_element(By.CSS_SELECTOR, "#timestamp").text
                        local_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        formatted_message = f'[{timestamp} | Local: {local_timestamp}] {author}: {text}'
                        message_batch.append(formatted_message)
                        print(f"{channel_name}: {formatted_message}")

            except StaleElementReferenceException:
                continue
            except WebDriverException as e:
                print(f"WebDriverException for channel '{channel_name}': {e}")
                time.sleep(5)

            if message_batch:
                f.write("\n".join(message_batch) + "\n")
                f.flush()
                message_batch.clear()

            time.sleep(10)

if __name__ == '__main__':
    processes = []
    for channel in channels:
        # Only start the extraction process if the channel is enabled
        if channel["enabled"]:
            p = Process(target=extract_chat, args=(channel["name"], channel["url"]))
            p.start()
            processes.append(p)

    for p in processes:
        p.join()
