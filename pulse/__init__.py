# System import
import argparse
import yaml
from typing import List
from os import path

# Local imports
from .logging import get_module_logger
from .profiles import Profile
from .profiles.storage import FileProfileStorage
from .providers import ProvidersManager
from .cron import ProfileRunner
from .cron.output import LogResultHandler


def main():
    default_input_config_file = "config/profiles_config.yaml"
    default_output_config_file = "config/profiles_config-template.yaml"

    _logger = get_module_logger(__name__)

    def _command_config_template(args):
        """
        The command that's executed for config template.
        """

        # Resolve dependencies
        providers_manager = ProvidersManager()

        # Create profile based on every registered provider
        templates = []  # type: List[Profile]
        for i, provider_id in enumerate(providers_manager.get_all_ids() * 2):
            profile_template = Profile("Profile name goes here ({})".format(i + 1), provider_id, 10)
            params = providers_manager.discover_parameters(provider_id)
            for param_key in params:
                param = params[param_key]
                profile_template.provider_parameters[param_key] = "[{}] {}".format("required" if param.required else "optional", param.description)
            templates.append(profile_template)

        filename = default_input_config_file

        # if the default input exists, output the template under the template name
        if path.exists(default_input_config_file):
            filename = default_output_config_file

        # Dump the profiles in the template file
        with open(filename, 'w') as file:
            file.write(yaml.dump(templates))

        _logger.info("Config template written into file '{}'. Edit it to your liking and use it as an input for the 'start' command.".format(filename))

    def _command_start(args):
        """
        The command that's executed for starting the app.
        """

        # Resolve dependencies
        runner = ProfileRunner(
            FileProfileStorage(args.input_filename),
            ProvidersManager(),
            LogResultHandler())

        # Start
        runner.start()

    def _setup_usage_args():
        parser = argparse.ArgumentParser(
            prog="pulse",
            description="Heartbeat monitor.",
            epilog="Further documentation is available at <https://hyankov.github.io/heartbeat-pulse/>."
        )
        subparsers = parser.add_subparsers(
                                dest='mode',
                                required=True,
                                help='What would you like to do?')

        # Generate Config Template
        config_parser = subparsers.add_parser(
                                'gct',
                                help='Generate a config template file.')

        config_parser.add_argument(
                                '-o',
                                '--output_filename',
                                default=default_output_config_file,
                                help='Configuration template filename (default: {})'.format(default_output_config_file))
        config_parser.set_defaults(func=_command_config_template)

        # Start
        start_parser = subparsers.add_parser(
                                'start',
                                help='Start the heartbeat monitor.')

        start_parser.add_argument(
                                '-i',
                                '--input_filename',
                                default=default_input_config_file,
                                help='Configuration filename (default: {})'.format(default_input_config_file))
        start_parser.set_defaults(func=_command_start)

        return parser.parse_args()

    menu_args = _setup_usage_args()
    menu_args.func(menu_args)


"""
When the script is executed.
"""
if __name__ == '__main__':
    main()
