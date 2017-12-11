from osc_lib import utils


DEFAULT_API_VERSION = '1'

# Required by the OSC plugin interface
API_NAME = 'osvmexpire'
API_VERSION_OPTION = 'os_vmexpire_api_version'
API_VERSIONS = {
    '1': 'osvmexpire.v1.client.Client',
}

# Required by the OSC plugin interface
def make_client(instance):
    """Returns a client to the ClientManager

    Called to instantiate the requested client version.  instance has
    any available auth info that may be required to prepare the client.

    :param ClientManager instance: The ClientManager that owns the new client
    """
    print("##OSALLOU make_client")
    plugin_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)

    client = plugin_client()
    return client

# Required by the OSC plugin interface
def build_option_parser(parser):
    """Hook to add global options

    Called from openstackclient.shell.OpenStackShell.__init__()
    after the builtin parser has been initialized.  This is
    where a plugin can add global options such as an API version setting.

    :param argparse.ArgumentParser parser: The parser object that has been
        initialized by OpenStackShell.
    """
    parser.add_argument(
        '--os-osvmexpire-api-version',
        metavar='<osvmexpire-api-version>',
        help='OSC Plugin API version, default=' +
             DEFAULT_API_VERSION +
             ' (Env: OS_OSCPLUGIN_API_VERSION)')
    return parser
