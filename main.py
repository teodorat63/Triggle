import sys


class TriggleGame:
    def __init__(self, side_length):
        self.side_length = side_length
        self.board = self.initialize_board(side_length)
        self.sticks = {
            # Za prvi trougao
            ((0, 0), (1, 0)),
            ((1, 0), (1, 1)),
            ((1, 1), (0, 0)),

            # Za drugi trougao
            ((1, 0), (2, 0)),
            ((2, 0), (2, 1)),
            ((2, 1), (1, 0))
        }
        self.triangles = {
            (0, 0): 'X',
            (1, 0): 'O'
        }

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

    def is_part_of_horizontal_stick(self, row, col):
        if ((row, col), (row, col + 1)) in self.sticks:
            return True
        return False

    def is_part_of_diagonal_stick(self, row, col, direction):
        if direction == "DL":  #
            return ((row, col), (row + 1, col)) in self.sticks or ((row + 1, col), (row, col)) in self.sticks
        elif direction == "DD":
            return ((row, col), (row + 1, col + 1)) in self.sticks or ((row + 1, col + 1), (row, col)) in self.sticks
        return False

    def is_valid_move(self, row, col, direction):
        deltas = {
            'D': (0, 1),  # Rightwards
            'DL': (1, 0),  # Down-left
            'DD': (1, 1)  # Down-right
        }

        if direction not in deltas:
            return False, "Invalid direction. Use 'D', 'DL', or 'DD'."

        dr, dc = deltas[direction]
        r, c = row, col

        for step in range(4):
            if r >= self.side_length:  # Bottom triangle offset adjustment
                bottom_offset = r - (self.side_length - 1)
                adjusted_col = c - bottom_offset
            else:
                adjusted_col = c

            if not (0 <= r < len(self.board) and 0 <= adjusted_col < len(self.board[r])):
                return False, f"Peg at step {step + 1} is out of bounds."

            r, c = r + dr, c + dc

        return True, None

    def make_move(self, row, col, direction):
        is_valid, error_message = self.is_valid_move(row, col, direction)
        if not is_valid:
            raise ValueError(error_message)

        deltas = {
            'D': (0, 1),
            'DL': (1, 0),
            'DD': (1, 1)
        }

        dr, dc = deltas[direction]
        r, c = row, col


        for _ in range(3):
            # Adjust for bottom triangle
            if r >= self.side_length:
                bottom_offset = r - (self.side_length - 1)
                if c < bottom_offset:
                    raise ValueError("Move out of bounds in bottom triangle.")
                adjusted_col = c - bottom_offset
            else:
                adjusted_col = c

            if not (0 <= r < len(self.board) and 0 <= adjusted_col < len(self.board[r])):
                raise ValueError("Move out of bounds.")

            next_r, next_c = r + dr, c + dc
            self.sticks.add(((r, c), (next_r, next_c)))
            r, c = next_r, next_c

#print(f"Debug: Current sticks in the game: {self.sticks}")

        self.check_and_capture_triangles(row, col, direction)
        self.switch_player()

    def check_and_capture_triangles(self, row, col, direction):
        # To be implemented
        pass

    def switch_player(self):
        self.current_player = 'X' if self.current_player == 'O' else 'O'

    def is_game_over(self):
        n = self.side_length

        #To be calculated
        max_triangles = sys.maxsize

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
        max_sticks = sys.maxsize

        # Check if all sticks are placed
        if len(self.sticks) == max_sticks:
            print("Game over: All sticks are placed.")
            return True

        return False


def setup_game():
    #n = int(input("Enter the side length of the hexagonal board (4-8): "))
    n = 8
    if n < 4 or n > 8:
        raise ValueError("Side length must be between 4 and 8.")

    #first_player = input("Who will play first? (X/O): ").strip().upper()
    first_player = 'X'
    if first_player not in ['X', 'O']:
        raise ValueError("Invalid choice. Choose 'X' or 'O'.")

    game = TriggleGame(n)
    game.current_player = first_player
    return game


def main():
    game = setup_game()

    while not game.is_game_over():
        print(f"\n{game.current_player}'s turn.")
        game.make_move(0,0, 'DL')
        game.make_move(0,0, 'DD')

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


    game.display_board()


    print("\nGame Over!")


if __name__ == "__main__":
    main()