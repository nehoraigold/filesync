import typing
from copier.icopier import ICopier
from copier.copier import Copier
from copier.test_copier import TestCopier
from configsparser.iconfigsparser import IConfigsParser
from utils.utils import OptionsFlag


class CopierFactory:
    @staticmethod
    def create(configs: IConfigsParser,
               src_path: str,
               dst_path: str,
               src_files: typing.Dict[str, str],
               dst_files: typing.Dict[str, str],
               number: int) -> ICopier:
        if configs.is_enabled(OptionsFlag.TEST_MODE):
            return TestCopier(src_path, dst_path, src_files, dst_files, number)
        else:
            return Copier(src_path, dst_path, src_files, dst_files, number)
