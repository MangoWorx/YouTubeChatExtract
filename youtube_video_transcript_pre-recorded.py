from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Path to ChromeDriver
driver_path = r'C:\Users\richa\Documents\chromedriver-win64\chromedriver.exe'
service = Service(driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# Open the YouTube video page (replace with your video link)
driver.get('https://www.youtube.com/watch?v=eZdf71xmsCc')

# Wait for the page to load
time.sleep(5)

# Open transcript (if available)
try:
    # Click the 'More options' button (three vertical dots) below the video
    more_options_button = driver.find_element(By.XPATH, "//yt-icon-button[@id='button' and contains(@aria-label, 'More actions')]")
    more_options_button.click()
    time.sleep(2)

    # Click 'Open transcript' if it exists
    transcript_button = driver.find_element(By.XPATH, "//yt-formatted-string[contains(text(), 'Transcript')]")
    transcript_button.click()
    time.sleep(2)

    # Extract transcript lines
    transcript_lines = driver.find_elements(By.CSS_SELECTOR, "div.cue")

    # Save the transcript to a file
    with open(r'C:\Users\richa\Desktop\YouTube Video\youtube_transcript.txt', 'w', encoding='utf-8') as f:
        for line in transcript_lines:
            f.write(line.text + '\n')
    
    print("Transcript saved successfully.")

except Exception as e:
    print(f"Error retrieving the transcript: {e}")

# Close the browser
driver.quit()
