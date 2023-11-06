import sys


class NumberLinkSolver:
    def __init__(self, filename):
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                self.rows, self.cols = map(int, lines[0].strip().split(","))

                # Inicializa el tablero con celdas vacías
                self.board = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
                self.original_numbers = (
                    {}
                )  # Diccionario para almacenar los números originales
                # Procesa las ubicaciones de las parejas
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

        self.connections = []  # Lista para almacenar las conexiones de los números

    def print_board(self):
        horizontal_line = "+---" * self.cols + "+"

        for i in range(self.rows):
            print(horizontal_line)
            for j in range(self.cols):
                print(f"| {self.board[i][j]} ", end="")
            print("|")
        print(horizontal_line)

    def play(self):
        while True:
            self.print_board()
            try:
                user_input = input(
                    "Ingresa las coordenadas (fila1, columna1, fila2, columna2,...) o 'q' para salir: "
                ).strip()

                if user_input.lower() == "q":
                    break  # Salir del bucle si se ingresa 'q'

                coordinates = list(map(int, user_input.split()))

                if len(coordinates) % 2 != 0:
                    print("Debes ingresar un número par de coordenadas.")
                    continue
                number_to_connect = input("Ingresa el número que deseas conectar: ")
                for i in range(0, len(coordinates), 2):
                    row1, col1 = coordinates[i], coordinates[i + 1]
                    if i + 2 < len(coordinates):
                        row2, col2 = coordinates[i + 2], coordinates[i + 3]
                        if self.is_valid_move(row1, col1, row2, col2):
                            self.connect_cells(
                                row1, col1, row2, col2, number_to_connect
                            )
                        else:
                            print(
                                "Movimiento inválido. Asegúrate de que las celdas sean adyacentes y estén vacías."
                            )
                            break
                if self.is_game_over():
                    print("¡Has ganado! ¡Todas las celdas están conectadas!")
                    print("Este es tu tablero final:")
                    self.print_board()
                    break
            except ValueError:
                if input("¿Deseas salir del juego? (S/N): ").strip().lower() == "s":
                    break
                else:
                    continue

    def is_valid_move(self, row1, col1, row2, col2):
        # Verifica si el movimiento es válido (celdas adyacentes y vacías)
        if (
            1 <= row1 <= self.rows
            and 1 <= col1 <= self.cols
            and 1 <= row2 <= self.rows
            and 1 <= col2 <= self.cols
            and (
                abs(row1 - row2) == 1
                and col1 == col2
                or abs(col1 - col2) == 1
                and row1 == row2
            )
            and self.board[row2 - 1][col2 - 1] == " "
            and self.board[row1 - 1][col1 - 1] == " "
            and ((row1, col1), (row2, col2)) not in self.connections
            and ((row2, col2), (row1, col1)) not in self.connections
            and ((row1, col1), (row2, col2)) not in self.original_numbers.keys()
            and ((row2, col2), (row1, col1)) not in self.original_numbers.keys()
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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python tu_script.py archivo.txt")
    else:
        input_file = sys.argv[1]
        solver = NumberLinkSolver(input_file)
        if solver.rows > 0 and solver.cols > 0 and solver.board is not None:
            print("Tablero de entrada:")
            solver.play()
        else:
            print(
                "No se pudo cargar el tablero inicial. Verifica el archivo de entrada."
            )
