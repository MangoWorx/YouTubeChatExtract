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
driver.get('https://www.youtube.com/watch?v=bDGH2m3DYog')

# Wait for the page to load
time.sleep(5)

# Open transcript (if available)
try:
    # Log current state
    print("Looking for 'More options' button...")

    # Use a broader CSS selector for the 'More options' button (three dots) near the video title
    more_options_button = driver.find_element(By.XPATH, "//button[@aria-label='More actions']")
    more_options_button.click()
    print("More options button clicked.")
    time.sleep(2)

    # Log state after clicking 'More actions'
    print("Looking for 'Transcript' option...")

    # Click 'Open transcript'
    transcript_button = driver.find_element(By.XPATH, "//yt-formatted-string[text()='Open transcript']")
    transcript_button.click()
    print("Transcript opened.")
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
