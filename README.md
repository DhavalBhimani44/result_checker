# Result Checker

An automated tool that periodically checks for exam results on the SIU exam portal.

## Features

- Automatically checks the SIU exam portal for result availability
- Plays an audio alert when results become available
- Runs in the background with minimal resource usage
- Logs all check attempts with timestamps

## Requirements

- Google Chrome browser
- ChromeDriver matching your Chrome version
- Python 3.6+ (if running from source)

## Setup Instructions

1. **Download the Application**

   - Download the latest release `.exe` file from the releases section
   - Or clone this repository to run from source

2. **ChromeDriver Setup**

   - Download ChromeDriver from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
   - Make sure the version matches your Chrome browser version
   - Place `chromedriver.exe` in your Windows directory (C:\Windows\) or update the path in the script

3. **Configuration**

   - Open `result_checker.py` in a text editor if running from source
   - Update your PRN and SEAT_NUMBER in the configuration section
   - Adjust CHECK_INTERVAL if needed (default is 10 minutes)

4. **Audio Alert**
   - Ensure `alert.mp3` is in the same directory as the executable or script
   - You can replace it with any mp3 file of your choice

## Running the Application

### From Executable

- Simply double-click the `result_checker.exe` file

### From Source

```
pip install selenium pygame
python result_checker.py
```

## Building from Source

To create your own executable:

```
pip install pyinstaller
python -m PyInstaller --onefile --windowed --add-data "alert.mp3;." result_checker.py
```

The executable will be created in the `dist` folder.

## Notes

- The application runs in headless mode (no visible browser window)
- All check activity is logged to `result_check_log.txt`
- Press Ctrl+C in the terminal to stop the script if running from source
