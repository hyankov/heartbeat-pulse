# System import
import argparse

# Local imports
from core.profiles.management import ProfileManager
from core.profiles.storage import FileProfileStorage
from core.providers.management import ProvidersManager
from cron.output import ConsoleResultHandler
from cron.running import ProfileRunner
from webui.ui import ConsoleUI


def setup_menu():
    """
    Description
    --
    Sets up the allowed usage.

    Returns
    --
    The command-line args.
    """

    def _run_config_ui(args):
        # Resolve dependencies
        providers_manager = ProvidersManager()
        profile_manager = ProfileManager(
                                providers_manager,
                                FileProfileStorage(args.input_filename))

        ui = ConsoleUI(profile_manager, providers_manager)
        ui.start(args.input_filename)

    def _run_config_template(args):
        # TODO: Generate template in args.output_filename
        pass

    def _run_start(args):
        # Resolve dependencies
        providers_manager = ProvidersManager()
        runner = ProfileRunner(
                                ProfileManager(
                                    providers_manager,
                                    FileProfileStorage(args.input_filename)),
                                providers_manager,
                                ConsoleResultHandler())

        # Start
        runner.start()

    """
    Main body function.
    """

    default_input_config_file = "config.dat"
    default_output_config_file = "template-config.dat"

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
                            dest='mode',
                            required=True,
                            help='What would you like to do?')

    # Config
    config_parser = subparsers.add_parser(
                            'config',
                            help='Configure the heartbeat monitor.')

    # Config -> UI
    config_subparsers = config_parser.add_subparsers(
                            dest='config_mode',
                            required=True,
                            help='Choose configuration mode')

    config_ui_parser = config_subparsers.add_parser(
                            'ui',
                            help='Start web UI editor.')

    config_ui_parser.add_argument(
                            '-i',
                            '--input_filename',
                            default=default_input_config_file,
                            help='Configuration filename (default: {})'.format(default_input_config_file))
    config_ui_parser.set_defaults(func=_run_config_ui)

    # Config -> Template
    config_template_parser = config_subparsers.add_parser(
                            'template',
                            help='Generate a config template file.')

    config_template_parser.add_argument(
                            '-o',
                            '--output_filename',
                            default=default_output_config_file,
                            help='Configuration template filename (default: {})'.format(default_output_config_file))
    config_template_parser.set_defaults(func=_run_config_template)

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
    menu_args = setup_menu()
    menu_args.func(menu_args)
