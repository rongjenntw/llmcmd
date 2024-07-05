from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import webbrowser
import time
import pyautogui
"""
all llm tools are here
"""
def get_current_weather(location="Tokyo", format="celsius"):
    print(f"current weather in {location} is 50 degree {format}")

def watch_youtube():
    # Set up the WebDriver (Chrome in this case)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    # Open YouTube
    driver.get("https://www.youtube.com")
    # Take a screenshot
    driver.save_screenshot("youtube_screenshot.png")
    # Close the browser
    driver.quit()

def open_browser():
    webbrowser.open("https://www.youtube.com")
    time.sleep(10)
    screenshot = pyautogui.screenshot()
    screenshot.save("youtube_screenshot.png")

if __name__ == "__main__":
    open_browser()
