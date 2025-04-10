# 🎮 Tic Tac Toe (Console Version)

A Python-based interactive **Tic Tac Toe** game for two players, with extra features like:
- ✅ Single-player mode with unbeatable **Minimax AI**
- 🌈 Colorful terminal UI using `colorama`
- 💾 Save & load game state
- 🏆 Persistent scoreboard tracking wins and draws

---

## 🚀 Features

- **Two Modes**:  
  - Player vs Player  
  - Player vs AI (Minimax algorithm)

- **Smart AI**:  
  - Uses recursive Minimax algorithm  
  - Never loses a game 😎

- **File Handling**:  
  - Save game progress to `game_state.txt`  
  - Resume games from saved state

- **Scoreboard**:  
  - Track game results in `scoreboard.txt`  
  - Auto-displays at the end of each game

- **Colorized Output**:  
  - Red for X, Blue for O, White for empty cells

---

## 🖥️ Run the Game

```bash
pip install colorama
python main.py
