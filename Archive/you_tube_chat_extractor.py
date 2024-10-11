from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Path to ChromeDriver
driver_path = r'C:\Users\richa\Documents\chromedriver-win64\chromedriver.exe'
service = Service(driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# Open the YouTube video with chat
driver.get('https://www.youtube.com/watch?v=q2L8XScdJUs')

# Wait for the page to load
time.sleep(5)

# Switch to the live chat iframe
driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe#chatframe"))

# Scroll through the chat to load all messages
last_height = driver.execute_script("return document.documentElement.scrollHeight")
while True:
    # Scroll down inside the chat iframe
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)  # Wait for new messages to load
    
    # Calculate new scroll height and compare with last height
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break  # Break if no new messages loaded
    last_height = new_height

# Extract messages
chat_messages = driver.find_elements(By.CSS_SELECTOR, "yt-live-chat-text-message-renderer")

# Create a file to store the chat messages
with open(r'C:\Users\richa\Desktop\YouTube Chat\youtube_zendoo_chat.txt', "w", encoding="utf-8") as f:
    for message in chat_messages:
        author = message.find_element(By.CSS_SELECTOR, "#author-name").text
        text = message.find_element(By.CSS_SELECTOR, "#message").text
        f.write(f'{author}: {text}\n')

# Close the browser
driver.quit()

print(r'C:\Users\richa\Desktop\YouTube Chat\youtube_zendoo_chat.txt')
