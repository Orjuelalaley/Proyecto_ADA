class NumberLinkSolver:
    def __init__(self):
        self.board = None
        self.rows = 0
        self.cols = 0

    def read_input_file(self, filename):
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                self.rows, self.cols = map(int, lines[0].strip().split(","))

                # Inicializa el tablero con celdas vacías
                self.board = [[" " for _ in range(self.cols)] for _ in range(self.rows)]

                # Procesa las ubicaciones de las parejas
                for line in lines[1:]:
                    pair_data = list(map(int, line.strip().split(",")))
                    row, col, value = pair_data
                    self.board[row - 1][col - 1] = str(value)

            return True
        except Exception as e:
            print(f"Error al leer el archivo de entrada: {e}")
            return False

    def print_board(self):
        horizontal_line = "+---" * self.cols + "+"

        for i in range(self.rows):
            print(horizontal_line)
            for j in range(self.cols):
                print(f"| {self.board[i][j]} ", end="")
            print("|")
        print(horizontal_line)

    def solve_game(self):
        def dfs(row, col, value, visited):
            visited.add((row, col))

            # Búsqueda hacia arriba
            if (
                row > 0
                and self.board[row - 1][col] == value
                and (row - 1, col) not in visited
            ):
                self.connect_cells(row, col, row - 1, col)
                dfs(row - 1, col, value, visited)

            # Búsqueda hacia abajo
            if (
                row < self.rows - 1
                and self.board[row + 1][col] == value
                and (row + 1, col) not in visited
            ):
                self.connect_cells(row, col, row + 1, col)
                dfs(row + 1, col, value, visited)

            # Búsqueda hacia la izquierda
            if (
                col > 0
                and self.board[row][col - 1] == value
                and (row, col - 1) not in visited
            ):
                self.connect_cells(row, col, row, col - 1)
                dfs(row, col - 1, value, visited)

            # Búsqueda hacia la derecha
            if (
                col < self.cols - 1
                and self.board[row][col + 1] == value
                and (row, col + 1) not in visited
            ):
                self.connect_cells(row, col, row, col + 1)
                dfs(row, col + 1, value, visited)

        for row in range(self.rows):
            for col in range(self.cols):
                value = self.board[row][col]
                if value != " ":
                    visited = set()
                    dfs(row, col, value, visited)

        print("Tablero resuelto:")
        self.print_board()


if __name__ == "__main__":
    solver = NumberLinkSolver()
    input_file = "inputfile.txt"

    if solver.read_input_file(input_file):
        print("Tablero de entrada:")
        solver.print_board()

        # Llama a tu función para resolver el juego
        solver.solve_game()
