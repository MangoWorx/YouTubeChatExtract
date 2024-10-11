from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Specify the path to the ChromeDriver
driver_path = r'C:\Users\richa\Documents\chromedriver-win64\chromedriver.exe'
service = Service(driver_path)

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=service)

# Open the YouTube video
driver.get('https://www.youtube.com/watch?v=eniUNJTWrJw')

# Wait for the chat to load (adjust time as needed)
driver.implicitly_wait(10)

# Extract messages
chat_messages = driver.find_elements(By.CSS_SELECTOR, "yt-live-chat-text-message-renderer")

for message in chat_messages:
    author = message.find_element(By.CSS_SELECTOR, "#author-name").text
    text = message.find_element(By.CSS_SELECTOR, "#message").text
    print(f'{author}: {text}')

# Close the driver
driver.quit()
