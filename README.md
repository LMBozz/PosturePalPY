# PosturePal

**PosturePal** is a real-time posture monitoring application built with Python. It uses computer vision to track a user's posture and provides gentle, non-intrusive alerts when poor posture is detected for a sustained period.  

The goal of PosturePal is to help users maintain good posture without being disruptive, making it an ideal tool for office workers, students, or anyone who spends long hours sitting at a desk.

---

## Features
- **Real-Time Posture Tracking**: Uses OpenCV and MediaPipe to analyze posture in real-time.
- **Non-Intrusive Alerts**: Provides subtle reminders when posture needs adjusting.
- **User-Friendly Interface**: Simple GUI built with Tkinter for easy interaction.

---

## Installation
PosturePal requires Python and a few external libraries, which are listed in `requirements.txt`.

### Windows
1. Ensure you have Python installed: [Download Python](https://www.python.org/downloads/)
2. Open Command Prompt and run:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python postureChecker.py
   ```

### macOS
1. Install Python if not already installed.
2. Open Terminal and run:
   ```sh
   pip3 install -r requirements.txt
   ```
3. Start the application:
   ```sh
   python3 postureChecker.py
   ```

### Linux
1. Ensure Python and `venv` are installed.
2. Open Terminal and create a virtual environment:
   ```sh
   python3 -m venv env
   source env/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python postureChecker.py
   ```

---

## Dependencies
PosturePal relies on the following Python libraries:
- **OpenCV** – for computer vision processing
- **MediaPipe** – for pose detection
- **Tkinter** – for the graphical user interface

All required dependencies are listed in `requirements.txt`. Install them using the instructions in the **Installation** section.

---

## File Structure
```
PosturePal/
│-- postureChecker.py  # Main application file
│-- requirements.txt   # List of required Python libraries
│-- LICENSE.txt        # MIT License file
```

---

## Usage
Once installed, simply run `postureChecker.py`, and the program will begin monitoring your posture in real time. Adjust the settings as needed to customize alert timing and sensitivity.

---

## Contributions
Contributions are welcome! Feel free to submit issues or pull requests to improve PosturePal.

---

## License
PosturePal is open-source and available under the **MIT License**.

---

**Happy posture tracking!** 🧑‍💻✨
