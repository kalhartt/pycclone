"""
test/test_utils.py

Test the included utility functions.
"""
import itertools
import os
import pycclone.utils as utils


def test_destination():
    """Test destination calculations."""
    test_files = [
        'test',
        'test.xyz',
        os.path.join('..', 'test.xyz'),
        os.path.join('subdir', 'test.xyz')
    ]
    test_dirs = [
        None,
        'dir',
        os.path.join('dir', 'dir'),
        os.path.join('..', 'dir'),
    ]
    testcases = itertools.product(test_files, test_dirs)
    for case in testcases:
        destination = utils.destination(*case)

        if case[1]:
            assert destination.endswith('test')
        else:
            assert destination == case[0]

        if not case[0].startswith('..') and case[1]:
            assert destination.startswith(case[1])


def test_split_path():
    """Test split_path calculations."""
    testcases = [[str(x) for x in range(n)] for n in range(1, 11)]
    for case in testcases:
        assert case == utils.split_path(os.path.join(*case))


def test_open_static():
    # TODO
    pass


def test_copy_static():
    # TODO
    pass
