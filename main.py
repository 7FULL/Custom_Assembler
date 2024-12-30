from assembler import assemble
from simulator import Simulator


# from schematic import make_schematic


def main():
    program = 'prueba_3'

    as_filename = f'code/assembly/{program}.as'
    mc_filename = f'code/machine/{program}.mc'
    schem_filename = f'schems/{program}.schem'

    assemble(as_filename, mc_filename)
    # make_schematic(mc_filename, schem_filename)

    simulator = Simulator()
    simulator.load_program(mc_filename)
    simulator.test_registers()
    simulator.run()


if __name__ == '__main__':
    main()
