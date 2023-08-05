from configparser import ConfigParser
from contextlib import contextmanager
from pathlib import Path
from os import chdir

from commandsheet.cli import CustomArgumentParser
from commandsheet.config import config_file_path_exists
from commandsheet.config import is_valid_config_file
from commandsheet.config import config_empty
from commandsheet.config import config_exists
from commandsheet.config import parse_config
from commandsheet.config import Section
from commandsheet.config import produce_sample_config

import pytest


@contextmanager
def inside_dir(path):
    old_path = Path.cwd()
    try:
        chdir(path)
        yield
    finally:
        chdir(str(old_path))


def test_section():
    section = Section(name='section', contents=('cmd', 'desc'))
    assert section.name == 'section'
    assert section.contents == ('cmd', 'desc')


def test_config_empty():
    empty_config = ConfigParser()
    not_empty_config = ConfigParser()
    with inside_dir('example'):
        assert config_empty(empty_config)
        not_empty_config.read('commandsheet.ini')
        assert not config_empty(not_empty_config)


def test_config_exists():
    exist_file = 'commandsheet.ini'
    no_exist_file = 'no_exist_commandsheet.ini'
    with inside_dir('example'):
        assert config_exists(exist_file)
        assert not config_exists(no_exist_file)


def test_is_valid_config_file():
    assert is_valid_config_file('commandsheet.ini')
    assert is_valid_config_file('also-valid.ini')
    assert not is_valid_config_file('config.invalid')


def test_config_file_path_exists():
    assert not config_file_path_exists('invalid/path/to/file')
    with inside_dir('example'):
        assert config_file_path_exists('commandsheet.ini')


def test_parse_config():
    with inside_dir('example'):
        not_empty_commandsheet = parse_config('commandsheet.ini')
        assert not_empty_commandsheet != []
        empty_commandsheet = parse_config('')
        assert empty_commandsheet == []


def test_sample_config(capsys):
    parser = CustomArgumentParser()

    with pytest.raises(SystemExit):
        produce_sample_config(parser)

    expected = (
        '[ffmpeg]\n'
        'ffmpeg -i input.mp4 output.avi = convert input.mp4 to output.avi\n'
        '\n'
        '[zipfiles]\n'
        'unzip filename.zip -d <dir> = unzip filename.zip to <dir>\n'
        'zip archive.zip file1 file2 = zip files to archive.zip\n'
        'zip -r archive.zip dir1 dir2 = zip dirs into archive.zip\n'
        'zip -r archive.zip dir1 dir2 file1 file2 = zip dirs & files into archive.zip\n'
        '\n'
        '[filesystem]\n'
        'ls -l = list in long format\n'
        'cp -v = copy and show what is happening\n'
        '\n'
        '[networking]\n'
        'ip a = show interface configuration\n'
        'ping <address> = ping address <address>\n'
    )

    out, err = capsys.readouterr()
    assert out == expected
    assert err == ''
