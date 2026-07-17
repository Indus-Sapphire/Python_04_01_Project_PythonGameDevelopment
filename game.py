"""
Geo-Aware Flight Trivia Game using tkinter.

This script runs a desktop trivia game that dynamically selects questions 
based on the user's chosen flight destination. It tracks session statistics 
and saves them to a local JSON file for long-term storage.
"""

from __future__ import annotations 

# json is used to read and write statistics to a local text file.
import json
# random is used to shuffle and pick questions so the game isn't identical every time.
import random
# time is used to track exactly how many seconds a player takes to answer.
import time
# tkinter is the standard Python library used to build graphical user interfaces (windows, buttons, etc.).
import tkinter as tk
# Path helps to find exactly where this Python file is saved on the computer.
from pathlib import Path
# messagebox enables pop up errors or information alerts to the user.
from tkinter import messagebox

# --- CONSTANTS (Paint Palette) ---
# Defined HEX colours here for enabling their easy reuse throughout the code.
NAVY =  "#01295C"
WHITE = "#FFFFFF"
RED =   "#EB2226"
LIGHT_BG =  "#F3F5F8"

# This finds the folder where game.py is located and creates a file named "game_stats.json" there.
STATS_FILE_PATH = Path(__file__).with_name("game_stats.json")

# --- QUESTION BANK ---
# A dictionary holding all questions, separated by Country, then by Difficulty.
QUESTION_BANK = {
    "Brazil": {
        "Easy": [
            {
                "question": "What is the capital city of Brazil?",
                "options": ["Sao Paulo", "Brasilia", "Rio de Janeiro", "Salvador"],
                "answer": "Brasilia",
            },
            {
                "question": "Which famous rainforest is mostly in Brazil?",
                "options": ["Congo Rainforest", "Daintree Rainforest", "Amazon Rainforest", "Black Forest"],
                "answer": "Amazon Rainforest",
            },
            {
                "question": "What language is primarily spoken in Brazil?",
                "options": ["Spanish", "Portuguese", "French", "English"],
                "answer": "Portuguese",
            },
            {
                "question": "Which sport is most associated with Brazil?",
                "options": ["Cricket", "Rugby", "Ice Hockey", "Football (Soccer)"],
                "answer": "Football (Soccer)",
            },
            {
                "question": "Which city hosts the Christ the Redeemer statue?",
                "options": ["Fortaleza", "Belo Horizonte", "Rio de Janeiro", "Manaus"],
                "answer": "Rio de Janeiro",
            },
            {
                "question": "Which celebration is world-famous in Rio?",
                "options": ["Carnival", "Oktoberfest", "Day of the Dead", "Diwali"],
                "answer": "Carnival",
            },
        ],
        "Hard": [
            {
                "question": "What is the name of the vast wetland in western Brazil?",
                "options": ["Pampas", "Pantanal", "Atacama", "Altiplano"],
                "answer": "Pantanal",
            },
            {
                "question": "Which architect co-designed many buildings in Brasilia?",
                "options": ["Oscar Niemeyer", "Antoni Gaudi", "I. M. Pei", "Le Corbusier"],
                "answer": "Oscar Niemeyer",
            },
            {
                "question": "What is Brazil's highest mountain?",
                "options": ["Pico da Bandeira", "Pico da Neblina", "Mount Roraima", "Pico das Agulhas Negras"],
                "answer": "Pico da Neblina",
            },
            {
                "question": "In which year did Brazil move its capital to Brasilia?",
                "options": ["1945", "1960", "1972", "1988"],
                "answer": "1960",
            },
            {
                "question": "Which ocean current strongly affects Brazil's southeast coast?",
                "options": ["Benguela Current", "Brazil Current", "Canary Current", "California Current"],
                "answer": "Brazil Current",
            },
            {
                "question": "What is the traditional mixed martial art and dance with Afro-Brazilian roots?",
                "options": ["Samba", "Capoeira", "Forro", "Bossa Nova"],
                "answer": "Capoeira",
            },
        ],
    },
    "Nigeria": {
        "Easy": [
            {
                "question": "What is the capital city of Nigeria?",
                "options": ["Lagos", "Kano", "Abuja", "Port Harcourt"],
                "answer": "Abuja",
            },
            {
                "question": "Which body of water lies to Nigeria's south?",
                "options": ["Mediterranean Sea", "Arabian Sea", "Gulf of Guinea", "Red Sea"],
                "answer": "Gulf of Guinea",
            },
            {
                "question": "Which Nigerian city is the country's largest by population?",
                "options": ["Abuja", "Lagos", "Ibadan", "Enugu"],
                "answer": "Lagos",
            },
            {
                "question": "What is Nigeria's official language?",
                "options": ["English", "Hausa", "Yoruba", "Igbo"],
                "answer": "English",
            },
            {
                "question": "Nigeria is located on which continent?",
                "options": ["Asia", "Africa", "Europe", "South America"],
                "answer": "Africa",
            },
            {
                "question": "Which movie industry nickname refers to Nigeria?",
                "options": ["Nollywood", "Mollywood", "Goldwood", "Afriwood"],
                "answer": "Nollywood",
            },
        ],
        "Hard": [
            {
                "question": "What major river joins the Niger River at Lokoja?",
                "options": ["Benue River", "Congo River", "Senegal River", "Volta River"],
                "answer": "Benue River",
            },
            {
                "question": "In what year did Nigeria gain independence?",
                "options": ["1957", "1960", "1963", "1975"],
                "answer": "1960",
            },
            {
                "question": "Which ancient Nigerian civilization is known for bronze and terracotta art?",
                "options": ["Nok", "Aksum", "Mali", "Songhai"],
                "answer": "Nok",
            },
            {
                "question": "Which city is historically linked to the Yoruba Oyo Empire?",
                "options": ["Sokoto", "Oyo", "Calabar", "Jos"],
                "answer": "Oyo",
            },
            {
                "question": "What is the name of the traditional ruler of Kano?",
                "options": ["Oba", "Eze", "Emir", "Lamido"],
                "answer": "Emir",
            },
            {
                "question": "Which plateau city in Nigeria is known for its cooler climate?",
                "options": ["Jos", "Warri", "Aba", "Onitsha"],
                "answer": "Jos",
            },
        ],
    },
    "UK": {
        "Easy": [
            {
                "question": "What is the capital city of the UK?",
                "options": ["Manchester", "Cardiff", "London", "Birmingham"],
                "answer": "London",
            },
            {
                "question": "Which river flows through London?",
                "options": ["Severn", "Thames", "Tyne", "Mersey"],
                "answer": "Thames",
            },
            {
                "question": "What is the currency used in the UK?",
                "options": ["Euro", "Dollar", "Pound Sterling", "Franc"],
                "answer": "Pound Sterling",
            },
            {
                "question": "Which famous clock tower is in London?",
                "options": ["Big Ben", "Eiffel Tower", "Clock of Dublin", "Tower of Pisa"],
                "answer": "Big Ben",
            },
            {
                "question": "Which sport is strongly associated with Wimbledon?",
                "options": ["Cricket", "Rugby", "Tennis", "Golf"],
                "answer": "Tennis",
            },
            {
                "question": "Which country is NOT part of the UK?",
                "options": ["Scotland", "Wales", "Ireland", "England"],
                "answer": "Ireland",
            },
        ],
        "Hard": [
            {
                "question": "What is the name of the prehistoric monument in Wiltshire?",
                "options": ["Avebury", "Stonehenge", "Hadrian's Wall", "Skara Brae"],
                "answer": "Stonehenge",
            },
            {
                "question": "Which document signed in 1215 limited royal power in England?",
                "options": ["Bill of Rights", "Magna Carta", "Act of Union", "Domesday Book"],
                "answer": "Magna Carta",
            },
            {
                "question": "What is the highest mountain in the UK?",
                "options": ["Scafell Pike", "Snowdon", "Ben Nevis", "Cairn Gorm"],
                "answer": "Ben Nevis",
            },
            {
                "question": "Which UK city is known as the 'Granite City'?",
                "options": ["Aberdeen", "Glasgow", "Leeds", "York"],
                "answer": "Aberdeen",
            },
            {
                "question": "Which battle in 1066 led to Norman rule in England?",
                "options": ["Battle of Bosworth", "Battle of Hastings", "Battle of Agincourt", "Battle of Bannockburn"],
                "answer": "Battle of Hastings",
            },
            {
                "question": "What is the name of the shortest commercial flight route in the UK?",
                "options": ["Belfast to Glasgow", "Westray to Papa Westray", "London to Manchester", "Edinburgh to Inverness"],
                "answer": "Westray to Papa Westray",
            },
        ],
    },
    "Mexico": {
        "Easy": [
            {
                "question": "What is the capital city of Mexico?",
                "options": ["Guadalajara", "Monterrey", "Mexico City", "Puebla"],
                "answer": "Mexico City",
            },
            {
                "question": "What is the currency of Mexico?",
                "options": ["Peso", "Real", "Dollar", "Quetzal"],
                "answer": "Peso",
            },
            {
                "question": "Which ancient civilization built Chichen Itza?",
                "options": ["Maya", "Aztec", "Inca", "Olmec"],
                "answer": "Maya",
            },
            {
                "question": "Which ocean borders Mexico's west coast?",
                "options": ["Atlantic Ocean", "Pacific Ocean", "Indian Ocean", "Arctic Ocean"],
                "answer": "Pacific Ocean",
            },
            {
                "question": "Which holiday honours deceased loved ones in Mexico?",
                "options": ["Cinco de Mayo", "Day of the Dead", "Easter", "Independence Day"],
                "answer": "Day of the Dead",
            },
            {
                "question": "Mexico shares its northern border with which country?",
                "options": ["Guatemala", "Belize", "United States", "Canada"],
                "answer": "United States",
            },
        ],
        "Hard": [
            {
                "question": "What is Mexico's highest peak?",
                "options": ["Popocatepetl", "Pico de Orizaba", "Nevado de Toluca", "Iztaccihuatl"],
                "answer": "Pico de Orizaba",
            },
            {
                "question": "Which peninsula in southeast Mexico is known for cenotes?",
                "options": ["Baja California", "Yucatan Peninsula", "Sonora Peninsula", "Isthmus of Tehuantepec"],
                "answer": "Yucatan Peninsula",
            },
            {
                "question": "In which year did Mexico gain independence from Spain?",
                "options": ["1810", "1821", "1836", "1848"],
                "answer": "1821",
            },
            {
                "question": "What is the name of the large square in central Mexico City?",
                "options": ["El Malecon", "Zocalo", "Plaza Nueva", "La Alameda"],
                "answer": "Zocalo",
            },
            {
                "question": "Which Mexican state is famous for the monarch butterfly biosphere reserve?",
                "options": ["Michoacan", "Jalisco", "Chiapas", "Tabasco"],
                "answer": "Michoacan",
            },
            {
                "question": "Which pre-Hispanic city is known for the Pyramid of the Sun?",
                "options": ["Teotihuacan", "Tulum", "Palenque", "Uxmal"],
                "answer": "Teotihuacan",
            },
        ],
    },
}

