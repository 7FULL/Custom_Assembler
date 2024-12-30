from assembler import assemble
from simulator import Simulator


def main():
    program = 'prueba_3'

    as_filename = f'code/assembly/{program}.as'
    mc_filename = f'code/machine/{program}.mc'

    assemble(as_filename, mc_filename)

    simulator = Simulator()
    simulator.load_program(mc_filename)
    simulator.test_registers()
    simulator.run()


if __name__ == '__main__':
    main()
