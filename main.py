from assembler import assemble
# from schematic import make_schematic


def main():
    program = 'prueba_2'

    as_filename = f'code/assembly/{program}.as'
    mc_filename = f'code/machine/{program}.mc'
    schem_filename = f'schems/{program}.schem'

    assemble(as_filename, mc_filename)
    # make_schematic(mc_filename, schem_filename)


if __name__ == '__main__':
    main()
