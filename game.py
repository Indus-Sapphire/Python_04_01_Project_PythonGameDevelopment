"""
Geo-Aware Flight Trivia Game using tkinter.

This script runs a desktop trivia game that dynamically selects questions 
based on the user's chosen flight destination. It tracks session statistics 
and saves them to a local JSON file for long-term storage.
"""

from __future__ import annotations 

import json
import random
import time
import tkinter as tk
from pathlib import Path
from typing import Callable, Optional
from tkinter import messagebox

# --- CONSTANTS (Paint Palette) ---
NAVY =  "#01295C"
WHITE = "#FFFFFF"
RED =   "#EB2226"
LIGHT_BG =  "#F3F5F8"

STATS_FILE_PATH = Path(__file__).with_name("game_stats.json")

# --- QUESTION BANK ---
QUESTION_BANK = {
    "Brazil": {
        "Easy": [
            {"question": "What is the capital city of Brazil?", "options": ["Sao Paulo", "Brasilia", "Rio de Janeiro", "Salvador"], "answer": "Brasilia"},
            {"question": "Which famous rainforest is mostly in Brazil?", "options": ["Congo Rainforest", "Daintree Rainforest", "Amazon Rainforest", "Black Forest"], "answer": "Amazon Rainforest"},
            {"question": "What language is primarily spoken in Brazil?", "options": ["Spanish", "Portuguese", "French", "English"], "answer": "Portuguese"},
            {"question": "Which sport is most associated with Brazil?", "options": ["Cricket", "Rugby", "Ice Hockey", "Football (Soccer)"], "answer": "Football (Soccer)"},
            {"question": "Which city hosts the Christ the Redeemer statue?", "options": ["Fortaleza", "Belo Horizonte", "Rio de Janeiro", "Manaus"], "answer": "Rio de Janeiro"},
            {"question": "Which celebration is world-famous in Rio?", "options": ["Carnival", "Oktoberfest", "Day of the Dead", "Diwali"], "answer": "Carnival"},
        ],
        "Hard": [
            {"question": "What is the name of the vast wetland in western Brazil?", "options": ["Pampas", "Pantanal", "Atacama", "Altiplano"], "answer": "Pantanal"},
            {"question": "Which architect co-designed many buildings in Brasilia?", "options": ["Oscar Niemeyer", "Antoni Gaudi", "I. M. Pei", "Le Corbusier"], "answer": "Oscar Niemeyer"},
            {"question": "What is Brazil's highest mountain?", "options": ["Pico da Bandeira", "Pico da Neblina", "Mount Roraima", "Pico das Agulhas Negras"], "answer": "Pico da Neblina"},
            {"question": "In which year did Brazil move its capital to Brasilia?", "options": ["1945", "1960", "1972", "1988"], "answer": "1960"},
            {"question": "Which ocean current strongly affects Brazil's southeast coast?", "options": ["Benguela Current", "Brazil Current", "Canary Current", "California Current"], "answer": "Brazil Current"},
            {"question": "What is the traditional mixed martial art and dance with Afro-Brazilian roots?", "options": ["Samba", "Capoeira", "Forro", "Bossa Nova"], "answer": "Capoeira"},
        ],
    },
    "Nigeria": {
        "Easy": [
            {"question": "What is the capital city of Nigeria?", "options": ["Lagos", "Kano", "Abuja", "Port Harcourt"], "answer": "Abuja"},
            {"question": "Which body of water lies to Nigeria's south?", "options": ["Mediterranean Sea", "Arabian Sea", "Gulf of Guinea", "Red Sea"], "answer": "Gulf of Guinea"},
            {"question": "Which Nigerian city is the country's largest by population?", "options": ["Abuja", "Lagos", "Ibadan", "Enugu"], "answer": "Lagos"},
            {"question": "What is Nigeria's official language?", "options": ["English", "Hausa", "Yoruba", "Igbo"], "answer": "English"},
            {"question": "Nigeria is located on which continent?", "options": ["Asia", "Africa", "Europe", "South America"], "answer": "Africa"},
            {"question": "Which movie industry nickname refers to Nigeria?", "options": ["Nollywood", "Mollywood", "Goldwood", "Afriwood"], "answer": "Nollywood"},
        ],
        "Hard": [
            {"question": "What major river joins the Niger River at Lokoja?", "options": ["Benue River", "Congo River", "Senegal River", "Volta River"], "answer": "Benue River"},
            {"question": "In what year did Nigeria gain independence?", "options": ["1957", "1960", "1963", "1975"], "answer": "1960"},
            {"question": "Which ancient Nigerian civilization is known for bronze and terracotta art?", "options": ["Nok", "Aksum", "Mali", "Songhai"], "answer": "Nok"},
            {"question": "Which city is historically linked to the Yoruba Oyo Empire?", "options": ["Sokoto", "Oyo", "Calabar", "Jos"], "answer": "Oyo"},
            {"question": "What is the name of the traditional ruler of Kano?", "options": ["Oba", "Eze", "Emir", "Lamido"], "answer": "Emir"},
            {"question": "Which plateau city in Nigeria is known for its cooler climate?", "options": ["Jos", "Warri", "Aba", "Onitsha"], "answer": "Jos"},
        ],
    },
    "UK": {
        "Easy": [
            {"question": "What is the capital city of the UK?", "options": ["Manchester", "Cardiff", "London", "Birmingham"], "answer": "London"},
            {"question": "Which river flows through London?", "options": ["Severn", "Thames", "Tyne", "Mersey"], "answer": "Thames"},
            {"question": "What is the currency used in the UK?", "options": ["Euro", "Dollar", "Pound Sterling", "Franc"], "answer": "Pound Sterling"},
            {"question": "Which famous clock tower is in London?", "options": ["Big Ben", "Eiffel Tower", "Clock of Dublin", "Tower of Pisa"], "answer": "Big Ben"},
            {"question": "Which sport is strongly associated with Wimbledon?", "options": ["Cricket", "Rugby", "Tennis", "Golf"], "answer": "Tennis"},
            {"question": "Which country is NOT part of the UK?", "options": ["Scotland", "Wales", "Ireland", "England"], "answer": "Ireland"},
        ],
        "Hard": [
            {"question": "What is the name of the prehistoric monument in Wiltshire?", "options": ["Avebury", "Stonehenge", "Hadrian's Wall", "Skara Brae"], "answer": "Stonehenge"},
            {"question": "Which document signed in 1215 limited royal power in England?", "options": ["Bill of Rights", "Magna Carta", "Act of Union", "Domesday Book"], "answer": "Magna Carta"},
            {"question": "What is the highest mountain in the UK?", "options": ["Scafell Pike", "Snowdon", "Ben Nevis", "Cairn Gorm"], "answer": "Ben Nevis"},
            {"question": "Which UK city is known as the 'Granite City'?", "options": ["Aberdeen", "Glasgow", "Leeds", "York"], "answer": "Aberdeen"},
            {"question": "Which battle in 1066 led to Norman rule in England?", "options": ["Battle of Bosworth", "Battle of Hastings", "Battle of Agincourt", "Battle of Bannockburn"], "answer": "Battle of Hastings"},
            {"question": "What is the name of the shortest commercial flight route in the UK?", "options": ["Belfast to Glasgow", "Westray to Papa Westray", "London to Manchester", "Edinburgh to Inverness"], "answer": "Westray to Papa Westray"},
        ],
    },
    "Mexico": {
        "Easy": [
            {"question": "What is the capital city of Mexico?", "options": ["Guadalajara", "Monterrey", "Mexico City", "Puebla"], "answer": "Mexico City"},
            {"question": "What is the currency of Mexico?", "options": ["Peso", "Real", "Dollar", "Quetzal"], "answer": "Peso"},
            {"question": "Which ancient civilization built Chichen Itza?", "options": ["Maya", "Aztec", "Inca", "Olmec"], "answer": "Maya"},
            {"question": "Which ocean borders Mexico's west coast?", "options": ["Atlantic Ocean", "Pacific Ocean", "Indian Ocean", "Arctic Ocean"], "answer": "Pacific Ocean"},
            {"question": "Which holiday honours deceased loved ones in Mexico?", "options": ["Cinco de Mayo", "Day of the Dead", "Easter", "Independence Day"], "answer": "Day of the Dead"},
            {"question": "Mexico shares its northern border with which country?", "options": ["Guatemala", "Belize", "United States", "Canada"], "answer": "United States"},
        ],
        "Hard": [
            {"question": "What is Mexico's highest peak?", "options": ["Popocatepetl", "Pico de Orizaba", "Nevado de Toluca", "Iztaccihuatl"], "answer": "Pico de Orizaba"},
            {"question": "Which peninsula in southeast Mexico is known for cenotes?", "options": ["Baja California", "Yucatan Peninsula", "Sonora Peninsula", "Isthmus of Tehuantepec"], "answer": "Yucatan Peninsula"},
            {"question": "In which year did Mexico gain independence from Spain?", "options": ["1810", "1821", "1836", "1848"], "answer": "1821"},
            {"question": "What is the name of the large square in central Mexico City?", "options": ["El Malecon", "Zocalo", "Plaza Nueva", "La Alameda"], "answer": "Zocalo"},
            {"question": "Which Mexican state is famous for the monarch butterfly biosphere reserve?", "options": ["Michoacan", "Jalisco", "Chiapas", "Tabasco"], "answer": "Michoacan"},
            {"question": "Which pre-Hispanic city is known for the Pyramid of the Sun?", "options": ["Teotihuacan", "Tulum", "Palenque", "Uxmal"], "answer": "Teotihuacan"},
        ],
    },
}

