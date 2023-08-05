import itertools as it
import re
from collections import OrderedDict
import pandas as pd

from robot.api import logger
from robot.errors import RobotError
from robot.libraries.BuiltIn import BuiltIn

from DataDriver.AbstractReaderClass import AbstractReaderClass
from DataDriver.ReaderConfig import TestCaseData


DEFAULT_PREFIX = 'arg'


def _flat_iterator(*source):
    _result = []
    for k in source:
        if isinstance(k, (tuple, list)):
            _result.extend(_flat_iterator(*k))
        else:
            _result.append(k)
    return _result


def all_permutation(*source):
    return [_flat_iterator(*_value) for _value in it.product(*source)]


def _pairs_permutation(*source):
    raise NotImplementedError()


PERMUTATION_METHOD = {
    'all': all_permutation,
    'pair': _pairs_permutation
}


def parse_permutations(prefix='arg', permutation_mode='all', **kwargs) -> pd.DataFrame:
    eq_cls = OrderedDict()
    err = []
    for var, item in {k: v for k, v in kwargs.items() if k.startswith(prefix)}.items():
        try:
            _list = re.split(r'\s*:\s*', item, 2)
            var_names, items = tuple(re.split(r'\s*,\s*', _list[0])), re.split(r'\s*,\s*', _list[1])
            if items[0] == 'kw':
                kw, kw_args = items[1], items[2:]
                values = BuiltIn().run_keyword(kw, *kw_args)
            else:
                values = items
        except Exception as e:
            err.append(f"Item ({var}: {item}) raise error: {e}")
        else:
            eq_cls[var_names] = values

    if len(err) > 0:
        raise RobotError("Following permutations raising errors:\n\t{}".format('\n\t'.join(err)))

    _data = PERMUTATION_METHOD[permutation_mode](*eq_cls.values())
    _columns = _flat_iterator(*eq_cls.keys())
    _index = [i+1 for i, _ in enumerate(_data)]
    _data_frame = pd.DataFrame(data=_data, columns=_columns, index=_index)
    return _data_frame


class courtesy_generator(AbstractReaderClass):
    __doc__ = """Courtesy generator are DataDriver extension for create data driven test from 
    courtesan multiplication between provided lists
    Test Suite usage:
        Library    DataDriver   reader_class=../../py/data_generators/courtesy_generator.py
        ...                     file_search_strategy=None
        ...                     prefix='prefix pattern' (Default: arg)
        ...                     tags=Attack,Sanity
        ...                     arg1=binary:kw,ReadBinaryList,${BINARY_PATH}
        ...                     arg2=mode:Blocking, NonBlocking
        ...                     permutation=all| pairs; (Default: all - currently supported only)
    Where:
        tags: must return same tags as in 'Force Tags' of suite
        arg1, arg2, ...: (bonded variable group separated by coma): [Options]
        Options:
            1. Elements for iteration separated by coma
            2. If first are 'kw', second handled as keyword name, rest handles as keyword arguments (As following from  
               usage of 'run keyword' of BuiltIn library
               Note: provided keyword must return list of tuples correlated to bonded variables count
        
        Assumption:
        Iteration calculating between arguments with prefix only
        
    """

    def get_data_from_source(self):
        test_data = []
        _tags = [t.strip() for t in re.split(r'\s*,\s*', self.kwargs.get('tags', ''))]
        prefix = self.kwargs.get('prefix', DEFAULT_PREFIX)
        permutation_mode = self.kwargs.get('permutation', 'all')
        data: pd.DataFrame = parse_permutations(prefix, permutation_mode, **self.kwargs)
        if len(data) == 0:
            logger.info("[ DataDriver ] empty data source created", also_console=True)
            return test_data
        logger.info("[ DataDriver ] data source created:\n\t{}".format(data), also_console=True)
        for index, item in data.iterrows():
            _args = {f"${{{var}}}": value for var, value in dict(item).items()}
            _documentation = "Test for {}".format(
                ', '.join([f'{var}: {value}' for var, value in dict(item).items()])
            )
            test_data.append(TestCaseData(_documentation, _args, _tags, _documentation))

        return test_data


__all__ = [
    'courtesy_generator',
    all_permutation.__name__
]
