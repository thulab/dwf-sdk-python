from dwf.util.id import generate_primary_key
import random

class DataPatternTestInstance:
    def __init__(self, id, name, semantic):
        self.id = id
        random_postfix = random.randint(1000, 9999)
        self.name = '%s_%s' % (name, random_postfix)
        self.semantic = semantic


_setup_test_datapattern1 = DataPatternTestInstance(
    id=generate_primary_key('DPAT'),
    name = 'test_datapattern1_name',
    semantic = 'test_description')

_setup_test_datapattern2 = DataPatternTestInstance(
    id=generate_primary_key('DPAT'),
    name = 'test_datapattern2_name',
    semantic = 'test_description')

_setup_test_datapattern3 = DataPatternTestInstance(
    id=generate_primary_key('DPAT'),
    name = 'test_datapattern3_name',
    semantic = 'test_description')

_setup_test_datapattern4 = DataPatternTestInstance(
    id=generate_primary_key('DPAT'),
    name = 'test_datapattern4_name',
    semantic = 'test_description')