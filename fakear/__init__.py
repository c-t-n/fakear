import os
import yaml
from shutil import rmtree

from subprocess import run
from voluptuous import Schema, Required, Optional, Exclusive, Match, ALLOW_EXTRA
from fakear import templates

class FakearMultipleSourceException(Exception):
    pass

class Fakear(object):

    validate_file = Schema({
        Match(r'^[A-Za-z0-9]+$'): list
    }, extra=ALLOW_EXTRA, required=True)

    validate_args = Schema([{
            Optional('args'): list,
            Required('return_code'): int,
            Exclusive('output', 'output'): str,
            Exclusive('output_file', 'output'): str
        }] )

    def __init__(self, cfg=None, rawdata=None):
        self.__fakedcmds = {}
        self.__enabled = False
        self.__faked_path="/tmp/fakear/binaries"
        self.__shell = self.__search_for_interpreter()

        if all([not cfg, not rawdata]): return
        if all([cfg, rawdata]):
            raise FakearMultipleSourceException()
        if cfg:
            with open(cfg) as d:
                rawdata = d.read()
        
        data = self.validate_file(yaml.load(rawdata))
        for cmd, args in data.items():
            self.__fakedcmds[cmd] = self.validate_args(args)


    @property
    def commands(self):
        return self.__fakedcmds


    @property
    def faked_path(self):
        return self.__faked_path

    @property
    def shell(self):
        return self.__shell


    def __search_for_interpreter(self):
        p = run(["which", "bash"], capture_output=True)
        return p.stdout.decode().replace("\n", "")

    def __write_binaries(self):
        for command, subcmds in self.__fakedcmds.items():
            subs = sorted(subcmds, key=lambda a: len(a.get('args', [])), reverse=True)
            filepath = os.path.join(self.faked_path, command)
            binary = []

            # Case for no subcommand
            if not subs:
                binary.append(templates.sh_default)    
            else:
                for sub in subs:
                    sub_extract = sub.get('args', [])
                    zipped_subs = list(zip(range(1, len(sub_extract) + 1), sub_extract))

                    sub_args = {
                        'length': len(zipped_subs),
                        'arg_line': " && ".join([ f"'${a[0]}' = '{a[1]}'" for a in zipped_subs ])
                    }

                    if not binary:
                        if sub_args['arg_line']:
                            binary.append(templates.sh_if.format(**sub_args))
                        if "output_file" in sub.keys():
                            binary.append(templates.sh_output_file.format(**sub))
                        else:
                            binary.append(templates.sh_output.format(**sub))
                    else:
                        if sub_args['arg_line']:
                            binary.append(templates.sh_elif.format(**sub_args))
                        else:
                            binary.append(templates.sh_else)

                        if "output_file" in sub.keys():
                            binary.append(templates.sh_output_file.format(**sub))
                        else:
                            binary.append(templates.sh_output.format(**sub))                        
                        
            if len(binary) > 1:
                binary.append(templates.sh_fi)

            with open(filepath, 'w+') as f:
                f.writelines(templates.sh_header.format(shell_path=self.__shell))
                f.writelines(binary)

            os.chmod(filepath, 0o777)


    def __enable_path(self):
        if self.__faked_path not in os.environ["PATH"]:
            os.environ["PATH"] = f'{self.__faked_path}:{os.environ["PATH"]}'
            

    def __disable_path(self):
        if self.__faked_path in os.environ["PATH"]:
            path = ":".join([
                p for p in os.environ["PATH"].split(":")
                    if self.__faked_path not in p
            ])
            os.environ['PATH'] = path

    def set_faked_path(self, path):
        if self.__enabled:
            self.__faked_path = path
            

    def enable(self):
        if not os.path.exists(self.__faked_path):
            os.makedirs(self.__faked_path)
        self.__write_binaries()
        self.__enable_path()
        self.__enabled = True

    def disable(self):
        if os.path.exists(self.__faked_path):
            rmtree(self.__faked_path)
        self.__disable_path()
        self.__enabled = False        
