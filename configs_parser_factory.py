import typing
from iconfigsparser import IConfigsParser
from json_configs_parser import JSONConfigsParser
from cli_configs_parser import CLIConfigsParser

class ConfigsParserFactory:
    @staticmethod
    def create(args: typing.List[str]) -> IConfigsParser:
        if len(args) > 1:
            return CLIConfigsParser(args)
        if len(args) < 1:
            raise Exception("No configuration information provided!")
        if ".json" in args[0]:
            return JSONConfigsParser.from_json(args[0])
        raise Exception("Encountered an issue attempting to create configuration parser!")