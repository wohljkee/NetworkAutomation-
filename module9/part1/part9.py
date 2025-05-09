import pylint

args = ['--disable=missing-class-docstring,missing-function-docstring,too-few-public-methods',
        'modul7/part2/configre_ospf.py']
pylint.run_pylint(args)