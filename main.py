import sys


class TriggleGame:
    def __init__(self, side_length):
        self.side_length = side_length
        self.board = self.initialize_board(side_length)
        self.sticks = set()
        self.triangles = {}
        self.current_player = None
        self.max_sticks = None
        self.peg_number = None
        self.player_moves = {'X': [], 'O': []}

#DONE
    def initialize_board(self, side_length):
        return (
            [[None] * (side_length + i) for i in range(side_length)] +  # Upper triangle
            [[None] * (2 * side_length - i - 1) for i in range(1, side_length)]  # Lower triangle
        )
#DONE
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

                # Get the triangle owner upper
                triangle_owner = self.get_triangle_owner(i, j, True)
                first_triangle_line.append(f" {triangle_owner} ")

            # Second triangle line
            second_triangle_line = []
            for j in range(len(self.board[i])):
                down_left = self.is_part_of_diagonal_stick(i, j, "DL")
                second_triangle_line.append("/" if down_left else " ")

                # Add the triangle owner
                triangle_owner = self.get_triangle_owner(i, j, False)
                second_triangle_line.append(f"{triangle_owner}")

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
        if direction == "DL" and row >= self.side_length - 1:
            return ((row, col), (row + 1, col-1)) in self.sticks or ((row + 1, col-1), (row, col)) in self.sticks
        if direction == "DD" and row < self.side_length - 1:
            return ((row, col), (row + 1, col + 1)) in self.sticks or ((row + 1, col + 1), (row, col)) in self.sticks
        if direction == "DD" and row >= self.side_length - 1:
            return ((row, col), (row + 1, col)) in self.sticks or ((row + 1, col), (row, col)) in self.sticks
        return False
#DONE
    def get_triangle_owner(self, row, col, downward):
        triangle_owner = " "

        # Determine potential triangles based on `firstRow` flag
        if downward:  # Use downward-facing triangle formula
            if row < self.side_length - 1:  # Upper triangle board
                potential_triangles = [
                    [(row, col), (row, col + 1), (row + 1, col+1)]  # Downward-facing triangle
                ]
            else:  # Lower triangle board
                potential_triangles = [
                    [(row, col), (row, col + 1), (row + 1, col)]  # Downward-facing triangle
                ]
        else:  # Use upward-facing triangle formula
            if row < self.side_length - 1:  # Upper triangle board
                potential_triangles = [
                    [(row, col), (row + 1, col), (row + 1, col + 1)]  # Upward-facing triangle
                ]
            else:  # Lower triangle board
                potential_triangles = [
                    [(row, col), (row + 1, col - 1), (row + 1, col)]  # Upward-facing triangle
                ]

        # Check ownership for potential triangles
        for corners in potential_triangles:
            triangle_key = tuple(sorted(corners))
            if triangle_key in self.triangles:
                triangle_owner = self.triangles[triangle_key]
                break  # Return the first matching triangle's owner

        return triangle_owner
#DONE
    def is_valid_move(self, row, col, direction):

        # Check if the move has already been played
        for moves in self.player_moves.values():
            if (row, col, direction) in moves:
                return False, "This move has already been played."

        r, c = row, col

        for step in range(3):
            # Set deltas based on the current row
            if r < self.side_length - 1:  # Upper triangle
                deltas = {
                    'D': (0, 1),
                    'DL': (1, 0),
                    'DD': (1, 1)
                }
            else:  # Lower triangle
                deltas = {
                    'D': (0, 1),
                    'DL': (1, -1),
                    'DD': (1, 0)
                }

            if direction not in deltas:
                return False, "Invalid direction. Use 'D', 'DL', or 'DD'."

            dr, dc = deltas[direction]
            next_r, next_c = r + dr, c + dc

            # Check if the new position is within bounds
            if not (0 <= next_r < len(self.board) and 0 <= next_c < len(self.board[next_r])):
                return False, f"Peg at step {step + 1} is out of bounds."

            r, c = next_r, next_c

        return True, None
#DONE
    def make_move(self, row, col, direction):
        is_valid, error_message = self.is_valid_move(row, col, direction)
        if not is_valid:
            raise ValueError(error_message)

        r, c = row, col
        self.player_moves[self.current_player].append((row, col, direction))

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

            dr, dc = deltas[direction]

            if not (0 <= r < len(self.board) and 0 <= c < len(self.board[r])):
                raise ValueError("Move out of bounds.")

            next_r, next_c = r + dr, c + dc
            self.sticks.add(((r, c), (next_r, next_c)))

            r, c = next_r, next_c

        self.check_and_capture_triangles()
        self.switch_player()

    def check_and_capture_triangles(self):
        def is_triangle_completed(corners):
            return all(
                ((corners[i], corners[(i + 1) % len(corners)]) in self.sticks or
                 (corners[(i + 1) % len(corners)], corners[i]) in self.sticks)
                for i in range(len(corners))
            )

        # Traverse the board
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                potential_triangles = []

                # Add potential triangles based on the peg's location
                if row < self.side_length - 1:  # Upper triangle
                    potential_triangles.extend([
                        # Triangle facing down
                        [(row, col), (row, col + 1), (row + 1, col+1)],
                        # Triangle facing up
                        [(row, col), (row + 1, col), (row + 1, col + 1)]
                    ])
                else:  # Lower triangle
                    potential_triangles.extend([
                        # Triangle facing down
                        [(row, col), (row, col + 1), (row + 1, col)],
                        # Triangle facing up
                        [(row, col), (row + 1, col - 1), (row + 1, col)]
                    ])

                # Check each potential triangle
                for corners in potential_triangles:
                    if is_triangle_completed(corners):
                        # Sort the corners to have a consistent representation
                        triangle_key = tuple(sorted(corners))
                        if triangle_key not in self.triangles:
                            # Capture the triangle with 'X' or 'O' (you can decide default ownership logic here)
                            self.triangles[triangle_key] = self.current_player
                            #print(f"Captured triangle: {triangle_key} by player {self.current_player}")
#DONE
    def switch_player(self):
        self.current_player = 'X' if self.current_player == 'O' else 'O'
#DONE
    def is_game_over(self):
        max_triangles = self.calculate_max_triangles()

        # Count triangles owned by each player
        x_count = sum(1 for owner in self.triangles.values() if owner == 'X')
        o_count = sum(1 for owner in self.triangles.values() if owner == 'O')
        print(f"Score - X: {x_count} O:{o_count}")

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

        # Check if all sticks are placed
        if len(self.sticks) == self.max_sticks:
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

#MAKE IT MORE READABLE
        number_of_connections =  6 * 3 + (self.side_length - 2) * 4 * 6 +  ( self.peg_number - 6 - (self.side_length - 2)* 6) * 6
        number_of_sticks = number_of_connections / 2
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

    game.peg_number = sum(len(row) for row in game.board)
    game.max_sticks = game.calculate_max_sticks()

    return game

#REDO
def main():
    game = setup_game()

    while not game.is_game_over():
        print(f"\n{game.current_player}'s turn.")

        game.display_board()
#This doesn't need to be here
        try:
            move = input("Enter your move (format: row column direction): ").strip()
            row, col, direction = move.rsplit(' ', 2)
            row, col = ord(row.upper()) - 65, int(col) - 1
            game.make_move(row, col, direction.upper())

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    print("\nGame Over!")

if __name__ == "__main__":
    main()