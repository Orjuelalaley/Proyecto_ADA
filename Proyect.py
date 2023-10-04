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

    def solve(self):
        # Implementa tu algoritmo de resolución aquí
        pass


if __name__ == "__main__":
    solver = NumberLinkSolver()
    input_file = "inputfile.txt"

    if solver.read_input_file(input_file):
        print("Tablero de entrada:")
        solver.print_board()
        solver.solve()
