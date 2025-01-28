import copy
import time


class TriggleGame:
    def __init__(self, side_length, first_player):
        self.side_length = side_length
        self.board = self.initialize_board(side_length)
        self.sticks = set()
        self.triangles = {}
        self.current_player = 'X'
        self.human_player = first_player
        self.peg_number = sum(len(row) for row in self.board)
        self.max_sticks = self.calculate_max_sticks()
        self.max_triangles = self.calculate_max_triangles()
        self.score = {'X': 0, 'O': 0}

    def initialize_board(self, side_length):
        return (
            [[None] * (side_length + i) for i in range(side_length)] +  # Upper triangle
            [[None] * (2 * side_length - i - 1) for i in range(1, side_length)]  # Lower triangle
        )

    def display_score(self):
        print(f"\n{self.current_player}'s turn.")
        print("Scoreboard")
        for player, score in self.score.items():
            print(f"{player}: {'█' * score} ({score})")

    def display_board(self):
        self.display_score()

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

    def is_part_of_horizontal_stick(self, row, col):
        if ((row, col), (row, col + 1)) in self.sticks:
            return True
        return False

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

    def get_triangle_owner(self, row, col, downward):
        triangle_owner = " "

        # Determine potential triangles based on `firstRow` flag
        if downward:  #fownward-facing triangle formula
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

    def is_valid_move(self, row, col, direction):

        occupied = True
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

            # Check if there's a stick already in this step
            if not (((r, c), (next_r, next_c)) in self.sticks):
                occupied = False

            r, c = next_r, next_c

        if occupied:
            return False, "This move is invalid: All steps in the path are occupied."

        return True, None

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

            dr, dc = deltas[direction]

            if not (0 <= r < len(self.board) and 0 <= c < len(self.board[r])):
                raise ValueError("Move out of bounds.")

            next_r, next_c = r + dr, c + dc
            self.sticks.add(((r, c), (next_r, next_c)))

            r, c = next_r, next_c

        self.check_and_capture_triangles()
        self.switch_player()
        return self

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
                            self.triangles[triangle_key] = self.current_player
                            #Change the score
                            self.score[self.current_player] += 1

    def switch_player(self):
        self.current_player = 'X' if self.current_player == 'O' else 'O'


    def is_game_over(self):

        if self.score['X'] + self.score['O'] == self.max_triangles:
            return True

        if self.score['X'] > self.max_triangles // 2:
            return True

        if self.score['O'] > self.max_triangles // 2:
            return True

        return False

    def calculate_max_triangles(self):
        max_triangles = 0
        for step in range(self.side_length - 1):
            max_triangles += 2 * len(self.board[step]) - 1
        max_triangles = max_triangles * 2
        return max_triangles

    def calculate_max_sticks(self):
        corner_connections = 6 * 3
        side_connections = (self.side_length - 2) * 4 * 6
        center_connections = (self.peg_number - 6 - (self.side_length - 2) * 6) * 6
        total_connections = corner_connections + side_connections + center_connections
        number_of_sticks = total_connections / 2
        return number_of_sticks

    def get_all_possible_moves(self):

        possible_moves = []

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                for direction in ['D', 'DL', 'DD']:
                    is_valid, _ = self.is_valid_move(row, col, direction)
                    if is_valid:
                        possible_moves.append((row, col, direction))
        return possible_moves

    def get_all_possible_states(self):

        possible_moves = self.get_all_possible_moves()
        possible_states = []

        for move in possible_moves:
            new_state = copy.deepcopy(self)

            # Apply the move to the new state
            row, col, direction = move
            new_state.make_move(row, col, direction)

            # Add the new state to the list
            possible_states.append(new_state)

        return possible_states



def human_move(game: TriggleGame):
    move = input("Enter your move (format: row column direction): ").strip()
    row, col, direction = move.rsplit(' ', 2)
    row, col = ord(row.upper()) - 65, int(col) - 1
    direction = direction.upper()
    game.make_move(row, col, direction)

def computer_move(game: TriggleGame):
    print("Computer is playing...")
    start = time.time()
    row, col, direction = get_best_move(game)
    game.make_move(row, col, direction)

    end = time.time()
    print(f"Computer played in {end - start} seconds")

def evaluate_state(game : TriggleGame):
    return game.score['O'] - game.score['X']


def play(game: TriggleGame):
    while not game.is_game_over():

        try:
            game.display_board()

            if game.current_player == game.human_player:
                human_move(game)
            else:
                computer_move(game)

        except ValueError as ex:
            print(f"{ex}")
        except Exception as e:
            print(f"An error occurred: {e}")

    if game.score['X'] + game.score['O'] == game.max_triangles and game.score['X'] == game.score['O']:
        print("Game over: Draw!")

    if game.score['X'] > game.max_triangles // 2:
        print(f"Game over: Player X has won by majority!")

    if game.score['O'] > game.max_triangles // 2:
        print(f"Game over: Player O has won by majority!")

    game.display_board()

def minimax(game: TriggleGame, depth: int, alpha: float, beta: float):
    if game.is_game_over() or depth == 0:
        return evaluate_state(game)

    #maximizing player
    if game.current_player == "O":
        max_eval = float('-inf')
        for newState in game.get_all_possible_states():
            value = minimax(newState, depth - 1, alpha, beta)
            max_eval = max(max_eval, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for newState in game.get_all_possible_states():
            value = minimax(newState, depth - 1, alpha, beta)
            min_eval = min(min_eval, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(game: TriggleGame):
    best_move = None
    best_value = float('-inf') if game.current_player == 'O' else float('inf')
    alpha = float('-inf')
    beta = float('inf')

    for move in game.get_all_possible_moves():
        row, col, direction = move
        if not game.is_valid_move(row, col, direction):
            print(f"Skipping invalid move: Row {row}, Col {col}, Direction {direction}")
            continue

        game_copy = copy.deepcopy(game)
        newState = game_copy.make_move(row, col, direction)

        if newState is None:
            continue

        value = minimax(newState, depth=2, alpha=alpha, beta=beta)
        if game.current_player == 'O':
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, value)
        else:
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, value)

        if beta <= alpha:
            break
    return best_move

def setup_game():
    n = int(input("Enter the side length of the hexagonal board (4-8): "))
    if n < 4 or n > 8:
        raise ValueError("Side length must be between 4 and 8.")

    first_player = input("Who do you wanna play as? (X/O): ").strip().upper()
    if first_player not in ['X', 'O']:
        raise ValueError("Invalid choice. Choose 'X' or 'O'.")

    game = TriggleGame(n, first_player)

    return game

def main():
    try:
        game = setup_game()
        play(game)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
