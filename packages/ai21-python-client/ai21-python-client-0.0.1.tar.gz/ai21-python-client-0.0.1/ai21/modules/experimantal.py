from ai21.modules.resources.nlp_task import NLPTask
from ai21.utils import validate_mandatory_field


class Experimental(NLPTask):
    MODULE_NAME = 'experimental'

    @classmethod
    def execute(cls, **params):
        url = f'{cls.get_base_url(**params)}/experimental/{cls.MODULE_NAME}'
        return super().execute(task_url=url, **params)
