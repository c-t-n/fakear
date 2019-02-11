# Fakear

A tool that mocks shell commands and binaries used for Python program testing

[![CircleCI](https://circleci.com/gh/c-t-n/fakear/tree/master.svg?style=svg)](https://circleci.com/gh/c-t-n/fakear/tree/master)

# Purpose


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