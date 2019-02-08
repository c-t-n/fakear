sh_header = """#!{shell_path}

# This program is automatically generated with the python Fakear library
# This program should temporary simulate the behaviour of the real program
# and it's for testing purpose only.
#
# (c) 2019 Franck Lourme

"""

sh_if = 'if [[ "$#" -eq {length} && {arg_line} ]]; then'
sh_elif = 'elif [[ "$#" -eq {length} && {arg_line} ]]; then'
sh_else = 'else'
sh_fi  = 'fi'

sh_output = """
    echo '{output}'
    exit {return_code}
"""
sh_output_file = """
    cat '{output_file}'
    exit {return_code}
"""

sh_default = 'echo "I am a fake binary !"'