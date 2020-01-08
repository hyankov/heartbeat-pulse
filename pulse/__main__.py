# System import
import argparse
import yaml

# Local imports
from profiles import Profile
from profiles.storage import FileProfileStorage
from providers.management import ProvidersManager
from cron import ProfileRunner
from cron.output import ConsoleResultHandler


def setup_usage():
    """
    Description
    --
    Sets up the allowed usage.

    Returns
    --
    The command-line args.
    """

    def _run_config_template(args):
        # Resolve dependencies
        providers_manager = ProvidersManager()

        # Create profile based on every registered provider
        templates = []
        for i, provider_id in enumerate(providers_manager.get_all_ids()):
            profile_template = Profile("Name goes here {}".format(i + 1), provider_id, 10)
            params = providers_manager.discover_parameters(provider_id)
            for param_key in params:
                param = params[param_key]
                profile_template.provider_parameters[param_key] = "[{}] {}".format("required" if param.required else "optional", param.description)
            templates.append(profile_template)

        # Dump the profiles in the template file
        with open(args.output_filename, 'w') as file:
            file.write(yaml.dump(templates))

        print("Config template written into file '{}'. Edit it to your liking and use it as an input for the 'start' command.".format(args.output_filename))

    def _run_start(args):
        # Resolve dependencies
        runner = ProfileRunner(
            FileProfileStorage(args.input_filename),
            ProvidersManager(),
            ConsoleResultHandler())

        # Start
        runner.start()

    """
    Main body function.
    """

    default_input_config_file = "config.yaml"
    default_output_config_file = "config-template.yaml"

    parser = argparse.ArgumentParser()
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
    config_parser.set_defaults(func=_run_config_template)

    # Start
    start_parser = subparsers.add_parser(
                            'start',
                            help='Start the heartbeat monitor.')

    start_parser.add_argument(
                            '-i',
                            '--input_filename',
                            default=default_input_config_file,
                            help='Configuration filename (default: {})'.format(default_input_config_file))
    start_parser.set_defaults(func=_run_start)

    return parser.parse_args()


"""
When the script is executed.
"""
if __name__ == '__main__':
    menu_args = setup_usage()
    menu_args.func(menu_args)
