from ai21.modules.experimantal import Experimental
from ai21.utils import validate_mandatory_field


class Summarize(Experimental):
    MODULE_NAME = 'summarize'

    @classmethod
    def execute(cls, **params):
        validate_mandatory_field(key='text', call_name=cls.MODULE_NAME, params=params, validate_type=True, expected_type=str)
        return super().execute(**params)