def create_default_global_stats() -> dict:
    """
    Generate a fresh, empty dictionary for tracking game statistics.
    """
    return {
        "sessions_played": 0,
        "wins": 0,
        "losses": 0,
        "correct_by_country": {country: 0 for country in QUESTION_BANK},
        "incorrect_by_country": {country: 0 for country in QUESTION_BANK},
        "elapsed_times": [],
        "quickest_answer_time": None,
    }

class StatsRepository:
    """
    Handles persistence and validation of game statistics.
    Responsible for loading from and saving to the JSON file.
    """

    def __init__(self, stats_file_path: Path) -> None:
        self.stats_file_path = stats_file_path

    def _non_negative_int(self, value: object) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("Expected a non-negative integer.")
        return value

    def _non_negative_float(self, value: object) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Expected a non-negative number.")
        return float(value)

    def load(self) -> dict:
        default_stats = create_default_global_stats()

        if not self.stats_file_path.exists():
            return default_stats

        try:
            stats_data = json.loads(self.stats_file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            messagebox.showerror("Statistics File Error", f"Could not read historical statistics. Defaults will be used.\n{exc}")
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
            if quickest_answer_time is not None:
                loaded_stats["quickest_answer_time"] = self._non_negative_float(quickest_answer_time)

            return loaded_stats

        except ValueError as exc:
            messagebox.showerror("Statistics Data Error", f"Statistics file data is invalid. Defaults will be used.\n{exc}")
            return default_stats

    def save(self, stats: dict) -> None:
        try:
            self.stats_file_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Statistics File Error", f"Could not save historical statistics.\n{exc}")

class GameSession:
    """
    Encapsulates the state of a single game session (per-round state).
    Tracks questions, answers, timing, and score for the current game.
    """

    def __init__(self, questions: list, difficulty: str, total_questions: int, timer_by_mode: dict) -> None:
        self.questions = questions
        self.difficulty = difficulty
        self.total_questions = total_questions
        self.timer_by_mode = timer_by_mode

        self.current_index = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.session_started_at = time.time()
        self.question_started_at = 0.0
        self.answer_times: list = []
        self.remaining_seconds = 0
        self.awaiting_next = False

    def start(self) -> None:
        self.current_index = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.session_started_at = time.time()
        self.question_started_at = 0.0
        self.answer_times = []
        self.remaining_seconds = 0
        self.awaiting_next = False

    def is_finished(self) -> bool:
        return self.current_index >= len(self.questions)

    def get_current_question(self) -> dict:
        if self.is_finished():
            return {}
        return self.questions[self.current_index]

    def record_answer(self, answer_duration: float, is_correct: bool) -> None:
        self.answer_times.append(answer_duration)
        if is_correct:
            self.correct_answers += 1
        else:
            self.incorrect_answers += 1

    def move_to_next(self) -> None:
        self.current_index += 1

    def get_session_elapsed(self) -> float:
        return time.time() - self.session_started_at

    def get_current_timer_seconds(self) -> int:
        return self.timer_by_mode[self.difficulty]

    def calculate_win_status(self) -> bool:
        wins_required = (len(self.questions) * 3 + 4) // 5
        return self.correct_answers >= wins_required

    def get_fastest_answer(self) -> float | None:
        return min(self.answer_times) if self.answer_times else None

class TriviaGame:
    """
    The main UI Manager.
    
    This class handles the creation of the graphical window and the flow of the 
    screens, relying on GameSession for logic and StatsRepository for data.
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Geo-Aware Flight Trivia")
        self.root.geometry("980x640")
        self.root.configure(bg=LIGHT_BG)

        self.main_frame = tk.Frame(self.root, bg=LIGHT_BG, padx=30, pady=30)
        self.main_frame.pack(fill="both", expand=True)

        self.country_options = list(QUESTION_BANK.keys())
        self.origin_var = tk.StringVar(value=self.country_options[0])
        self.destination_var = tk.StringVar(
            value=self.country_options[1] if len(self.country_options) > 1 else self.country_options[0]
        )
        
        self.difficulty = ""
        self.session: GameSession | None = None
        self.active_timer_job = None

        self.total_questions = 5
        self.timer_by_mode = {"Easy": 20, "Hard": 12}

        self.title_font = ("Helvetica", 28, "bold")
        self.header_font = ("Helvetica", 18, "bold")
        self.body_font = ("Helvetica", 13)
        self.button_font = ("Helvetica", 12, "bold")

        # Dependency Injection & Encapsulation: Use objects instead of global variables
        self.stats_repo = StatsRepository(STATS_FILE_PATH)
        self.global_stats = self.stats_repo.load()
        self.stats_repo.save(self.global_stats) # Ensure file is created on first run
        
        self.show_welcome_screen()

    # --- UI Helper Methods (DRY Principle) ---
    def _create_action_button(self, parent, text: str, command: Optional[Callable[..., None]] = None, is_primary: bool = True, **kwargs) -> tk.Button:
        """Helper to create buttons with consistent theme styling to avoid redundant code."""
        bg_color = NAVY if is_primary else RED
        active_bg = RED if is_primary else NAVY
        
        # Only include the command kwarg when a callable is provided to satisfy static type checkers
        btn_kwargs = dict(text=text, bg=bg_color, fg=WHITE,
                          activebackground=active_bg, activeforeground=WHITE,
                          font=self.button_font, relief="flat", **kwargs)
        if command is not None:
            btn_kwargs["command"] = command

        btn = tk.Button(parent, **btn_kwargs)
        return btn

    def _render_stats_panel(self, parent: tk.Widget, lines: list, padx_val: int = 110) -> None:
        """Helper to render the white data-display panels on statistics screens."""
        stats_panel = tk.Frame(parent, bg=WHITE, padx=22, pady=20)
        stats_panel.pack(fill="x", padx=padx_val, pady=(4, 16))
        for line in lines:
            tk.Label(
                stats_panel, text=line, bg=WHITE, fg=NAVY, font=("Helvetica", 12),
                anchor="w", justify="left"
            ).pack(fill="x", pady=3)

    def clear_screen(self) -> None:
        if self.active_timer_job is not None:
            self.root.after_cancel(self.active_timer_job)
            self.active_timer_job = None

        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_welcome_screen(self) -> None:
        self.clear_screen()

        tk.Label(self.main_frame, text="Geo-Aware Flight Trivia", bg=LIGHT_BG, fg=NAVY, font=self.title_font).pack(pady=(10, 18))
        tk.Label(self.main_frame, text="Select your route details to begin your in-flight challenge.", bg=LIGHT_BG, fg=NAVY, font=self.body_font).pack(pady=(0, 24))

        form_frame = tk.Frame(self.main_frame, bg=WHITE, bd=0, padx=26, pady=24)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Country of Origin:", bg=WHITE, fg=NAVY, font=self.body_font, anchor="w", width=20).grid(row=0, column=0, sticky="w", padx=(0, 12), pady=10)
        origin_menu = tk.OptionMenu(form_frame, self.origin_var, *self.country_options)
        origin_menu.config(font=self.body_font, width=24, bg=WHITE, fg=NAVY, activebackground=LIGHT_BG, activeforeground=NAVY, relief="groove", highlightthickness=0)
        origin_menu["menu"].config(font=self.body_font, bg=WHITE, fg=NAVY)
        origin_menu.grid(row=0, column=1, sticky="w", pady=10)

        tk.Label(form_frame, text="Destination Country:", bg=WHITE, fg=NAVY, font=self.body_font, anchor="w", width=20).grid(row=1, column=0, sticky="w", padx=(0, 12), pady=10)
        destination_menu = tk.OptionMenu(form_frame, self.destination_var, *self.country_options)
        destination_menu.config(font=self.body_font, width=24, bg=WHITE, fg=NAVY, activebackground=LIGHT_BG, activeforeground=NAVY, relief="groove", highlightthickness=0)
        destination_menu["menu"].config(font=self.body_font, bg=WHITE, fg=NAVY)
        destination_menu.grid(row=1, column=1, sticky="w", pady=10)

        supported_countries = ", ".join(QUESTION_BANK.keys())
        tk.Label(self.main_frame, text=f"Supported destination countries: {supported_countries}", bg=LIGHT_BG, fg=RED, font=("Helvetica", 11, "bold")).pack(pady=(16, 16))

        self._create_action_button(
            self.main_frame, "Continue", self.validate_route_inputs, is_primary=True, width=18
        ).pack(pady=(0, 22))

        tk.Button(
            self.main_frame, text="Menu", bg=WHITE, fg=NAVY, activebackground=LIGHT_BG, 
            activeforeground=NAVY, font=self.body_font, width=14, relief="groove", 
            command=self.show_historical_statistics_screen
        ).pack(side="bottom", pady=(12, 6))

    def validate_route_inputs(self) -> None:
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

        self.show_difficulty_screen()

    def _generate_history_summary_lines(self) -> list[str]:
        """Helper to compute historical string logic for use in multiple screens."""
        sessions_played = self.global_stats["sessions_played"]
        wins = self.global_stats["wins"]
        losses = self.global_stats["losses"]
        ratio = f"{wins}:{losses}" if losses > 0 else f"{wins}:0"
        
        quickest = self.global_stats["quickest_answer_time"]
        quickest_text = f"{quickest:.2f}s" if quickest is not None else "N/A"
        
        elapsed_times = self.global_stats["elapsed_times"]
        average_elapsed = (sum(elapsed_times) / len(elapsed_times) if elapsed_times else 0.0)
        total_elapsed = sum(elapsed_times) if elapsed_times else 0.0

        return [
            f"Sessions Played: {sessions_played}",
            f"Win/Loss Record: {ratio}",
            f"Average Session Time: {average_elapsed:.2f}s",
            f"Total Elapsed Time: {total_elapsed:.2f}s",
            f"Quickest Answer Time: {quickest_text}",
        ]

    def show_historical_statistics_screen(self) -> None:
        self.clear_screen()

        tk.Label(self.main_frame, text="Historical Statistics", bg=LIGHT_BG, fg=NAVY, font=self.title_font).pack(pady=(12, 18))

        # Use helper method to render summary panel
        summary_lines = self._generate_history_summary_lines()
        self._render_stats_panel(self.main_frame, summary_lines)

        # Build country-specific breakdown
        country_lines = ["Correct / Incorrect Answers by Country"]
        for country in self.country_options:
            correct = self.global_stats['correct_by_country'][country]
            incorrect = self.global_stats['incorrect_by_country'][country]
            country_lines.append(f"{country}: {correct} correct, {incorrect} incorrect")
            
        self._render_stats_panel(self.main_frame, country_lines)

        self._create_action_button(self.main_frame, "Back", self.show_welcome_screen, width=14).pack()

    def show_difficulty_screen(self) -> None:
        self.clear_screen()

        tk.Label(self.main_frame, text=f"Route: {self.origin_var.get().strip()} \u2192 {self.destination_var.get().strip()}", bg=LIGHT_BG, fg=NAVY, font=self.header_font).pack(pady=(20, 18))
        tk.Label(self.main_frame, text="Select Difficulty", bg=LIGHT_BG, fg=NAVY, font=self.title_font).pack(pady=(0, 22))

        button_row = tk.Frame(self.main_frame, bg=LIGHT_BG)
        button_row.pack(pady=8)

        self._create_action_button(button_row, "Easy", lambda: self.start_game("Easy"), is_primary=True, width=14, padx=10, pady=10).pack(side="left", padx=10)
        self._create_action_button(button_row, "Hard", lambda: self.start_game("Hard"), is_primary=False, width=14, padx=10, pady=10).pack(side="left", padx=10)

        tk.Button(self.main_frame, text="Back", bg=WHITE, fg=NAVY, width=12, font=self.body_font, relief="groove", command=self.show_welcome_screen).pack(pady=(30, 0))

    def start_game(self, difficulty: str) -> None:
        if difficulty not in ("Easy", "Hard"):
            messagebox.showerror("Selection Error", "Please choose a valid difficulty.")
            return

        self.difficulty = difficulty
        destination = self.destination_var.get().strip()
        bank = QUESTION_BANK.get(destination, {}).get(difficulty, [])

        if len(bank) < self.total_questions:
            messagebox.showerror("Question Bank Error", "Insufficient questions available.")
            return

        self.session = GameSession(random.sample(bank, self.total_questions), difficulty, self.total_questions, self.timer_by_mode)
        self.session.start()
        
        self.show_trivia_screen()
        self.load_question()

    def show_trivia_screen(self) -> None:
        self.clear_screen()

        top_bar = tk.Frame(self.main_frame, bg=LIGHT_BG)
        top_bar.pack(fill="x", pady=(0, 15))

        self.progress_label = tk.Label(top_bar, text="Question 1/5", bg=LIGHT_BG, fg=NAVY, font=self.body_font)
        self.progress_label.pack(side="left")

        self.timer_label = tk.Label(top_bar, text="Time: --", bg=LIGHT_BG, fg=RED, font=("Helvetica", 14, "bold"))
        self.timer_label.pack(side="right")

        self.question_label = tk.Label(self.main_frame, text="", bg=WHITE, fg=NAVY, wraplength=860, justify="center", padx=20, pady=24, font=self.header_font)
        self.question_label.pack(fill="x", pady=(0, 18))

        self.answer_buttons = []
        for _ in range(4):
            btn = self._create_action_button(self.main_frame, "", None, wraplength=760, justify="center", padx=10, pady=12)
            btn.pack(fill="x", pady=6, padx=70)
            self.answer_buttons.append(btn)

        self.feedback_label = tk.Label(self.main_frame, text="", bg=LIGHT_BG, fg=NAVY, font=("Helvetica", 12, "bold"))
        self.feedback_label.pack(pady=(16, 0))

    def load_question(self) -> None:
        if self.session is None or self.session.is_finished():
            self.finish_game()
            return

        self.session.awaiting_next = False
        question_data = self.session.get_current_question()
        question_text = question_data.get("question", "Question unavailable.")
        options = question_data.get("options", [])

        self.progress_label.config(text=f"Question {self.session.current_index + 1}/{len(self.session.questions)}")
        self.question_label.config(text=question_text)
        self.feedback_label.config(text="")

        for idx, button in enumerate(self.answer_buttons):
            option_text = options[idx] if idx < len(options) else "N/A"
            button.config(text=option_text, state="normal", command=lambda answer=option_text: self.select_answer(answer))

        self.session.question_started_at = time.time()
        self.session.remaining_seconds = self.session.get_current_timer_seconds()
        self.update_timer()

    def update_timer(self) -> None:
        if self.session is None:
            return
        self.timer_label.config(text=f"Time: {self.session.remaining_seconds}s")

        if self.session.remaining_seconds <= 0:
            self.handle_timeout()
            return

        self.session.remaining_seconds -= 1
        self.active_timer_job = self.root.after(1000, self.update_timer)

    def select_answer(self, selected_option: str) -> None:
        if self.session is None or self.session.awaiting_next or self.session.is_finished():
            return

        if self.active_timer_job is not None:
            self.root.after_cancel(self.active_timer_job)
            self.active_timer_job = None

        self.session.awaiting_next = True
        question_data = self.session.get_current_question()
        correct_answer = question_data.get("answer")

        answer_duration = time.time() - self.session.question_started_at
        is_correct = (selected_option == correct_answer)
        self.session.record_answer(answer_duration, is_correct)

        for button in self.answer_buttons:
            button.config(state="disabled")

        if is_correct:
            self.feedback_label.config(text="Correct!", fg=NAVY)
        else:
            self.feedback_label.config(text=f"Incorrect. Correct answer: {correct_answer}", fg=RED)

        self.active_timer_job = self.root.after(2200, self.move_to_next_question)

    def handle_timeout(self) -> None:
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
        self.active_timer_job = None
        if self.session is not None:
            self.session.move_to_next()
        self.load_question()

    def finish_game(self) -> None:
        if self.session is None:
            return
            
        session_elapsed = self.session.get_session_elapsed()
        destination = self.destination_var.get().strip()
        session_won = self.session.calculate_win_status()

        # Update the encapsulated master scoreboard
        self.global_stats["sessions_played"] += 1
        if session_won:
            self.global_stats["wins"] += 1
        else:
            self.global_stats["losses"] += 1

        self.global_stats["correct_by_country"][destination] += self.session.correct_answers
        self.global_stats["incorrect_by_country"][destination] += self.session.incorrect_answers
        self.global_stats["elapsed_times"].append(session_elapsed)

        fastest_in_session = self.session.get_fastest_answer()
        if fastest_in_session is not None:
            current_fastest = self.global_stats["quickest_answer_time"]
            if current_fastest is None or fastest_in_session < current_fastest:
                self.global_stats["quickest_answer_time"] = fastest_in_session

        self.stats_repo.save(self.global_stats)
        self.show_statistics_screen(session_elapsed, session_won)

    def show_statistics_screen(self, session_elapsed: float, session_won: bool) -> None:
        self.clear_screen()

        headline = "Great Flight! You Won!" if session_won else "Good Try! You Lost!"
        headline_colour = NAVY if session_won else RED
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

        # Re-use our helper logic for standard items
        summary_lines = self._generate_history_summary_lines()
        
        # We replace the two 'Total/Average Elapsed Time' strings with 'Current Session Time' for this specific view
        summary_lines[2] = f"Current Session Time: {session_elapsed:.2f}s"
        del summary_lines[3]
        
        # Add the country specific variables to our lines 
        summary_lines.extend([
            f"Correct Answers in {destination}: {self.global_stats['correct_by_country'][destination]}",
            f"Incorrect Answers in {destination}: {self.global_stats['incorrect_by_country'][destination]}"
        ])

        # Use helper method to render panel
        self._render_stats_panel(self.main_frame, summary_lines, padx_val=120)

        action_row = tk.Frame(self.main_frame, bg=LIGHT_BG)
        action_row.pack(pady=12)

        self._create_action_button(action_row, "Play Again", self.show_welcome_screen, width=14).pack(side="left", padx=10)
        self._create_action_button(action_row, "Exit", self.root.destroy, is_primary=False, width=14).pack(side="left", padx=10)

    def run(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    TriviaGame().run()
