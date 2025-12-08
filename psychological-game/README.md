# 🧠 Psychological Interference Test: Quick Reaction Challenge

A digital implementation of a cognitive interference test (similar to the **Stroop Effect**), developed entirely in Python using the **Flet** framework for a modern, cross-platform user interface.

This game measures your reaction speed and your brain's ability to **inhibit an automatic response** and focus on the relevant task.

---

## ✨ Features

* **Dual Game Modes:** Allows switching between the response based on the **Shape (Figures)** or the **Color (Colors)** of the ink.
* **Dual Controls:** Full support for responding via **mouse click** on the figures or using the **Q** and **P** keys for rapid-fire answers.
* **Visual Feedback:** Quick notifications (`SnackBar`) for incorrect responses.
* **Clear Interface:** Intuitive user interface designed to minimize distractions during the test.

---

## 🕹️ How to Play

The goal is to react as quickly as possible to the rule established by the game mode, selecting the correct figure (Blue Square **Q** or Red Circle **P**).

| Figure | Response Key | Meaning (Figures Mode) | Meaning (Colors Mode) |
| :--- | :--- | :--- | :--- |
| **Blue Square** | **Q** | Matches the written word "Cuadrado" (Square) | Matches the ink color **Blue** |
| **Red Circle** | **P** | Matches the written word "Círculo" (Circle) | Matches the ink color **Red** |

### ➡️ Game Modes

1.  **Figures Mode:** You must respond to the **written word** ("Cuadrado" or "Círculo"), ignoring the ink color.
2.  **Colors Mode (Modified Stroop Effect):** You must respond to the **INK COLOR** (Blue or Red), ignoring the word that is written.
