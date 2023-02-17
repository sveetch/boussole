import os

from boussole.utils import file_md5


def test_file_md5_001(settings):
    result = file_md5(os.path.join(settings.sample_path, 'dummy'))
    assert result == 'daef0a139a08d261f9ea9926b6b6dfdd'


def test_file_md5_002(settings):
    result = file_md5(os.path.join(settings.sample_path, 'utils/dummy.txt'))
    assert result == '4c713d41e328eb729d0ddfe85bfc9a00'


def test_file_md5_003(settings):
    result = file_md5(os.path.join(settings.sample_path, 'components/.dummy'))
    assert result == '946f722ff997f0d76e554aae7afc7ea8'
