from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import datetime
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException

# Path to ChromeDriver
driver_path = r'C:\Users\richa\Documents\chromedriver-win64\chromedriver.exe'
service = Service(driver_path)

# Number of messages to process before saving to file
batch_size = 10

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# Open the YouTube video with chat
driver.get('https://www.youtube.com/watch?v=HPxifkx1Mmo') 

# Wait for the page to load
time.sleep(5)

# Try switching to the live chat iframe
try:
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe#chatframe"))
    print("Switched to chat iframe successfully")
except Exception as e:
    print(f"Error switching to iframe: {e}")
    driver.quit()
    exit()

# Keep track of seen messages to avoid duplicates
seen_messages = set()

# Initialize a batch to store messages
message_batch = []

# Continuously check for new messages and append them to the file in batches
with open(r'C:\Users\richa\Desktop\YouTube Chat\youtube_zendoo_chat.txt', "a", encoding="utf-8") as f:
    while True:
        try:
            # Scroll through the chat to load new messages
            try:
                last_height = driver.execute_script("return document.documentElement.scrollHeight")
                while True:
                    try:
                        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                        time.sleep(2)  # Wait for new messages to load

                        # Calculate new scroll height and compare with last height
                        new_height = driver.execute_script("return document.documentElement.scrollHeight")
                        if new_height == last_height:
                            break  # Break if no new messages loaded
                        last_height = new_height
                    except WebDriverException as e:
                        print(f"WebDriverException encountered while scrolling: {e}")
                        break
            except WebDriverException as e:
                print(f"WebDriverException encountered during initial scroll handling: {e}")


            # Extract chat messages
            try:
                chat_messages = driver.find_elements(By.CSS_SELECTOR, "yt-live-chat-text-message-renderer")

                for message in chat_messages:
                    try:
                        message_id = message.get_attribute("id")
                        if message_id not in seen_messages:
                            seen_messages.add(message_id)

                            # Extract message details
                            author = message.find_element(By.CSS_SELECTOR, "#author-name").text
                            text = message.find_element(By.CSS_SELECTOR, "#message").text
                            timestamp = message.find_element(By.CSS_SELECTOR, "#timestamp").text

                            # Add a local timestamp down to milliseconds
                            local_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                            # Format the message
                            formatted_message = f'[{timestamp} | Local: {local_timestamp}] {author}: {text}'

                            # Append to the message batch
                            message_batch.append(formatted_message)

                            # Print to console
                            print(formatted_message)

                    except StaleElementReferenceException:
                        print("StaleElementReferenceException encountered, skipping message.")
                    except WebDriverException as e:
                        print(f"WebDriverException encountered while processing message: {e}")

            except StaleElementReferenceException:
                print("StaleElementReferenceException encountered while processing messages, retrying...")
            except WebDriverException as e:
                print(f"WebDriverException encountered while extracting messages: {e}")
                
        except WebDriverException as e:
            print(f"WebDriverException encountered in main loop: {e}")
            time.sleep(5)  # Wait for a few seconds before retrying in case of a temporary disconnect
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(5)  # Optionally wait before retrying to prevent rapid errors
        
        # If there's any leftover in the batch, write it before waiting again
        if message_batch:
            f.write("\n".join(message_batch) + "\n")
            f.flush()
            message_batch.clear()

        # Wait before checking for new messages again
        time.sleep(10)  # Adjust time as needed for how often you want to check for new messages

# Note: To stop the script, manually interrupt the process (Ctrl + C).
