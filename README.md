# Fakear

A tool that mocks shell commands and binaries used for Python program testing

[![CircleCI](https://circleci.com/gh/c-t-n/fakear/tree/master.svg?style=svg)](https://circleci.com/gh/c-t-n/fakear/tree/master)

# Purpose

This tool acts like a program faker, that takes yaml files or raw dict data as input and create fake binaries from them.

Binaries simulates an output with given arguments, in the context of your Python program.

This tool should help you testing your programs that need specific output from other binaries you run throught the `subprocess` module.

# Quick Start

This is a mock of the `ls` command.

In our mock, `ls` should respond to the args `cheeses`  and `-1 cheeses`, which have 2 different outputs. One with a string, the other with the content of another file.

```yaml
ls:
    - args:
        - cheeses
      return_code: 0
      output: cheddar   gouda   abondance   emmenthal   raclette
    - args:
        - -1
        - cheeses
      return_code: 0
      output_file: cheeses.txt
```

For this command, `cheeses.txt` contains this:
```sh
$> cat cheeses.txt
cheddar
gouda
abondance
emmenthal
raclette
$>
```

In our python program now, we can create a Fakear instance and enable it to mock the program call when it's invoked with the subprocess module

```python
>>> from subprocess import run
>>> from fakear import Fakear
>>> fakear = Fakear(cfg="fake_ls.yaml")
>>> p = run (["ls", "cheeses"])
ls: cheeses: No such file or directory
>>> p.returncode
1
>>> fakear.enable()
>>> p = run (["ls", "cheeses"])
cheddar   gouda   abondance   emmenthal   raclette
>>> p.returncode
0
>>> p = run (["ls", "-1", "cheeses"])
cheddar
gouda
abondance
emmenthal
raclette
>>> p.returncode
0
>>> fakear.disable()
>>> p = run (["ls", "cheeses"])
ls: cheeses: No such file or directory
>>>
```

# Documentation

## YAML Files

Every program mock should start with the program name as a key. Then you can describe multiple behaviours for a given set of arguments.

```yaml
__command_name__ :
  - args:
    - first_arg
    - sec_arg
    return_code: 0
    output: This is an example of fake command
  - return_code: -1
    output: This is a fake program, please give the correct arguments
```

You can use those options to customise your fake program:

  - **args (Optionna̦l)** : a list of positionnal arguments that invoke this fake output
  - **return_code** : the return code when the program exits
  - **output**: The raw data to output when you invoke the program with these args
  - **output_file**: The path of a file containing the output to show

Notice that if you mention no args to your list, this command overrides the default behaviour of your fake program.

Also, you can't have **output** and **output_file** keys in the same command. It should throw an error.


## API


