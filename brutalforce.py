import sys


class NumberLinkSolver:
    def __init__(self, filename):
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                self.rows, self.cols = map(int, lines[0].strip().split(","))
                self.board = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
                self.original_numbers = {}
                for line in lines[1:]:
                    pair_data = list(map(int, line.strip().split(",")))
                    if len(pair_data) == 3:
                        row, col, value = pair_data
                        self.original_numbers[(row, col)] = value
                        self.board[row - 1][col - 1] = str(value)
                    else:
                        row1, col1, row2, col2 = pair_data
                        self.board[row1 - 1][col1 - 1] = " "
                        self.board[row2 - 1][col2 - 1] = " "
        except Exception as e:
            print(f"Error al leer el archivo de entrada: {e}")
            self.rows = 0
            self.cols = 0
            self.board = None

        self.connections = []

    def print_board(self):
        horizontal_line = "+---" * self.cols + "+"
        for i in range(self.rows):
            print(horizontal_line)
            for j in range(self.cols):
                print(f"| {self.board[i][j]} ", end="")
            print("|")
        print(horizontal_line)

    def is_valid_move(self, row1, col1, row2, col2):
        # Verifica si el movimiento es válido
        if (
            1 <= row1 <= self.rows
            and 1 <= col1 <= self.cols
            and 1 <= row2 <= self.rows
            and 1 <= col2 <= self.cols
            and (
                (abs(row1 - row2) == 1 and col1 == col2)
                or (abs(col1 - col2) == 1 and row1 == row2)
            )
            and self.board[row2 - 1][col2 - 1] == " "
            and self.board[row1 - 1][col1 - 1] == " "
            and ((row1, col1), (row2, col2)) not in self.connections
            and ((row2, col2), (row1, col1)) not in self.connections
        ):
            return True
        return False

    def connect_cells(self, row1, col1, row2, col2, number_to_connect):
        # Conecta las celdas en el tablero y registra la conexión
        self.board[row1 - 1][col1 - 1] = number_to_connect
        self.board[row2 - 1][col2 - 1] = number_to_connect
        self.connections.append(((row1, col1), (row2, col2)))

    def is_game_over(self):
        # Verifica si se ha completado el juego
        for row in self.board:
            if " " in row:
                return False
        return True

    def heuristic_solver(self):
        numbers_in_order = self.sort_numbers_by_heuristic()
        for number in numbers_in_order:
            if not self.solve_for_number(number):
                return False
        return self.is_game_over()

    def sort_numbers_by_heuristic(self):
        return sorted(self.original_numbers.values(), key=self.distance_between_pairs)

    def distance_between_pairs(self, number):
        positions = [pos for pos, val in self.original_numbers.items() if val == number]
        if len(positions) < 2:
            return float("inf")
        (x1, y1), (x2, y2) = positions
        return abs(x1 - x2) + abs(y1 - y2)

    def solve_for_number(self, number):
        # Encontrar las posiciones de inicio y fin para el número dado
        positions = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if self.board[r][c] == str(number)
        ]
        if len(positions) != 2:
            return False  # No se puede resolver si no hay exactamente dos puntos para conectar

        start, end = positions
        return self.find_path(start, end, number)

    def find_path(self, start, end, number):
        # Implementar la búsqueda de un camino desde el inicio hasta el final
        # Esto puede ser una búsqueda simple primero en anchura o profundidad con heurísticas
        # Por ejemplo, prefiriendo movimientos que se acerquen al punto final
        # ...

        # Marcador para evitar revisitar celdas
        visited = set()

        # Función recursiva para buscar el camino
        def search(current_pos):
            if current_pos == end:
                return True
            if current_pos in visited:
                return False

            visited.add(current_pos)
            r, c = current_pos

            # Lista de posibles movimientos: arriba, abajo, izquierda, derecha
            moves = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
            for next_pos in moves:
                next_r, next_c = next_pos
                if (
                    0 <= next_r < self.rows
                    and 0 <= next_c < self.cols
                    and self.board[next_r][next_c] in [" ", str(number)]
                ):
                    # Realizar el movimiento
                    self.board[next_r][next_c] = str(number)
                    if search(next_pos):
                        return True
                    # Deshacer el movimiento si no conduce a una solución
                    self.board[next_r][next_c] = " " if next_pos != end else str(number)

            visited.remove(current_pos)
            return False

        return search(start)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python tu_script.py archivo.txt")
    else:
        input_file = sys.argv[1]
        solver = NumberLinkSolver(input_file)
        if solver.rows > 0 and solver.cols > 0 and solver.board is not None:
            print("Tablero de entrada:")
            solver.print_board()
            if solver.heuristic_solver():
                print("Solución encontrada:")
                solver.print_board()
            else:
                print("No se encontró una solución.")
        else:
            print(
                "No se pudo cargar el tablero inicial. Verifica el archivo de entrada."
            )
