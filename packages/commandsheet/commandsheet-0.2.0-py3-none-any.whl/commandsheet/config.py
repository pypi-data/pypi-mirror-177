"""Code for parsing the user config."""

from attrs import define
from attrs import field
from pathlib import Path
from configparser import ConfigParser

CONFIG_FILE_FORMATS = {'.ini'}

SAMPLE_CONFIG = (
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
    'ping <address> = ping address <address>'
)


def produce_sample_config(parser):
    print(SAMPLE_CONFIG)
    parser.exit(status=0)


@define
class Section:
    name = field()
    contents = field()


def config_empty(config):
    return not config.sections()


def config_exists(path):
    return Path(path).expanduser().exists()


def is_valid_config_file(path):
    return Path(path).expanduser().suffix in CONFIG_FILE_FORMATS


def config_file_path_exists(path):
    """Verifies that, when `commandsheet -c <config>`, that <config> exists."""
    return config_exists(path)


def parse_config(path):
    config = ConfigParser()
    config.read(Path(path).expanduser())

    if config_empty(config):
        return []

    sections_raw = [
        section for section in config.values()
        # In our case, we don't care about the DEFAULT
        # section configparser creates to the config
        # object by default, so we'll just leave it out
        if not section.name == 'DEFAULT'
    ]

    sections_pretty = []
    for section in sections_raw:
        content = []
        for cmd, desc in section.items():
            content.append((cmd, desc))
        sections_pretty.append(Section(name=section.name, contents=content))

    return sections_pretty
