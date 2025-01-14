class Board:
    def __init__(self, side_length):
        self.side_length = side_length
        self.board = self.initialize_board(side_length)
        self.sticks = set()
        self.triangles = {}

    def initialize_board(self, side_length):
        return (
            [[None] * (side_length + i) for i in range(side_length)] +
            [[None] * (2 * side_length - i - 1) for i in range(1, side_length)]
        )

    def add_stick(self, start, end):
        self.sticks.add((start, end))

    def is_stick_placed(self, start, end):
        return (start, end) in self.sticks or (end, start) in self.sticks

    def get_triangle_owner(self, corners):
        triangle_key = tuple(sorted(corners))
        return self.triangles.get(triangle_key, None)

    def check_and_capture_triangles(self, current_player):
        def is_triangle_completed(corners):
            return all(
                self.is_stick_placed(corners[i], corners[(i + 1) % len(corners)])
                for i in range(len(corners))
            )

        # Traverse the board and capture triangles
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                potential_triangles = self.get_potential_triangles(row, col)
                for corners in potential_triangles:
                    if is_triangle_completed(corners):
                        triangle_key = tuple(sorted(corners))
                        if triangle_key not in self.triangles:
                            self.triangles[triangle_key] = current_player

    def get_potential_triangles(self, row, col):
        # Define potential triangles based on the location
        if row < self.side_length - 1:
            return [
                [(row, col), (row, col + 1), (row + 1, col + 1)],  # Downward
                [(row, col), (row + 1, col), (row + 1, col + 1)]   # Upward
            ]
        else:
            return [
                [(row, col), (row, col + 1), (row + 1, col)],      # Downward
                [(row, col), (row + 1, col - 1), (row + 1, col)]   # Upward
            ]


class Display:
    @staticmethod
    def render_board(board):
        n = board.side_length
        max_width = 2 * n - 1
        column_numbers = '     '.join(f"{i}" for i in range(1, max_width + 1))

        print(f"   {'   ' * (n - 1)}{column_numbers}")
        for i, row in enumerate(board.board):
            offset = abs(n - 1 - i)
            peg_line = []
            for j in range(len(row)):
                peg_line.append("●")
                peg_line.append("-----" if board.is_stick_placed((i, j), (i, j + 1)) else "     ")
            print(f"{chr(65 + i)} {'   ' * offset}{''.join(peg_line)}")
        print(f"   {'   ' * (n - 1)}{column_numbers}")

    @staticmethod
    def get_player_input():
        move = input("Enter your move (format: row column direction): ").strip()
        row, col, direction = move.rsplit(' ', 2)
        return ord(row.upper()) - 65, int(col) - 1, direction.upper()


class TriggleGame:
    def __init__(self, side_length, first_player):
        self.board = Board(side_length)
        self.current_player = first_player
        self.max_triangles = self.calculate_max_triangles()

    def play_turn(self, move):
        row, col, direction = move
        # Validate and place stick
        is_valid, error = self.validate_move(row, col, direction)
        if not is_valid:
            raise ValueError(error)

        self.make_move(row, col, direction)
        self.board.check_and_capture_triangles(self.current_player)
        self.switch_player()

    def validate_move(self, row, col, direction):
        # Add validation logic for moves
        return True, None

    def make_move(self, row, col, direction):
        # Add move-making logic
        pass

    def switch_player(self):
        self.current_player = 'X' if self.current_player == 'O' else 'O'

    def calculate_max_triangles(self):
        max_triangles = 0
        for step in range(self.board.side_length - 1):
            max_triangles += 2 * len(self.board.board[step]) - 1
        return max_triangles * 2


def main():
    n = int(input("Enter the side length of the hexagonal board (4-8): "))
    first_player = input("Who will play first? (X/O): ").strip().upper()

    game = TriggleGame(n, first_player)

    while True:
        Display.render_board(game.board)
        print(f"{game.current_player}'s turn.")

        try:
            move = Display.get_player_input()
            game.play_turn(move)
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
