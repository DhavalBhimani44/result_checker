from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pygame
from datetime import datetime
import time
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# --- Configuration ---
URL = "https://siuexam.siu.edu.in/forms/resultview.html"
PRN = "22070122051"
SEAT_NUMBER = "523538"
CHECK_INTERVAL = 30  # in seconds
LOG_FILE = "result_check_log.txt"
ALERT_SOUND = "alert.mp3"
CHROME_DRIVER = r"C:\Windows\chromedriver.exe"

# --- Initialize Sound ---
pygame.mixer.init()

# --- Tkinter GUI Setup ---
root = tk.Tk()
root.title("SIU Result Checker")
root.geometry("500x300")
root.resizable(False, False)

status_label = tk.Label(root, text="Status: Waiting to start...", fg="blue", font=("Arial", 11))
status_label.pack(pady=5)

log_box = ScrolledText(root, width=65, height=12, font=("Courier", 9), state="disabled")
log_box.pack(padx=10, pady=5)

quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.pack(pady=5)

# --- Logger ---
def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {message}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    
    log_box.configure(state="normal")
    log_box.insert(tk.END, line + "\n")
    log_box.see(tk.END)
    log_box.configure(state="disabled")
    print(line)

# --- Main Result Check Function ---
def check_result():
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")

        driver = webdriver.Chrome(options=options)
        driver.get(URL)
        time.sleep(2)

        log("Loaded result page.")

        try:
            season_dropdown = driver.find_element(By.NAME, "grp")
            Select(season_dropdown).select_by_visible_text("EVEN 2025")
            log("Selected exam season.")
        except:
            log("Exam season dropdown not found or already selected.")

        prn_field = driver.find_element(By.ID, "login")
        prn_field.clear()
        prn_field.send_keys(PRN)
        log("Entered PRN.")

        login_btn = driver.find_element(By.ID, "lgnbtn")
        login_btn.click()
        log("Clicked login button.")
        time.sleep(3)

        page = driver.page_source

        if "Enter Seat Number of Sem 6" in page or "txt8" in page:
            log("Seat number entry detected.")

            seat_input = driver.find_element(By.ID, "txt8")
            seat_input.clear()
            seat_input.send_keys(SEAT_NUMBER)
            log(f"Entered seat number: {SEAT_NUMBER}")

            view_btn = driver.find_element(By.XPATH, "//input[@type='button' and @value='View']")
            view_btn.click()
            log("Clicked 'View' button after seat number entry.")

            pygame.mixer.music.load(ALERT_SOUND)
            for i in range(3):
                log(f"🔊 Playing alert sound ({i+1}/3)...")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(1)
                time.sleep(0.5)

        elif "Semester - 6 Result not yet declared" in page:
            log("Semester - 6 Result not yet declared.")
        else:
            log("⚠️ Unexpected page content. Manual check advised.")

    except Exception as e:
        log(f"❌ Error: {str(e)}")
    finally:
        try:
            driver.quit()
        except:
            pass

# --- Continuous Loop Thread ---
def start_checker():
    status_label.config(text="Status: Running...", fg="green")
    while True:
        check_result()
        time.sleep(CHECK_INTERVAL)

# --- Launch Threaded Loop ---
threading.Thread(target=start_checker, daemon=True).start()

# --- Run the Tkinter Loop ---
root.mainloop()
