import sys
import random

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] < self.rank[rootY]:
                rootX, rootY = rootY, rootX
            self.parent[rootY] = rootX
            if self.rank[rootX] == self.rank[rootY]:
                self.rank[rootX] += 1

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

    def play(self):
        while True:
            self.print_board()
            try:
                user_input = input(
                    "Ingresa las coordenadas (fila1, columna1, fila2, columna2,...) o 'q' para salir: "
                ).strip()

                if user_input.lower() == "q":
                    break

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
                            self.connect_cells(row1, col1, row2, col2, number_to_connect)
                        else:
                            print("Movimiento inválido. Asegúrate de que las celdas sean adyacentes y estén vacías.")
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
        self.board[row1 - 1][col1 - 1] = number_to_connect
        self.board[row2 - 1][col2 - 1] = number_to_connect
        self.connections.append(((row1, col1), (row2, col2)))

    def is_game_over(self):
        for row in self.board:
            if " " in row:
                return False
        return True

    def get_valid_neighbors(self, row, col):
        neighbors = []
        for drow, dcol in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nrow, ncol = row + drow, col + dcol
            if 0 <= nrow < self.rows and 0 <= ncol < self.cols and self.board[nrow][ncol] == " ":
                neighbors.append((nrow, ncol))
        return neighbors

    def generate_path(self):
        uf = UnionFind(self.rows * self.cols)

        while True:
            empty_cells = [(r, c) for r in range(self.rows) for c in range(self.cols) if self.board[r][c] == " "]
            if not empty_cells:
                print("No hay más celdas vacías.")
                break

            while empty_cells:
                cell1 = random.choice(empty_cells)
                neighbors = self.get_valid_neighbors(*cell1)
                if neighbors:
                    break
                else:
                    print(f"No se encontraron vecinos válidos para la celda {cell1}.")
                    empty_cells.remove(cell1)  # Eliminar la celda sin vecinos válidos

            if not neighbors:  # Si no se encontraron vecinos para ninguna celda vacía
                break

            # Encontrar un número para conectar
            number_to_connect = self.find_number_to_connect(cell1)

            cell2 = random.choice(neighbors)
            uf.union(cell1[0] * self.cols + cell1[1], cell2[0] * self.cols + cell2[1])
            self.connect_cells(cell1[0]+1, cell1[1]+1, cell2[0]+1, cell2[1]+1, number_to_connect)

            while True:
                new_neighbors = [n for n in self.get_valid_neighbors(*cell2) if uf.find(n[0] * self.cols + n[1]) != uf.find(cell2[0] * self.cols + cell2[1])]
                if not new_neighbors:
                    break

                cell1, cell2 = cell2, random.choice(new_neighbors)
                uf.union(cell1[0] * self.cols + cell1[1], cell2[0] * self.cols + cell2[1])
                self.connect_cells(cell1[0]+1, cell1[1]+1, cell2[0]+1, cell2[1]+1, number_to_connect)

        print("Generación de caminos completada.")

    def find_number_to_connect(self, cell):
        # Buscar en la celda actual
        if self.board[cell[0]][cell[1]].isdigit():
            return self.board[cell[0]][cell[1]]
        
        # Buscar en las celdas vecinas
        neighbors = self.get_valid_neighbors(*cell)
        for n in neighbors:
            if self.board[n[0]][n[1]].isdigit():
                return self.board[n[0]][n[1]]
        
        return "#"  # Por defecto, si no se encuentra un número

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python tu_script.py archivo.txt")
    else:
        input_file = sys.argv[1]
        solver = NumberLinkSolver(input_file)
        if solver.rows > 0 and solver.cols > 0 and solver.board is not None:
            print("Tablero de entrada:")
            solver.print_board()
            choice = input("Elige: (1) Jugar manualmente (2) Resolver automáticamente: ")
            if choice == "2":
                solver.generate_path()
                solver.print_board()
            else:
                solver.play()
        else:
            print("No se pudo cargar el tablero inicial. Verifica el archivo de entrada.")
