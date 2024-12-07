import sys


class TriggleGame:
    def __init__(self, side_length):
        self.side_length = side_length
        self.board = self.initialize_board(side_length)
        self.sticks = set()
        self.triangles = {}

        self.current_player = None

#DONE
    def initialize_board(self, side_length):
        return (
            [[None] * (side_length + i) for i in range(side_length)] +  # Upper triangle
            [[None] * (2 * side_length - i - 1) for i in range(1, side_length)]  # Lower triangle
        )

    def display_board(self):
        n = self.side_length
        max_width = 2 * self.side_length - 1
        column_numbers = '     '.join(f"{i}" for i in range(1, max_width + 1))

        # Display column numbers
        print(f"   {'   ' * (n - 1)}{column_numbers}")

        for i in range(len(self.board)):

            offset = abs(n - 1 - i)  # Indent for alignment
            row_label = chr(65 + i)

            # Peg line
            peg_line = []
            for j in range(len(self.board[i])):
                peg_line.append("●")
                peg_line.append("-----" if self.is_part_of_horizontal_stick(i, j) else "     ")

            # First triangle line (diagonal sticks)
            first_triangle_line = []
            for j in range(len(self.board[i])):
                down_left = self.is_part_of_diagonal_stick(i, j, "DL")
                down_right = self.is_part_of_diagonal_stick(i, j, "DD")

                # Add left diagonal
                first_triangle_line.append("/" if down_left else " ")

                # Add space between left and right diagonals
                first_triangle_line.append(" " * 1)

                # Add right diagonal
                first_triangle_line.append("\\" if down_right else " ")
                #first_triangle_line.append("   ")
                # Add the triangle owner
                owner = self.triangles.get((i, j), " ")  # Get the owner ('X', 'O', or None)
                first_triangle_line.append(f" {owner} ")


            # Second triangle line
            second_triangle_line = []
            for j in range(len(self.board[i])):
                down_left = self.is_part_of_diagonal_stick(i, j, "DL")
                second_triangle_line.append("/" if down_left else " ")

                # Add the triangle owner
                owner = self.triangles.get((i, j), " ")  # Get the owner ('X', 'O', or None)
                second_triangle_line.append(f"{owner}")

                down_right = self.is_part_of_diagonal_stick(i, j, "DD")
                second_triangle_line.append("\\" if down_right else " ")

            # Print peg line
            print(f"{row_label} {'   ' * offset}{''.join(peg_line)}")

            if i < len(self.board) - 1:  # Avoid printing after the last peg line
                print(f" {'   ' * offset}{''.join(first_triangle_line)}")
                print(f"{'   ' * offset}{' '.join(second_triangle_line)}")

        print(f"   {'   ' * (n - 1)}{column_numbers}")
#DONE
    def is_part_of_horizontal_stick(self, row, col):
        if ((row, col), (row, col + 1)) in self.sticks:
            return True
        return False
#DONE
    def is_part_of_diagonal_stick(self, row, col, direction):
        if direction == "DL" and row < self.side_length - 1:  #
            return ((row, col), (row + 1, col)) in self.sticks or ((row + 1, col), (row, col)) in self.sticks
        elif direction == "DL" and row >= self.side_length - 1:
            return ((row, col), (row + 1, col-1)) in self.sticks or ((row + 1, col-1), (row, col)) in self.sticks
        elif direction == "DD" and row < self.side_length - 1:
            return ((row, col), (row + 1, col + 1)) in self.sticks or ((row + 1, col + 1), (row, col)) in self.sticks
        elif direction == "DD" and row >= self.side_length - 1:
            return ((row, col), (row + 1, col)) in self.sticks or ((row + 1, col), (row, col)) in self.sticks
        return False
#DONE
    def is_valid_move(self, row, col, direction):

        r, c = row, col

        for step in range(3):
            #TOP TRIANGLE
            if r < self.side_length - 1:
                deltas = {
                    'D': (0, 1),
                    'DL': (1, 0),
                    'DD': (1, 1)
                }
            else:
                #BOTTOM TRIANGLE
                deltas = {
                    'D': (0, 1),
                    'DL': (1, -1),
                    'DD': (1, 0)
                }

            if direction not in deltas:
                return False, "Invalid direction. Use 'D', 'DL', or 'DD'."

            dr, dc = deltas[direction]

            if not (0 <= r < len(self.board) and 0 <= c < len(self.board[r])):
                return False, f"Peg at step {step + 1} is out of bounds."

            r, c = r + dr, c + dc
        return True, None