def create_default_global_stats() -> dict:
    """
    Generate a fresh, empty dictionary for tracking game statistics.

    Returns:
        dict: A dictionary containing default values (0 or empty) for wins, 
              losses, times, and country-specific performance.
    """
    return {
        "sessions_played": 0,
        "wins": 0,
        "losses": 0,
        # Comprehensions are used here to automatically create a key for every country in QUESTION_BANK
        "correct_by_country": {country: 0 for country in QUESTION_BANK},
        "incorrect_by_country": {country: 0 for country in QUESTION_BANK},
        "elapsed_times": [],
        "quickest_answer_time": None,
    }


# GLOBAL_STATS acts as the master scoreboard for the entire programme.
GLOBAL_STATS = create_default_global_stats()

class StatsRepository:
    """
    Handles persistence and validation of game statistics.
    Responsible for loading from and saving to the JSON file.
    """

    def __init__(self, stats_file_path: Path) -> None:
        """
        Initialize the repository with a file path.

        Args:
            stats_file_path (Path): Path to the JSON statistics file.
        """
        self.stats_file_path = stats_file_path

    def _non_negative_int(self, value: object) -> int:
        """
        Validate that a given value is a non-negative integer.

        Args:
            value (object): The value to check (usually read from JSON).

        Returns:
            int: The safely validated non-negative integer.

        Raises:
            ValueError: If the value is invalid.
        """
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("Expected a non-negative integer.")
        return value

    def _non_negative_float(self, value: object) -> float:
        """
        Validate that a given value is a non-negative float.

        Args:
            value (object): The time value to check.

        Returns:
            float: The safely validated non-negative float.

        Raises:
            ValueError: If the value is invalid.
        """
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Expected a non-negative number.")
        return float(value)

    def load(self) -> dict:
        """
        Attempt to load statistics from the JSON file.
        If the file doesn't exist or is corrupted, returns default statistics.

        Returns:
            dict: The loaded and validated statistics dictionary.
        """
        default_stats = create_default_global_stats()

        if not self.stats_file_path.exists():
            return default_stats

        try:
            stats_data = json.loads(self.stats_file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            messagebox.showerror(
                "Statistics File Error",
                f"Could not read historical statistics. Defaults will be used.\n{exc}",
            )
            return default_stats

        try:
            loaded_stats = create_default_global_stats()
            loaded_stats["sessions_played"] = self._non_negative_int(stats_data.get("sessions_played", 0))
            loaded_stats["wins"] = self._non_negative_int(stats_data.get("wins", 0))
            loaded_stats["losses"] = self._non_negative_int(stats_data.get("losses", 0))

            correct_by_country = stats_data.get("correct_by_country", {})
            if not isinstance(correct_by_country, dict):
                raise ValueError("correct_by_country must be an object.")
            for country in QUESTION_BANK:
                loaded_stats["correct_by_country"][country] = self._non_negative_int(
                    correct_by_country.get(country, 0)
                )

            incorrect_by_country = stats_data.get("incorrect_by_country", {})
            if not isinstance(incorrect_by_country, dict):
                raise ValueError("incorrect_by_country must be an object.")
            for country in QUESTION_BANK:
                loaded_stats["incorrect_by_country"][country] = self._non_negative_int(
                    incorrect_by_country.get(country, 0)
                )

            elapsed_times = stats_data.get("elapsed_times", [])
            if not isinstance(elapsed_times, list):
                raise ValueError("elapsed_times must be a list.")
            loaded_stats["elapsed_times"] = [self._non_negative_float(value) for value in elapsed_times]

            quickest_answer_time = stats_data.get("quickest_answer_time")
            if quickest_answer_time is None:
                loaded_stats["quickest_answer_time"] = None
            else:
                loaded_stats["quickest_answer_time"] = self._non_negative_float(quickest_answer_time)

            return loaded_stats

        except ValueError as exc:
            messagebox.showerror(
                "Statistics Data Error",
                f"Statistics file data is invalid. Defaults will be used.\n{exc}",
            )
            return default_stats

    def save(self, stats: dict) -> None:
        """
        Save statistics to the JSON file.

        Args:
            stats (dict): The statistics dictionary to persist.
        """
        try:
            self.stats_file_path.write_text(
                json.dumps(stats, indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            messagebox.showerror(
                "Statistics File Error",
                f"Could not save historical statistics.\n{exc}",
            )


class GameSession:
    """
    Encapsulates the state of a single game session (per-round state).
    Tracks questions, answers, timing, and score for the current game.
    """

    def __init__(self, questions: list, difficulty: str, total_questions: int, timer_by_mode: dict) -> None:
        """
        Initialize a game session with questions and settings.

        Args:
            questions (list): List of question dictionaries for this session.
            difficulty (str): The difficulty level ("Easy" or "Hard").
            total_questions (int): Total number of questions in this session.
            timer_by_mode (dict): Mapping of difficulty levels to timer durations.
        """
        self.questions = questions
        self.difficulty = difficulty
        self.total_questions = total_questions
        self.timer_by_mode = timer_by_mode

        # Live game state
        self.current_index = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.session_started_at = time.time()
        self.question_started_at = 0.0
        self.answer_times: list = []
        self.remaining_seconds = 0
        self.awaiting_next = False

    def start(self) -> None:
        """Reset per-round state and start timing the session."""
        self.current_index = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.session_started_at = time.time()
        self.question_started_at = 0.0
        self.answer_times = []
        self.remaining_seconds = 0
        self.awaiting_next = False

    def is_finished(self) -> bool:
        """Check if all questions have been answered."""
        return self.current_index >= len(self.questions)

    def get_current_question(self) -> dict:
        """Get the current question data."""
        if self.is_finished():
            return {}
        return self.questions[self.current_index]

    def record_answer(self, answer_duration: float, is_correct: bool) -> None:
        """
        Record an answer and update counters.

        Args:
            answer_duration (float): Time taken to answer this question.
            is_correct (bool): Whether the answer was correct.
        """
        self.answer_times.append(answer_duration)
        if is_correct:
            self.correct_answers += 1
        else:
            self.incorrect_answers += 1

    def move_to_next(self) -> None:
        """Move to the next question."""
        self.current_index += 1

    def get_session_elapsed(self) -> float:
        """Get total elapsed time for this session."""
        return time.time() - self.session_started_at

    def get_current_timer_seconds(self) -> int:
        """Get the timer duration for the current difficulty."""
        return self.timer_by_mode[self.difficulty]

    def calculate_win_status(self) -> bool:
        """Determine if the player won based on their score."""
        wins_required = (len(self.questions) * 3 + 4) // 5
        return self.correct_answers >= wins_required

    def get_fastest_answer(self) -> float | None:
        """Get the fastest answer time in this session, or None if no answers."""
        return min(self.answer_times) if self.answer_times else None

class TriviaGame:
    """
    The main blueprint (Class) that coordinates the trivia game.
    
    This class handles the creation of the graphical window, the flow of the 
    screens (menus to game to results), and tracks the live score during a session.
    """

    def __init__(self) -> None:
        """
        Initialise the game, setup the main window, and load historical data.
        This block runs automatically the moment TriviaGame() is called.
        """
        # tk.Tk() creates the main application window (the physical game board).
        self.root = tk.Tk()
        self.root.title("Geo-Aware Flight Trivia")
        self.root.geometry("980x640")
        self.root.configure(bg=LIGHT_BG)

        # We create a single 'main_frame' acting like a canvas. Instead of opening
        # new windows, we will just erase and redraw on this single frame.
        self.main_frame = tk.Frame(self.root, bg=LIGHT_BG, padx=30, pady=30)
        self.main_frame.pack(fill="both", expand=True)

        # Extract just the country names from our QUESTION_BANK for the dropdowns.
        self.country_options = list(QUESTION_BANK.keys())
        default_origin = self.country_options[0]
        default_destination = (
            self.country_options[1]
            if len(self.country_options) > 1
            else self.country_options[0]
        )
        
        # tk.StringVar() is a special tkinter variable that allows the dropdown 
        # menus to automatically update the program when the user makes a choice.
        self.origin_var = tk.StringVar(value=default_origin)
        self.destination_var = tk.StringVar(value=default_destination)
        
        # Define placeholder variables that will track the active game's state
        self.difficulty = ""
        self.session: GameSession | None = None
        self.active_timer_job = None

        # Game balancing settings
        self.total_questions = 5
        self.timer_by_mode = {"Easy": 20, "Hard": 12}

        # Font styles stored here so they are consistent across all screens
        self.title_font = ("Helvetica", 28, "bold")
        self.header_font = ("Helvetica", 18, "bold")
        self.body_font = ("Helvetica", 13)
        self.button_font = ("Helvetica", 12, "bold")

        # Load history and immediately save it to ensure the JSON file exists
        self.load_historical_statistics()
        self.save_historical_statistics()
        
        # Launch the first screen for the user
        self.show_welcome_screen()

    def _apply_global_statistics(self, stats: dict) -> None:
        """
        Overwrite the current global statistics with a new dictionary.

        Args:
            stats (dict): The new statistics dictionary to apply.
        """
        GLOBAL_STATS.clear()
        GLOBAL_STATS.update(stats)

    def _non_negative_int(self, value: object) -> int:
        """
        Validate that a given value is a non-negative integer. Used for error handling.

        Args:
            value (object): The value to check (usually read from the JSON file).

        Returns:
            int: The safely validated non-negative integer.

        Raises:
            ValueError: If the value is a boolean, string, or less than zero.
        """
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("Expected a non-negative integer.")
        return value

    def _non_negative_float(self, value: object) -> float:
        """
        Validate that a given value is a non-negative float (decimal). Used for timings.

        Args:
            value (object): The time value to check.

        Returns:
            float: The safely validated non-negative float.

        Raises:
            ValueError: If the value is invalid or less than zero.
        """
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Expected a non-negative number.")
        return float(value)

    def load_historical_statistics(self) -> None:
        """
        Attempt to read the game_stats.json file. If it fails or the data is 
        corrupted, it safely falls back to default zeroed statistics.
        """
        default_stats = create_default_global_stats()
        
        # If the file doesn't exist yet (e.g. very first time playing), use defaults
        if not STATS_FILE_PATH.exists():
            self._apply_global_statistics(default_stats)
            return

        # Attempt to read the file using a try/except block to prevent crashes
        try:
            stats_data = json.loads(STATS_FILE_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            messagebox.showerror(
                "Statistics File Error",
                f"Could not read historical statistics. Defaults will be used.\n{exc}",
            )
            self._apply_global_statistics(default_stats)
            return

        # Validate every piece of data pulled from the JSON to ensure it hasn't been tampered with
        try:
            loaded_stats = create_default_global_stats()
            loaded_stats["sessions_played"] = self._non_negative_int(stats_data.get("sessions_played", 0))
            loaded_stats["wins"] = self._non_negative_int(stats_data.get("wins", 0))
            loaded_stats["losses"] = self._non_negative_int(stats_data.get("losses", 0))

            correct_by_country = stats_data.get("correct_by_country", {})
            if not isinstance(correct_by_country, dict):
                raise ValueError("correct_by_country must be an object.")
            for country in QUESTION_BANK:
                loaded_stats["correct_by_country"][country] = self._non_negative_int(correct_by_country.get(country, 0))

            incorrect_by_country = stats_data.get("incorrect_by_country", {})
            if not isinstance(incorrect_by_country, dict):
                raise ValueError("incorrect_by_country must be an object.")
            for country in QUESTION_BANK:
                loaded_stats["incorrect_by_country"][country] = self._non_negative_int(incorrect_by_country.get(country, 0))

            elapsed_times = stats_data.get("elapsed_times", [])
            if not isinstance(elapsed_times, list):
                raise ValueError("elapsed_times must be a list.")
            loaded_stats["elapsed_times"] = [self._non_negative_float(value) for value in elapsed_times]

            quickest_answer_time = stats_data.get("quickest_answer_time")
            if quickest_answer_time is None:
                loaded_stats["quickest_answer_time"] = None
            else:
                loaded_stats["quickest_answer_time"] = self._non_negative_float(quickest_answer_time)
                
        except ValueError as exc:
            messagebox.showerror(
                "Statistics Data Error",
                f"Statistics file data is invalid. Defaults will be used.\n{exc}",
            )
            self._apply_global_statistics(default_stats)
            return

        self._apply_global_statistics(loaded_stats)

    def save_historical_statistics(self) -> None:
        """Write the current GLOBAL_STATS dictionary into the JSON file."""
        try:
            STATS_FILE_PATH.write_text(
                json.dumps(GLOBAL_STATS, indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            messagebox.showerror(
                "Statistics File Error",
                f"Could not save historical statistics.\n{exc}",
            )

    def clear_screen(self) -> None:
        """
        Erase all buttons, labels, and text from the main frame. 
        Also cancels any active countdown timers to prevent background glitches.
        """
        if self.active_timer_job is not None:
            self.root.after_cancel(self.active_timer_job)
            self.active_timer_job = None

        # Loop through every widget on the screen and destroy it
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_welcome_screen(self) -> None:
        """Render the main menu where users select their flight route."""
        self.clear_screen()

        # .pack() is a geometry manager in tkinter that stacks items vertically
        title_label = tk.Label(
            self.main_frame,
            text="Geo-Aware Flight Trivia",
            bg=LIGHT_BG,
            fg=NAVY,
            font=self.title_font,
        )
        title_label.pack(pady=(10, 18))

        subtitle_label = tk.Label(
            self.main_frame,
            text="Select your route details to begin your in-flight challenge.",
            bg=LIGHT_BG,
            fg=NAVY,
            font=self.body_font,
        )
        subtitle_label.pack(pady=(0, 24))

        # A sub-frame to group the dropdown menus together neatly
        form_frame = tk.Frame(self.main_frame, bg=WHITE, bd=0, padx=26, pady=24)
        form_frame.pack(pady=10)

        # .grid() is used here instead of .pack() to align labels and dropdowns in rows/columns
        tk.Label(
            form_frame, text="Country of Origin:", bg=WHITE, fg=NAVY,
            font=self.body_font, anchor="w", width=20,
        ).grid(row=0, column=0, sticky="w", padx=(0, 12), pady=10)

        origin_menu = tk.OptionMenu(form_frame, self.origin_var, *self.country_options)
        origin_menu.config(
            font=self.body_font, width=24, bg=WHITE, fg=NAVY,
            activebackground=LIGHT_BG, activeforeground=NAVY,
            relief="groove", highlightthickness=0,
        )
        origin_menu["menu"].config(font=self.body_font, bg=WHITE, fg=NAVY)
        origin_menu.grid(row=0, column=1, sticky="w", pady=10)

        tk.Label(
            form_frame, text="Destination Country:", bg=WHITE, fg=NAVY,
            font=self.body_font, anchor="w", width=20,
        ).grid(row=1, column=0, sticky="w", padx=(0, 12), pady=10)

        destination_menu = tk.OptionMenu(form_frame, self.destination_var, *self.country_options)
        destination_menu.config(
            font=self.body_font, width=24, bg=WHITE, fg=NAVY,
            activebackground=LIGHT_BG, activeforeground=NAVY,
            relief="groove", highlightthickness=0,
        )
        destination_menu["menu"].config(font=self.body_font, bg=WHITE, fg=NAVY)
        destination_menu.grid(row=1, column=1, sticky="w", pady=10)

        supported_countries = ", ".join(QUESTION_BANK.keys())
        tk.Label(
            self.main_frame,
            text=f"Supported destination countries: {supported_countries}",
            bg=LIGHT_BG, fg=RED, font=("Helvetica", 11, "bold"),
        ).pack(pady=(16, 16))

        tk.Button(
            self.main_frame, text="Continue", bg=NAVY, fg=WHITE,
            activebackground=RED, activeforeground=WHITE, font=self.button_font,
            width=18, relief="flat", command=self.validate_route_inputs,
        ).pack(pady=(0, 22))

        tk.Button(
            self.main_frame, text="Menu", bg=WHITE, fg=NAVY,
            activebackground=LIGHT_BG, activeforeground=NAVY, font=self.body_font,
            width=14, relief="groove", command=self.show_historical_statistics_screen,
        ).pack(side="bottom", pady=(12, 6))

    def validate_route_inputs(self) -> None:
        """
        Check that the user made valid selections on the welcome screen.
        If origin and destination are identical, it forces 'Hard' mode.
        """
        origin = self.origin_var.get().strip()
        destination = self.destination_var.get().strip()

        if not origin or not destination:
            messagebox.showerror("Input Error", "Both Country of Origin and Destination Country are required.")
            return

        if origin not in QUESTION_BANK or destination not in QUESTION_BANK:
            messagebox.showerror("Selection Error", "Please choose countries from the dropdown list.")
            return

        if origin == destination:
            messagebox.showinfo("Difficulty Set to Hard", "Origin and destination are the same, so the game is set to Hard mode.")
            self.start_game("Hard")
            return

        # If validation passes, move to the difficulty selection screen
        self.show_difficulty_screen()

    def show_historical_statistics_screen(self) -> None:
        """Render a dashboard showing the data loaded from game_stats.json."""
        self.clear_screen()

        # Extract data from the global dictionary for easy formatting
        sessions_played = GLOBAL_STATS["sessions_played"]
        wins = GLOBAL_STATS["wins"]
        losses = GLOBAL_STATS["losses"]
        ratio = f"{wins}:{losses}" if losses > 0 else f"{wins}:0"
        quickest = GLOBAL_STATS["quickest_answer_time"]
        quickest_text = f"{quickest:.2f}s" if quickest is not None else "N/A"
        elapsed_times = GLOBAL_STATS["elapsed_times"]
        average_elapsed = (sum(elapsed_times) / len(elapsed_times) if elapsed_times else 0.0)
        total_elapsed = sum(elapsed_times) if elapsed_times else 0.0

        tk.Label(
            self.main_frame, text="Historical Statistics", bg=LIGHT_BG, fg=NAVY, font=self.title_font,
        ).pack(pady=(12, 18))

        stats_panel = tk.Frame(self.main_frame, bg=WHITE, padx=22, pady=20)
        stats_panel.pack(fill="x", padx=110, pady=(0, 16))

        summary_lines = [
            f"Sessions Played: {sessions_played}",
            f"Win/Loss Record: {ratio}",
            f"Average Session Time: {average_elapsed:.2f}s",
            f"Total Elapsed Time: {total_elapsed:.2f}s",
            f"Quickest Answer Time: {quickest_text}",
        ]
        
        # We loop over the list above to create multiple labels efficiently
        for line in summary_lines:
            tk.Label(
                stats_panel, text=line, bg=WHITE, fg=NAVY, font=("Helvetica", 12),
                anchor="w", justify="left",
            ).pack(fill="x", pady=3)

        country_panel = tk.Frame(self.main_frame, bg=WHITE, padx=22, pady=16)
        country_panel.pack(fill="x", padx=110, pady=(0, 18))

        tk.Label(
            country_panel, text="Correct / Incorrect Answers by Country", bg=WHITE, fg=NAVY,
            font=("Helvetica", 13, "bold"), anchor="w", justify="left",
        ).pack(fill="x", pady=(0, 8))

        for country in self.country_options:
            tk.Label(
                country_panel,
                text=(f"{country}: {GLOBAL_STATS['correct_by_country'][country]} correct, "
                      f"{GLOBAL_STATS['incorrect_by_country'][country]} incorrect"),
                bg=WHITE, fg=NAVY, font=("Helvetica", 12), anchor="w", justify="left",
            ).pack(fill="x", pady=2)

        tk.Button(
            self.main_frame, text="Back", bg=NAVY, fg=WHITE, activebackground=RED,
            activeforeground=WHITE, font=self.button_font, width=14, relief="flat",
            command=self.show_welcome_screen,
        ).pack()

    def show_difficulty_screen(self) -> None:
        """Render a screen allowing the user to pick Easy or Hard mode."""
        self.clear_screen()

        tk.Label(
            self.main_frame,
            text=f"Route: {self.origin_var.get().strip()} \u2192 {self.destination_var.get().strip()}",
            bg=LIGHT_BG, fg=NAVY, font=self.header_font,
        ).pack(pady=(20, 18))

        tk.Label(
            self.main_frame, text="Select Difficulty", bg=LIGHT_BG, fg=NAVY, font=self.title_font,
        ).pack(pady=(0, 22))

        button_row = tk.Frame(self.main_frame, bg=LIGHT_BG)
        button_row.pack(pady=8)

        # 'lambda' is used here to pass a specific argument ("Easy" or "Hard") to start_game
        tk.Button(
            button_row, text="Easy", bg=NAVY, fg=WHITE, activebackground=RED, activeforeground=WHITE,
            width=14, padx=10, pady=10, font=self.button_font, relief="flat",
            command=lambda: self.start_game("Easy"),
        ).pack(side="left", padx=10)

        tk.Button(
            button_row, text="Hard", bg=RED, fg=WHITE, activebackground=NAVY, activeforeground=WHITE,
            width=14, padx=10, pady=10, font=self.button_font, relief="flat",
            command=lambda: self.start_game("Hard"),
        ).pack(side="left", padx=10)

        tk.Button(
            self.main_frame, text="Back", bg=WHITE, fg=NAVY, width=12, font=self.body_font,
            relief="groove", command=self.show_welcome_screen,
        ).pack(pady=(30, 0))

    def start_game(self, difficulty: str) -> None:
        """
        Pull the correct questions from the Question Bank based on destination 
        and difficulty, then randomise them.

        Args:
            difficulty (str): "Easy" or "Hard" selected by the user.
        """
        if difficulty not in ("Easy", "Hard"):
            messagebox.showerror("Selection Error", "Please choose a valid difficulty.")
            return

        self.difficulty = difficulty
        destination = self.destination_var.get().strip()
        
        # Navigate the dictionary: Find Destination -> Find Difficulty -> Get List of Questions
        bank = QUESTION_BANK.get(destination, {}).get(difficulty, [])

        if len(bank) < self.total_questions:
            messagebox.showerror("Question Bank Error", "Insufficient questions available.")
            return

        # random.sample picks 5 unique questions from the bank so they are out of order
        self.session = GameSession(random.sample(bank, self.total_questions), difficulty, self.total_questions, self.timer_by_mode)
        self.session.start()
        
        # Build the question screen and load the first question
        self.show_trivia_screen()
        self.load_question()

    def show_trivia_screen(self) -> None:
        """Build the core UI template used to display questions and answers."""
        self.clear_screen()

        top_bar = tk.Frame(self.main_frame, bg=LIGHT_BG)
        top_bar.pack(fill="x", pady=(0, 15))

        self.progress_label = tk.Label(top_bar, text="Question 1/5", bg=LIGHT_BG, fg=NAVY, font=self.body_font)
        self.progress_label.pack(side="left")

        self.timer_label = tk.Label(top_bar, text="Time: --", bg=LIGHT_BG, fg=RED, font=("Helvetica", 14, "bold"))
        self.timer_label.pack(side="right")

        self.question_label = tk.Label(
            self.main_frame, text="", bg=WHITE, fg=NAVY, wraplength=860,
            justify="center", padx=20, pady=24, font=self.header_font,
        )
        self.question_label.pack(fill="x", pady=(0, 18))

        # We create 4 blank buttons and store them in a list so we can update them later
        self.answer_buttons = []
        for _ in range(4):
            button = tk.Button(
                self.main_frame, text="", bg=NAVY, fg=WHITE, activebackground=RED,
                activeforeground=WHITE, wraplength=760, justify="center", padx=10,
                pady=12, font=self.button_font, relief="flat",
            )
            button.pack(fill="x", pady=6, padx=70)
            self.answer_buttons.append(button)

        self.feedback_label = tk.Label(self.main_frame, text="", bg=LIGHT_BG, fg=NAVY, font=("Helvetica", 12, "bold"))
        self.feedback_label.pack(pady=(16, 0))

    def load_question(self) -> None:
        """Inject the text of the current question into the UI template."""
        # If we have answered all questions, end the game
        if self.session is None or self.session.is_finished():
            self.finish_game()
            return

        self.session.awaiting_next = False
        question_data = self.session.get_current_question()
        question_text = question_data.get("question", "Question unavailable.")
        options = question_data.get("options", [])

        # Update the UI labels to reflect the current question data
        self.progress_label.config(text=f"Question {self.session.current_index + 1}/{len(self.session.questions)}")
        self.question_label.config(text=question_text)
        self.feedback_label.config(text="")

        # Loop through the 4 buttons we created earlier and assign the option text and commands
        for idx, button in enumerate(self.answer_buttons):
            option_text = options[idx] if idx < len(options) else "N/A"
            button.config(
                text=option_text,
                state="normal",
                # The lambda ensures select_answer receives the specific text of the button clicked
                command=lambda answer=option_text: self.select_answer(answer),
            )

        self.session.question_started_at = time.time()
        self.session.remaining_seconds = self.session.get_current_timer_seconds()
        self.update_timer()

    def update_timer(self) -> None:
        """
        Decrease the countdown timer by 1 second. Uses a recursive tkinter 
        callback (.after) to loop itself continuously.
        """
        if self.session is None:
            return
        self.timer_label.config(text=f"Time: {self.session.remaining_seconds}s")

        # If time runs out, force a timeout
        if self.session.remaining_seconds <= 0:
            self.handle_timeout()
            return

        self.session.remaining_seconds -= 1
        
        # .after(1000) tells tkinter to run this exact function again in 1000 milliseconds (1 second)
        self.active_timer_job = self.root.after(1000, self.update_timer)

    def select_answer(self, selected_option: str) -> None:
        """
        Evaluate the player's chosen answer, provide visual feedback, 
        and schedule the transition to the next question.

        Args:
            selected_option (str): The text of the button the player clicked.
        """
        # Prevent players from clicking multiple buttons at once
        if self.session is None or self.session.awaiting_next or self.session.is_finished():
            return

        # Stop the countdown timer immediately
        if self.active_timer_job is not None:
            self.root.after_cancel(self.active_timer_job)
            self.active_timer_job = None

        self.session.awaiting_next = True
        question_data = self.session.get_current_question()
        correct_answer = question_data.get("answer")

        # Record how fast they clicked the button
        answer_duration = time.time() - self.session.question_started_at
        self.session.record_answer(answer_duration, selected_option == correct_answer)

        # Disable all buttons so they cannot be clicked again
        for button in self.answer_buttons:
            button.config(state="disabled")

        # Check if the answer was right or wrong and update counters
        if selected_option == correct_answer:
            self.feedback_label.config(text="Correct!", fg=NAVY)
        else:
            self.feedback_label.config(text=f"Incorrect. Correct answer: {correct_answer}", fg=RED)

        # Wait 2.2 seconds (2200ms) so the player can read the feedback, then move on
        self.active_timer_job = self.root.after(2200, self.move_to_next_question)

    def handle_timeout(self) -> None:
        """Process what happens when the countdown timer hits 0."""
        if self.session is None or self.session.awaiting_next or self.session.is_finished():
            return

        self.session.awaiting_next = True
        self.session.record_answer(0.0, False)
        correct_answer = self.session.get_current_question().get("answer", "Unavailable")

        for button in self.answer_buttons:
            button.config(state="disabled")

        self.feedback_label.config(text=f"Time up. Correct answer: {correct_answer}", fg=RED)
        self.active_timer_job = self.root.after(2200, self.move_to_next_question)

    def move_to_next_question(self) -> None:
        """Increase the index tracker and trigger the loading of the next question."""
        self.active_timer_job = None
        if self.session is not None:
            self.session.move_to_next()
        self.load_question()

    def finish_game(self) -> None:
        """
        Calculate final win/loss conditions based on score, update the 
        global statistics, and save them to the JSON file.
        """
        if self.session is None:
            return
        session_elapsed = self.session.get_session_elapsed()
        destination = self.destination_var.get().strip()
        
        # To win, they need at least 4 out of 5 correct
        wins_required = (len(self.session.questions) * 3 + 4) // 5
        session_won = self.session.calculate_win_status()

        # Update the master scoreboard
        GLOBAL_STATS["sessions_played"] += 1
        if session_won:
            GLOBAL_STATS["wins"] += 1
        else:
            GLOBAL_STATS["losses"] += 1

        GLOBAL_STATS["correct_by_country"][destination] += self.session.correct_answers
        GLOBAL_STATS["incorrect_by_country"][destination] += self.session.incorrect_answers
        GLOBAL_STATS["elapsed_times"].append(session_elapsed)

        # Check if they set a new personal speed record
        fastest_in_session = self.session.get_fastest_answer()
        if fastest_in_session is not None:
            current_fastest = GLOBAL_STATS["quickest_answer_time"]
            if current_fastest is None or fastest_in_session < current_fastest:
                GLOBAL_STATS["quickest_answer_time"] = fastest_in_session

        self.save_historical_statistics()
        self.show_statistics_screen(session_elapsed, session_won)

    def show_statistics_screen(self, session_elapsed: float, session_won: bool) -> None:
        """
        Render the final results screen displaying the player's score and stats.

        Args:
            session_elapsed (float): Total seconds spent playing this round.
            session_won (bool): True if the player met the required win score.
        """
        self.clear_screen()

        headline = "Great Flight! You Won!" if session_won else "Good Try! You Lost!"
        headline_colour = NAVY if session_won else RED
        
        sessions_played = GLOBAL_STATS["sessions_played"]
        wins = GLOBAL_STATS["wins"]
        losses = GLOBAL_STATS["losses"]
        ratio = f"{wins}:{losses}" if losses > 0 else f"{wins}:0"
        quickest = GLOBAL_STATS["quickest_answer_time"]
        quickest_text = f"{quickest:.2f}s" if quickest is not None else "N/A"
        average_elapsed = (sum(GLOBAL_STATS["elapsed_times"]) / len(GLOBAL_STATS["elapsed_times"]) if GLOBAL_STATS["elapsed_times"] else 0.0)
        destination = self.destination_var.get().strip()

        session = self.session
        correct_answers = session.correct_answers if session is not None else 0
        total_questions = len(session.questions) if session is not None else 0

        tk.Label(self.main_frame, text=headline, bg=LIGHT_BG, fg=headline_colour, font=self.title_font).pack(pady=(10, 18))
        tk.Label(
            self.main_frame,
            text=(f"Route: {self.origin_var.get().strip()} \u2192 {destination}\n"
                f"Difficulty: {self.difficulty} | Score: {correct_answers}/{total_questions}"),
            bg=LIGHT_BG, fg=NAVY, font=self.body_font, justify="center",
        ).pack(pady=(0, 16))

        stats_panel = tk.Frame(self.main_frame, bg=WHITE, padx=22, pady=20)
        stats_panel.pack(fill="x", padx=120, pady=(4, 16))

        lines = [
            f"Sessions Played: {sessions_played}",
            f"Win/Loss Record: {ratio}",
            f"Current Session Time: {session_elapsed:.2f}s",
            f"Average Session Time: {average_elapsed:.2f}s",
            f"Quickest Answer Time: {quickest_text}",
            f"Correct Answers in {destination}: {GLOBAL_STATS['correct_by_country'][destination]}",
            f"Incorrect Answers in {destination}: {GLOBAL_STATS['incorrect_by_country'][destination]}",
        ]

        for line in lines:
            tk.Label(
                stats_panel, text=line, bg=WHITE, fg=NAVY, font=("Helvetica", 12),
                anchor="w", justify="left",
            ).pack(fill="x", pady=3)

        action_row = tk.Frame(self.main_frame, bg=LIGHT_BG)
        action_row.pack(pady=12)

        tk.Button(
            action_row, text="Play Again", bg=NAVY, fg=WHITE, activebackground=RED,
            activeforeground=WHITE, font=self.button_font, relief="flat", width=14,
            command=self.show_welcome_screen,
        ).pack(side="left", padx=10)

        # root.destroy completely closes the application window safely
        tk.Button(
            action_row, text="Exit", bg=RED, fg=WHITE, activebackground=NAVY,
            activeforeground=WHITE, font=self.button_font, relief="flat", width=14,
            command=self.root.destroy,
        ).pack(side="left", padx=10)

    def run(self) -> None:
        """Start the application. This keeps the window open and listening for clicks."""
        self.root.mainloop()


# This line ensures the game only runs if this specific file is executed directly.
if __name__ == "__main__":
    TriviaGame().run()
