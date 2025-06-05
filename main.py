# Author: aqeelanwar
# Created: 12 March,2020, 7:06 PM
# Email: aqeel.anwar@gatech.edu

from tkinter import *
import numpy as np
import pygame
from tkinter import messagebox
import os
import sys

# Constants
size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#2E86C1'
symbol_O_color = '#E74C3C'
Green_color = '#27AE60'
background_color = '#ECF0F1'
line_color = '#34495E'

class Tic_Tac_Toe():
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.window.configure(bg=background_color)
        
        # Initialize pygame for sound
        try:
            pygame.mixer.init()
            self.load_sounds()
        except Exception as e:
            print(f"Warning: Sound system initialization failed: {e}")
            self.sound_enabled = False
        else:
            self.sound_enabled = True
        
        # Create main frame
        self.main_frame = Frame(self.window, bg=background_color)
        self.main_frame.pack(pady=20)
        
        # Create title label
        self.title_label = Label(
            self.main_frame,
            text="Tic Tac Toe",
            font=('Helvetica', 24, 'bold'),
            bg=background_color,
            fg=line_color
        )
        self.title_label.pack(pady=10)
        
        # Create canvas
        self.canvas = Canvas(
            self.main_frame,
            width=size_of_board,
            height=size_of_board,
            bg='white',
            highlightthickness=2,
            highlightbackground=line_color
        )
        self.canvas.pack(pady=10)
        
        # Create control buttons frame
        self.control_frame = Frame(self.main_frame, bg=background_color)
        self.control_frame.pack(pady=10)
        
        # Create reset button
        self.reset_button = Button(
            self.control_frame,
            text="New Game",
            font=('Helvetica', 12),
            command=self.reset_game,
            bg=Green_color,
            fg='white',
            padx=20,
            pady=10
        )
        self.reset_button.pack(side=LEFT, padx=10)
        
        # Create score label
        self.score_label = Label(
            self.main_frame,
            text="",
            font=('Helvetica', 12),
            bg=background_color,
            fg=line_color
        )
        self.score_label.pack(pady=5)
        
        # Bind events
        self.window.bind('<Button-1>', self.click)
        self.window.bind('<Return>', lambda e: self.reset_game())
        self.window.bind('<space>', lambda e: self.reset_game())
        
        self.initialize_game()

    def load_sounds(self):
        """Load game sound effects"""
        sound_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sounds')
        try:
            if not os.path.exists(sound_dir):
                os.makedirs(sound_dir)
            
            self.move_sound = pygame.mixer.Sound(os.path.join(sound_dir, "move.wav"))
            self.win_sound = pygame.mixer.Sound(os.path.join(sound_dir, "win.wav"))
            self.draw_sound = pygame.mixer.Sound(os.path.join(sound_dir, "draw.wav"))
        except Exception as e:
            print(f"Warning: Could not load sound files: {e}")
            self.sound_enabled = False
            self.move_sound = self.win_sound = self.draw_sound = type('', (), {'play': lambda: None})()

    def play_sound(self, sound):
        """Play a sound if sound system is enabled"""
        if self.sound_enabled:
            try:
                sound.play()
            except Exception as e:
                print(f"Warning: Could not play sound: {e}")

    def initialize_game(self):
        """Initialize or reset the game state"""
        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))
        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False
        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0
        self.update_score_display()

    def update_score_display(self):
        """Update the score display"""
        score_text = f"Player X: {self.X_score} | Player O: {self.O_score} | Ties: {self.tie_score}"
        self.score_label.config(text=score_text)

    def initialize_board(self):
        """Draw the initial game board"""
        self.canvas.delete("all")
        for i in range(2):
            self.canvas.create_line(
                (i + 1) * size_of_board / 3, 0,
                (i + 1) * size_of_board / 3, size_of_board,
                fill=line_color, width=2
            )
            self.canvas.create_line(
                0, (i + 1) * size_of_board / 3,
                size_of_board, (i + 1) * size_of_board / 3,
                fill=line_color, width=2
            )

    def draw_O(self, logical_position):
        """Draw O symbol at the given position"""
        logical_position = np.array(logical_position)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(
            grid_position[0] - symbol_size,
            grid_position[1] - symbol_size,
            grid_position[0] + symbol_size,
            grid_position[1] + symbol_size,
            width=symbol_thickness,
            outline=symbol_O_color
        )
        self.play_sound(self.move_sound)

    def draw_X(self, logical_position):
        """Draw X symbol at the given position"""
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(
            grid_position[0] - symbol_size,
            grid_position[1] - symbol_size,
            grid_position[0] + symbol_size,
            grid_position[1] + symbol_size,
            width=symbol_thickness,
            fill=symbol_X_color
        )
        self.canvas.create_line(
            grid_position[0] - symbol_size,
            grid_position[1] + symbol_size,
            grid_position[0] + symbol_size,
            grid_position[1] - symbol_size,
            width=symbol_thickness,
            fill=symbol_X_color
        )
        self.play_sound(self.move_sound)

    def display_gameover(self):
        """Display game over screen with results"""
        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player X'
            color = symbol_X_color
            self.play_sound(self.win_sound)
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player O'
            color = symbol_O_color
            self.play_sound(self.win_sound)
        else:
            self.tie_score += 1
            text = 'Game Tied!'
            color = 'gray'
            self.play_sound(self.draw_sound)

        self.canvas.delete("all")
        self.canvas.create_text(
            size_of_board / 2,
            size_of_board / 3,
            font=('Helvetica', 40, 'bold'),
            fill=color,
            text=text
        )

        self.update_score_display()
        self.gameover = True
        self.reset_board = True

        # Show message box
        messagebox.showinfo("Game Over", f"{text}\nClick 'New Game' to play again!")

    def reset_game(self):
        """Reset the game for a new round"""
        self.canvas.delete("all")
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

    def click(self, event):
        """Handle mouse click events"""
        if self.gameover:
            return

        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.is_grid_occupied(logical_position):
            if self.player_X_turns:
                self.draw_X(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = -1
            else:
                self.draw_O(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = 1

            self.player_X_turns = not self.player_X_turns

            if self.is_gameover():
                self.display_gameover()

    def mainloop(self):
        """Start the game main loop"""
        self.window.mainloop()

    def convert_logical_to_grid_position(self, logical_position):
        """Convert logical position to grid position"""
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        """Convert grid position to logical position"""
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        """Check if the grid position is occupied"""
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        return True

    def is_winner(self, player):
        """Check if the player has won"""
        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):
        """Check if the game is a tie"""
        return not np.any(self.board_status == 0)

    def is_gameover(self):
        """Check if the game is over"""
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        return self.X_wins or self.O_wins or self.tie

def main():
    """Main function to start the game"""
    try:
        game_instance = Tic_Tac_Toe()
        game_instance.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()