#FIX OUT oF RANGE
    def make_move(self, row, col, direction):
        is_valid, error_message = self.is_valid_move(row, col, direction)
        if not is_valid:
            raise ValueError(error_message)

        r, c = row, col
        for _ in range(3):

            # Update deltas based on the current value of r

            #TOP TRIANGLE
            if r < self.side_length - 1:
                deltas = {
                    'D': (0, 1),
                    'DL': (1, 0),
                    'DD': (1, 1)
                }
            else:
                #BOTTOM TRIANGLE
                deltas = {
                    'D': (0, 1),
                    'DL': (1, -1),
                    'DD': (1, 0)
                }

            print(f"1. Debug: Current sticks in the game: {self.sticks}")
            print(f"Current r: {self.sticks}")

            dr, dc = deltas[direction]

            if not (0 <= r < len(self.board) and 0 <= c < len(self.board[r])):
                raise ValueError("Move out of bounds.")

            next_r, next_c = r + dr, c + dc
            self.sticks.add(((r, c), (next_r, next_c)))
            r, c = next_r, next_c

        print(f"2. Debug: Current sticks in the game: {self.sticks}")

        self.check_and_capture_triangles(row, col, direction)
        self.switch_player()
#TO DO
    def check_and_capture_triangles(self, row, col, direction):
        # To be implemented
        pass
#DONE
    def switch_player(self):
        self.current_player = 'X' if self.current_player == 'O' else 'O'
#DONE
    def is_game_over(self):
        n = self.side_length

        max_triangles = self.calculate_max_triangles()

        # Count triangles owned by each player
        x_count = sum(1 for owner in self.triangles.values() if owner == 'X')
        o_count = sum(1 for owner in self.triangles.values() if owner == 'O')

        # All triangles are taken/ player has majority
        if x_count + o_count == max_triangles:
            print("Game over: All triangles are captured.")
            return True

        if x_count > max_triangles // 2:
            print("Game over: Player X has won by majority!")
            return True

        if o_count > max_triangles // 2:
            print("Game over: Player O has won by majority!")
            return True

        #Calculate max_sticks here
        max_sticks = self.calculate_max_sticks()

        # Check if all sticks are placed
        if len(self.sticks) == max_sticks:
            print("Game over: All sticks are placed.")
            return True

        return False
#DONE
    def calculate_max_triangles(self):
        max_triangles = 0
        for step in range(self.side_length - 1):
            max_triangles += 2 * len(self.board[step]) - 1
        max_triangles = max_triangles * 2
        return max_triangles
#DONE
    def calculate_max_sticks(self):

        number_of_pegs = sum(len(row) for row in self.board)

        number_of_sticks =  6 * 3 + (self.side_length - 2) * 4 * 6 +  ( number_of_pegs - 6 - (self.side_length - 2)* 6) * 6
        number_of_sticks = number_of_sticks / 2;
        return number_of_sticks
#DONE
def setup_game():
    #n = int(input("Enter the side length of the hexagonal board (4-8): "))
    n = 4
    if n < 4 or n > 8:
        raise ValueError("Side length must be between 4 and 8.")

    #first_player = input("Who will play first? (X/O): ").strip().upper()
    first_player = 'X'
    if first_player not in ['X', 'O']:
        raise ValueError("Invalid choice. Choose 'X' or 'O'.")

    game = TriggleGame(n)
    game.current_player = first_player
    print(f" Broj gumica: {game.calculate_max_sticks()}")
    return game

def main():
    game = setup_game()

    while not game.is_game_over():
        print(f"\n{game.current_player}'s turn.")

        game.display_board()
        try:
            move = input("Enter your move (format: row column direction): ").strip()
            row, col, direction = move.rsplit(' ', 2)
            row, col = ord(row.upper()) - 65, int(col) - 1
            game.make_move(row, col, direction.upper())
            game.display_board()


        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")




    print("\nGame Over!")

if __name__ == "__main__":
    main()