from pathlib import Path

import pytest

from config.config_parser import Config


def test_exception_for_args_parsed_count():

    with pytest.raises(Exception):
        Config._args_count_is_valid(
            ['test', 'test2', 'test3', 'test4', 'test5'])


def test_output_for_args_parsed_count():
    assert Config._args_count_is_valid(
        ['test', 'test2', 'test3', 'test4']) == True


def test_exception_for_invalid_path_arg():
    with pytest.raises(Exception):
        Config._entry_file_path_exists('test')


def test_output_for_parsed_path():
    assert Config()._entry_file_path_exists('systems') == True

def test_exception_for_invalid_mode_arg():
    with pytest.raises(Exception):
        Config._mode_is_valid('-u', ['-e', '-t'])

def test_output_for_valid_mode_arg():
    assert Config._mode_is_valid('-c',['-c', '-s'])

def test_output_for_initialization_config():
    ret_dict = {
        'entry_path': '/Users/dewciu/Development/private/krypton_polska_zadanie/systems',
        'output_path': '/Users/dewciu/Development/private/krypton_polska_zadanie/forecasts',
        'mode': 'continous',
        'api_key': 'ACEzczt5WrNJ4jTBN9XypvOQss6l02rl'
    }

    assert Config().get_config(['main.py', 'systems', 'forecasts', '-c']) == ret_dict

def test_output_for_valid_args():
    assert Config()._is_valid(['main.py', 'systems', 'forecasts', '-c']) == True

