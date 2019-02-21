import pytest
import yaml
import os

from fakear import Fakear
from voluptuous import Error as VoluptuousError


class TestErrorsFakear(object):
    def test_engine_multiple_args_one_error(self):
        with pytest.raises(VoluptuousError):
            Fakear(cfg="tests/cfgs/simple_cmd_mult_args_one_error.yml")


    def test_engine_YAMLError(self):
        with pytest.raises(yaml.YAMLError):
            Fakear(rawdata="unbalanced blackets: ][")


    def test_engine_VoluptuousError(self):
        with pytest.raises(VoluptuousError):
            Fakear(rawdata="- command: echo")


    def test_fuzzy_text(self):
        with pytest.raises(VoluptuousError):
            Fakear(cfg="tests/cfgs/fuzzy_text.yml")



