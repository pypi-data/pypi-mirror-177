import configparser
import warnings

_CONFIG_FILE = '../ml_models/scheduler_config.properties'


def read_properties(model_files):
    """Reads config properties from config file. Validates the config.
    Returns dictionary containing all properties belonging to each section"""
    config = _read_config()
    print('Read config')
    properties = {}

    for section in config.sections():
        properties[section] = _parse_section(config, section)

    _validate_config(model_files, properties)
    print('Validated config')
    return properties


def _read_config():
    config = configparser.ConfigParser()
    config.read(_CONFIG_FILE)
    return config


def _parse_section(config, section):
    properties = {}
    for key in config[section]:
        properties[key] = config[section][key]
    return properties


def _validate_config(model_files, properties):
    """Validate that for each model file, a cron job is specified."""
    config_sections = set(properties.keys())
    models = set(model_files)
    if config_sections != models:
        _print_warning(config_sections, models)


def _print_warning(config_sections, models):
    warnings.warn("WARNING:\n"
                  + "Wrong configuration in file /ml_models/scheduler_config.properties.\n"
                  + "The models /ml_models/*.py and sections in scheduler_config.properties do not match.\n"
                  + "Missing models for given config properties: {0}\n".format(config_sections.difference(models))
                  + "Missing config properties for given models: {0}\n".format(models.difference(config_sections)))
