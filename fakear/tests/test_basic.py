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




class TestErrorsFakear(object):
    def test_engine_multiple_args_one_error(self):
        with pytest.raises(VoluptuousError):
            Fakear(cfg="fakear/tests/cfgs/simple_cmd_mult_args_one_error.yml")


    def test_engine_YAMLError(self):
        with pytest.raises(yaml.YAMLError):
            Fakear(rawdata="unbalanced blackets: ][")


    def test_engine_VoluptuousError(self):
        with pytest.raises(VoluptuousError):
            Fakear(rawdata="- command: echo")


    def test_fuzzy_text(self):
        with pytest.raises(VoluptuousError):
            Fakear(cfg="fakear/tests/cfgs/fuzzy_text.yml")




class TestEndToEndFakear(object):
    def test_enable_basic_cmd(self):
        fe = Fakear(cfg="fakear/tests/cfgs/multiple_cmd_mult_args.yml")
        fe.enable()
        assert fe.faked_path in os.environ["PATH"]
        assert os.path.exists(fe.faked_path)
        assert os.path.exists(fe.faked_path + "/echo")
        assert os.path.exists(fe.faked_path + "/ls")
        
        
        p = run(["ls", "omelette", "du", "fromage"], capture_output=True)
        assert p.stdout.decode() == "Dexter ??\n"
        assert p.returncode == 4