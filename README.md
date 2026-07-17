# Python_04_01_Project_PythonGameDevelopment
# ✈️ Geo-Aware Flight Trivia

A dynamic, route-based desktop trivia game built in Python. Designed to keep passengers engaged during their journey, this application tests your knowledge of your destination country while tracking your historical performance over time.

## ✨ Features
* **Dynamic Route Selection:** Questions are specifically tailored to the user's selected destination country (Currently supporting routes to the UK, Brazil, Nigeria, and Mexico). More countries and questions can easily be added in the dictionary.
* **Smart Difficulty Scaling:** Players can choose between Easy and Hard modes. Domestic flights (same origin and destination country selected) automatically lock the player into Hard mode.
* **Robust Input Handling:** To satisfy the requirement of handling unexpected or non-numeric inputs, this application completely bypasses the terminal. By strictly utilizing a Graphical User Interface (GUI) with dropdown menus for route selection and clickable buttons for trivia answers, the game mathematically prevents invalid user typing and guarantees a crash-free experience.
* **Persistent Statistics (Global Counters):** The game tracks performance using a series of global counters managed by the `StatsRepository` class. These counters automatically save locally to a `game_stats.json` file, safely tracking lifetime sessions played, win/loss ratios, average completion times, and country-specific accuracy without requiring a database.
* **Live Countdown Timer:** Each question features a live timer that automatically triggers a timeout penalty if the player takes too long.

## 🛠️ Prerequisites
This game is built entirely using Python's Standard Library. **No external dependencies or third-party installations are required.** 

* **Python 3.7 or higher** (Required for type hinting and `pathlib`).
* **Tkinter** (Usually comes pre-installed with standard Python distributions).

## 🏗️ Code Structure
The application adheres to strict Object-Oriented Programming (OOP) and DRY (Don't Repeat Yourself) principles:

* **`StatsRepository`**: A data-layer class dedicated entirely to reading, validating, and writing to the `game_stats.json` file.
* **`GameSession`**: A logic-layer class that encapsulates the rules of a single quiz round, managing the active question index, score counters, and win conditions.
* **`TriviaGame`**: The presentation-layer class that acts as the UI Manager, handling the tkinter window loops, widget rendering, and dynamic screen clearing.

## 🚀 How to Run the Game
1. Clone or download this repository to your local machine.
2. Open your terminal or command prompt.
3. Navigate to the folder containing the game files.
4. Run the following command:
   ```bash
   python game.py
   
## 🎮 How to Play
1. Set Your Route: On the welcome screen, use the dropdown menus to select your 'Country of Origin' and your 'Destination Country'.

2. Select Difficulty: Click 'Continue' to choose your difficulty level. (Easy mode gives you 20 seconds per question; Hard mode gives you 12 seconds).

3. Answer the Trivia: You will be asked 5 multiple-choice questions about your destination. Click the button corresponding to your answer before the timer hits zero!

4. Check Your Stats: To win a session, you must get at least 4 out of 5 questions correct. At the end of the round, a summary screen will display your score, your speed, and your lifetime historical statistics.

5. Review History: You can view your overall lifetime performance across all flights at any time by clicking "Menu" on the start screen.
