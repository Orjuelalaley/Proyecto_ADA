import sys
from collections import deque


class NumberLinkSolver:
    def __init__(self, filename):
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                self.rows, self.cols = map(int, lines[0].strip().split(","))

                # Inicializa el tablero con celdas vacías
                self.board = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
                self.original_numbers = {}  # Corrección: Inicializar como diccionario vacío

                # Procesa las ubicaciones de las parejas
                for line in lines[1:]:
                    pair_data = list(map(int, line.strip().split(",")))
                    if len(pair_data) == 3:
                        row, col, value = pair_data
                        # Almacena la posición como clave y el valor como valor en el diccionario
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
            try:
                user_input = input(
                    "Ingresa las coordenadas (fila, columna) o 'q' para salir: "
                ).strip()

                if user_input.lower() == "q":
                    break  # Salir del bucle si se ingresa 'q'

                coordinates = list(map(int, user_input.split()))

                if len(coordinates) == 2:  # Si se ingresa solo una coordenada
                    row1, col1 = coordinates
                    number_to_connect = input("Ingresa el número que deseas conectar: ")
                    self.connect_single_cell(row1, col1, number_to_connect)
                    if self.is_game_over():
                        print("¡Has ganado! ¡Todas las celdas están conectadas!")
                        print("Este es tu tablero final:")
                        self.print_board()
                        break
                    else:
                        self.print_board()
                elif len(coordinates) % 2 != 0:
                    print("Debes ingresar un número par de coordenadas.")
                    continue
                else:
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
                    else:
                        self.print_board()

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

    def connect_single_cell(self, row, col, number_to_connect):
        # Conecta una sola celda en el tablero con un número específico
        self.board[row - 1][col - 1] = number_to_connect

    def connect_cells(self, row1, col1, row2, col2, number_to_connect):
        # Conecta las celdas en el tablero y registra la conexión
        self.board[row1 - 1][col1 - 1] = number_to_connect
        self.board[row2 - 1][col2 - 1] = number_to_connect
        self.connections.append(((row1, col1), (row2, col2)))

    def is_game_over(self):
        # Verifica si se ha completado el juego
        for row in self.board:
            if " " in row or "X" in row:  # Se añade "X" a las condiciones de finalización del juego
                return False
        return True

    def find_number_coordinates(self, number):
        coordinates = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == str(number):
                    coordinates.append((i+1, j+1))
        return coordinates

    def group_numbers(self):
        unique_numbers = set()
        for pair in self.original_numbers:
            value = self.original_numbers[pair]
            unique_numbers.add(value)

        grouped_numbers = {}
        for number in unique_numbers:
            grouped_numbers[number] = self.find_number_coordinates(number)
        return grouped_numbers

    def solve_by_heuristic(self):
        grouped_numbers = self.group_numbers()

        # Diccionario para almacenar las rutas más cortas por número
        shortest_paths = {number: {} for number in grouped_numbers.keys()}

        for number, group in grouped_numbers.items():
            if len(group) >= 2:
                for i in range(len(group)):
                    for j in range(i + 1, len(group)):
                        start = group[i]
                        end = group[j]
                        print(f"Buscando camino entre {start} y {end} para el número {number}...")
                        found_paths = self.find_all_paths(start, end)

                        if found_paths:
                            shortest_path = min(found_paths, key=len)
                            path_length = len(shortest_path) - 1
                            if end not in shortest_paths[number] or path_length < len(shortest_paths[number][end]):
                                shortest_paths[number][end] = shortest_path

        # Actualizar el tablero con las rutas más cortas encontradas
        for number, paths in shortest_paths.items():
            for path in paths.values():
                for coord in path[1:-1]:
                    row, col = coord
                    if self.board[row - 1][col - 1] == " ":
                        self.board[row - 1][col - 1] = str(number)

        print("Tablero después de la resolución:")
        self.print_board()

    def find_all_paths(self, start, end):
        queue = deque()
        queue.append((start, [start]))

        all_paths = []
        visited = set()
        visited.add(start)

        while queue:
            current, path = queue.popleft()
            if current == end:
                all_paths.append(path)
            row, col = current

            # Direcciones posibles
            possible_moves = [
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1)
            ]

            for move in possible_moves:
                if (
                        0 <= move[0] < self.rows and
                        0 <= move[1] < self.cols and
                        (self.board[move[0]][move[1]] == " " or self.board[move[0]][move[1]] == str(end)) and
                        move not in path and move not in visited
                ):
                    queue.append((move, path + [move]))
                    visited.add(move)
        return all_paths


def main():
    print("Bienvenido al juego NumberLink")
    print("¿Quieres resolverlo tú mismo? (s/n/q)")

    # Tomar la decisión del usuario
    decision_usuario = input().strip().lower()
    if decision_usuario not in ["s", "n", "q"]:
        print(
            "Por favor, ingresa 's' para resolverlo tú mismo, 'n' para dejar que la máquina lo haga, o 'q' para salir.")
        return

    if decision_usuario == "q":
        print("Saliendo del juego...")
        return

    # Leer el archivo de entrada
    if len(sys.argv) != 2:
        print("Uso: python tu_script.py archivo.txt")
        return
    input_file = sys.argv[1]

    # Crear el solucionador
    solver = NumberLinkSolver(input_file)

    if solver.rows <= 0 or solver.cols <= 0 or solver.board is None:
        print("No se pudo cargar el tablero inicial. Verifica el archivo de entrada.")
        return

    print("Tablero de entrada:")
    solver.print_board()

    # Jugar o resolver automáticamente según la elección del usuario
    if decision_usuario == "s":
        solver.play()  # Juego manual
    elif decision_usuario == "n":
        solver.solve_by_heuristic()  # Resolución automática


if __name__ == "__main__":
    main()
