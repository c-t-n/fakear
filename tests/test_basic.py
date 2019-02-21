import pytest
import yaml
import os

from fakear import Fakear
from voluptuous import Error as VoluptuousError


class TestBasicFakear(object):
    def test_engine_instanciation(self):
        h = Fakear()
        assert isinstance(h, Fakear)


    def test_engine_simple_cmd(self):
        h = Fakear(cfg="tests/cfgs/simple_cmd.yml")
        assert isinstance(h, Fakear)
        assert "echo" in h.commands.keys()

    def test_engine_multiple_args(self):
        h = Fakear(cfg="tests/cfgs/simple_cmd_mult_args.yml")
        assert isinstance(h, Fakear)
        assert h.commands.get('echo', False)


    def test_path_immutable_when_activated(self):
        with Fakear() as fe:
            old_path = fe.faked_path
            fe.set_path("/etc/default")
            assert old_path == fe.faked_path