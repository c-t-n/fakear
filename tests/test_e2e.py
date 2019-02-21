import pytest
import yaml
import os
import sys

if sys.version_info[0] < 3:
    from .run_py27 import run
else:
    from .run_py3 import run

from subprocess import PIPE
from fakear import Fakear
from voluptuous import Error as VoluptuousError


class TestEndToEndFakear(object):
    def test_enable_basic_cmd_default_only(self):
        fe = Fakear(cfg="tests/cfgs/simple_cmd.yml")
        fe.enable()
        assert fe.faked_path in os.environ["PATH"]
        assert os.path.exists(fe.faked_path)
        assert os.path.exists(fe.faked_path + "/echo")
       
       
        p = run(["echo"], stdout=PIPE, stderr=PIPE)
        assert p.stderr.decode() == ""
        assert p.stdout.decode() == "I am a fake binary !\n"
        assert p.returncode == 0

    def test_enable_basic_cmd_default_overwritten(self):
        fe = Fakear(cfg="tests/cfgs/simple_cmd_default.yml")
        fe.enable()
        assert fe.faked_path in os.environ["PATH"]
        assert os.path.exists(fe.faked_path)
        assert os.path.exists(fe.faked_path + "/echo")
       
       
        p = run(["echo"], stdout=PIPE, stderr=PIPE)
        assert p.stderr.decode() == ""
        assert p.stdout.decode() == "Hello World\n"
        assert p.returncode == 0

    def test_enable_basic_cmd_mult_args(self):
        fe = Fakear(cfg="tests/cfgs/multiple_cmd_mult_args.yml")
        fe.enable()
        assert fe.faked_path in os.environ["PATH"]
        assert os.path.exists(fe.faked_path)
        assert os.path.exists(fe.faked_path + "/echo")
        assert os.path.exists(fe.faked_path + "/ls")
       
       
        p = run(["ls", "omelette", "du", "fromage"], stdout=PIPE, stderr=PIPE)
        assert p.stderr.decode() == ""
        assert p.stdout.decode() == "Dexter ??\n"
        assert p.returncode == 4

   
    def test_disable_basic_cmd(self):
        fe = Fakear(cfg="tests/cfgs/multiple_cmd_mult_args.yml")
        fe.enable()
        assert fe.faked_path in os.environ["PATH"]
        assert os.path.exists(fe.faked_path)
        assert os.path.exists(fe.faked_path + "/echo")
        assert os.path.exists(fe.faked_path + "/ls")

        fe.disable()
        assert fe.faked_path not in os.environ["PATH"]
        assert not os.path.exists(fe.faked_path)


    def test_enable_cmd_with_file(self):
        fe = Fakear(cfg="tests/cfgs/cmd_with_output_file.yml")
        fe.enable()
        assert fe.faked_path in os.environ["PATH"]
        assert os.path.exists(fe.faked_path)
        assert os.path.exists(fe.faked_path + "/cc")
        assert os.path.exists( os.path.join(fe.faked_path, "cc_files") )

        p = run(["cc", "dd"], stdout=PIPE, stderr=PIPE)
        assert p.stderr.decode() == ""
        assert p.stdout.decode() == "ee ff\n"
        assert p.returncode == 0

    def test_disable_cmd_with_file(self):
        fe = Fakear(cfg="tests/cfgs/cmd_with_output_file.yml")
        fe.enable()
        p = run(["cc", "dd"], stdout=PIPE, stderr=PIPE)
        assert p.stderr.decode() == ""
        assert p.stdout.decode() == "ee ff\n"
        assert p.returncode == 0

        fe.disable()
        assert fe.faked_path not in os.environ["PATH"]
        assert not os.path.exists(fe.faked_path)

    def test_as_ctx_manager(self):
        with Fakear(cfg="tests/cfgs/cmd_with_output_file.yml") as fe:
            assert fe.faked_path in os.environ["PATH"]
            assert os.path.exists(fe.faked_path)
            assert os.path.exists(fe.faked_path + "/cc")
            assert os.path.exists( os.path.join(fe.faked_path, "cc_files") )

        assert fe.faked_path not in os.environ["PATH"]
        assert not os.path.exists(fe.faked_path)