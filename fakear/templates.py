"""
Template variables for shell script generation

Do not modify unless you know what you're doing
"""


SH_HEADER = """#!{shell_path}

# This program is automatically generated with the python Fakear library
# This program should temporary simulate the behaviour of the real program
# and it's for testing purpose only.
#
# (c) 2019 Franck Lourme

"""

SH_IF = 'if [[ "$#" -eq {length} && {arg_line} ]]; then'
SH_ELIF = 'elif [[ "$#" -eq {length} && {arg_line} ]]; then'
SH_ELSE = 'else'
SH_FI = 'fi'

SH_OUTPUT = """
    echo '{output}'
    exit {return_code}
"""
SH_OUTPUT_FILE = """
    cat '{output_file}'
    exit {return_code}
"""

SH_DEFAULT = 'echo "I am a fake binary !"'
