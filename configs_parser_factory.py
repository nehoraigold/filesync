import typing
from iconfigsparser import IConfigsParser
from json_configs_parser import JSONConfigsParser
from cli_configs_parser import CLIConfigsParser

class ConfigsParserFactory:
    @staticmethod
    def create(args: typing.List[str]) -> IConfigsParser:
        if ".json" in args[0]:
            return JSONConfigsParser.from_json(args[0])
        if len(args) > 0:
            return CLIConfigsParser(args)
        raise Exception("Encountered an issue attempting to create configuration parser!")