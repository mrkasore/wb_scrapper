import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pynput import keyboard
from yt_dlp import YoutubeDL

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
driver = webdriver.Chrome(service=service, options=options)


def download_hls_video(m3u8_url):
    try:
        filename = os.path.join(DOWNLOAD_DIR, f"video_{int(time.time())}.mp4")

        ydl_opts = {
            'outtmpl': filename,
            'format': 'best',
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([m3u8_url])
        print(f"[✅] Видео скачано: {filename}")
    except Exception as e:
        print(f"[-] Ошибка при скачивании видео: {e}")

def enable_network_tracking(driver):
    driver.execute_cdp_cmd("Network.enable", {})

def wait_for_m3u8_url(driver, timeout=30):
    enable_network_tracking(driver)

    start_time = time.time()
    m3u8_url = None

    while time.time() - start_time < timeout:
        logs = driver.get_log("performance")

        for log in logs:
            message = log.get("message", "")
            if ".m3u8" in message:
                print(f"[+] Найден HLS-поток: {message}")
                message = json.loads(message)
                return message['message']['params']['request']['url']

        time.sleep(1)

    return None


def get_m3u8_url():
    try:
        print("[*] Ожидание загрузки видео...")
        m3u8_url = wait_for_m3u8_url(driver)
        if m3u8_url:
            download_hls_video(m3u8_url)
        else:
            print("[-] HLS-поток не найден или недоступен.")
    except Exception as e:
        print(f"[-] Ошибка поиска видео: {e}")


def on_press(key):
    if key == keyboard.Key.f4:
        print("[*] Запрос на скачивание видео...")
        get_m3u8_url()


url = "https://www.wildberries.ru/"
driver.get(url)
print("[*] Скрипт запущен. Нажмите F4 для скачивания видео.")

listener = keyboard.Listener(on_press=on_press)
listener.start()

try:
    listener.join()
except KeyboardInterrupt:
    print("[!] Остановка скрипта.")
finally:
    driver.quit()
