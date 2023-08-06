import getopt
import sys

from ..parser import GhsMapParser, ConfigParser
from ..reporter import ExcelReporter

def _usage(error: str):
    if error != "":
        print(error)
    print("map-analyzer [-c|--cfg name] [-m|--map name] [-e|--excel name] [-h|-help]")
    print("The analyze tools for C language Map file.")
    print("   -c|--cfg name   : The TOML configure file name")
    print("   -m|--map name   : The map file name")
    print("   -e|--excel name : The excel file name for all the reports")
    print("   -h            : Show the help information.")
    sys.exit(2)

def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hc:m:e:", ["help", "cfg=", "map=", "excel="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        _usage("")

    cfg_name = ""
    map_name = ""
    excel_name = ""
    for o, arg in opts:
        if o in ("-c", "--cfg"):
            cfg_name = arg
        elif o in ("-m", "--map"):
            map_name = arg
        elif o in ("-e", "--excel"):
            excel_name = arg
        elif o in ("-h", "--help"):
            _usage("")
        else:
            assert False, "unhandled option"

    if cfg_name == "":
        _usage("Please enter the TOML configure file name")

    if map_name == "":
        _usage("Please enter the map file name")

    try:
        
        config = ConfigParser()
        config.parse(cfg_name)

        if (config.compiler == "ghs"):
            map = GhsMapParser()
        else:
            raise ValueError("Invalid compiler <%s> is not supported." % config.compiler)

        map.parse(map_name, config.parameters)

        if (len(config.type_regexes) > 0):
            map.patch_type (config.type_regexes)

        if (len(config.group_regexes) > 0):
            map.patch_group(config.group_regexes)

        if (len(config.group_formats) > 0):
            map.format_group_name(config.group_formats)

        if (len(config.group_core_mapping) > 0):
            map.patch_group_core_mapping(config.group_core_mapping)

        if (len(config.core_regexes) > 0):
            map.patch_core(config.core_regexes)

        if (len(config.file_properties) > 0):
            map.patch_file_property(config.file_properties)

        map.analyze_core_data()

        if (excel_name == ""):
            map.display_groups()
        else:
            reporter = ExcelReporter()
            reporter.write_detail(map.items)
            reporter.write_summary(map.cores)
            reporter.save(excel_name)

    except Exception as e:
        #print(e)
        raise (e)


if __name__ == "__main__":
    main()
