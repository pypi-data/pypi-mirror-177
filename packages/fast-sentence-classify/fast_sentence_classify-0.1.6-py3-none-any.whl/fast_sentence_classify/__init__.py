# -*- coding: utf-8 -*-
from .core import *
from .datablock import *

from typing import Any
from typing import Dict
from fast_sentence_classify.core.bp import Classifier

def classify(input_text: str) -> Dict[Any, Any]:
    return Classifier().run(input_text)

    # def test_orchestrator():

    #     bp = Classifier()
    #     assert bp

    #     input_text = "I'd like it if you could give me some directions to the library"

    #     result = bp.run(input_text)

    #     assert 'ts' in result
    #     result['ts'] = '1666897985.085184'

    #     assert 'stopwatch' in result
    #     result['stopwatch'] = '117.30μs'

    #     pprint(result)

    #     assert result == {
    #         'data': {
    #             'input_text': "I'd like it if you could give me some directions to the library",
    #             'output_text': 'WHERE_LOCATION'
    #         },
    #         'event': 'fast-sentence-classify',
    #         'service': 'classify',
    #         'stopwatch': '117.30μs',
    #         'ts': '1666897985.085184'
    #     }
