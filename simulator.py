class Simulator:
    def __init__(self):
        self.registers = [0] * 16  # 16 registros de 8 bits
        self.memory = [0] * 256  # RAM con 256 direcciones de 8 bits
        self.pc = 0  # Contador de programa
        self.flags = {"EQ": False, "NEQ": False}  # Flags para comparaciones
        self.running = True  # Estado del simulador

    def load_program(self, file_path):
        """
        Carga un programa desde un archivo (ruta especificada) en la memoria.
        """
        try:
            with open(file_path, 'r') as file:
                for i, line in enumerate(file):
                    if line.strip():  # Ignorar líneas vacías
                        self.memory[i] = int(line.strip(), 2)  # Convierte binario a entero
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo '{file_path}' no se encontró.")
        except ValueError as e:
            raise ValueError(f"Error al procesar una línea del archivo: {e}")

    def fetch(self):
        """
        Recupera la instrucción actual desde la memoria.
        """
        instruction = self.memory[self.pc]
        self.pc += 1
        return instruction

    def decode_and_execute(self, instruction):
        """
        Decodifica y ejecuta la instrucción actual.
        """
        opcode = (instruction >> 11) & 0b11111  # Primeros 5 bits
        reg1 = (instruction >> 7) & 0b1111  # Siguiente 4 bits
        reg2 = (instruction >> 3) & 0b1111  # Siguiente 4 bits
        operand = instruction & 0b111  # Últimos 3 bits o dirección/valor inmediato

        if opcode == 0b00010:  # ADD
            self.registers[reg1] = (self.registers[reg2] + self.registers[operand]) & 0xFF
        elif opcode == 0b01111:  # HLT
            self.running = False
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    def run(self):
        """
        Ejecuta el programa cargado en la memoria.
        """
        print("Simulador iniciado...")
        while self.running:
            instruction = self.fetch()
            self.decode_and_execute(instruction)
            self.print_state()

    def print_state(self):
        """
        Imprime el estado actual de los registros y la memoria.
        """
        print(f"PC: {self.pc}")
        print("Registros:", self.registers)
        print("Memoria (primeros 16):", self.memory[:16])
        print("-" * 30)