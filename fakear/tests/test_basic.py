import pytest
import yaml
import os

from subprocess import run
from fakear import Fakear
from voluptuous import Error as VoluptuousError


class TestBasicFakear(object):
    def test_engine_instanciation(self):
        h = Fakear()
        assert isinstance(h, Fakear)


    def test_engine_simple_cmd(self):
        h = Fakear(cfg="fakear/tests/cfgs/simple_cmd.yml")
        assert isinstance(h, Fakear)
        assert "echo" in h.commands.keys()

    def test_engine_multiple_args(self):
        h = Fakear(cfg="fakear/tests/cfgs/simple_cmd_mult_args.yml")
        assert isinstance(h, Fakear)
        assert h.commands.get('echo', False)
