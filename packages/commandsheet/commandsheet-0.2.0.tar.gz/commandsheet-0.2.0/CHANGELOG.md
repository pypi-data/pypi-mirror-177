# Changelog

## 0.2.0 (2022-11-17)

### Changes
- Add a `--sample-config` option to easily produce a basic config file

### Bugfixes
- Exit and print error message when `--fillchar` or `-f` is supplied with more than one argument

## 0.1.0 (2022-11-02)

### Changes
- Make output prettier thanks to `rich`
- Drop support for Windows due to problems with encoding
- Declare compatibility for python versions `3.7` and higher
- Move from `pytest-cov` to `coverage`
- Make example photo point to full url
- Use `tox-gh-actions` for automated testing
- Improve tests

### Bugfixes
- Add missing dependency `attrs`

## 0.1.0a1 (2022-10-18)
- First release of Commandsheet
