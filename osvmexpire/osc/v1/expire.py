# osc-lib interfaces available to plugins:
from osc_lib.cli import parseractions
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import logs
from osc_lib import utils

import osvmexpire.exc
import logging

import requests

SERVICE_TYPE = 'openstackvmexpirationmanagement'

def get_endpoint(client_manager):
    return client_manager.get_endpoint_for_service_type(SERVICE_TYPE)

class ExtendExpire(command.Command):
    """Extend osvmexpire"""

    def take_action(self, parsed_args):
        # Client manager interfaces are available to plugins.
        # This includes the OSC clients created.
        client_manager = self.app.client_manager
        return

class DeleteExpire(command.Command):
    """Delete osvmexpire"""

    def take_action(self, parsed_args):
        # Client manager interfaces are available to plugins.
        # This includes the OSC clients created.
        client_manager = self.app.client_manager
        return

class ListExpire(command.Command):
    """Delete osvmexpire"""

    log = logging.getLogger(__name__ + '.ListVMExpire')

    def take_action(self, parsed_args):
        # Client manager interfaces are available to plugins.
        # This includes the OSC clients created.
        client_manager = self.app.client_manager
        self.log.error("Endpoint: " + self.app.client_manager.get_endpoint_for_service_type('openstackvmexpirationmanagement'))
        return self._list()

    def _list(self):
        endpoint = get_endpoint(self.app.client_manager)
        headers = {'Content-Type': 'application/json', 'X-Auth-Token': self.app.client_manager.auth_ref.auth_token}
        req = requests.get(endpoint + '/vmexpires/', headers=headers)
        if not req.status_code == 200:
            raise exc.Forbidden()
        res = req.json()
        if 'vmexpires' not in res:
            raise exc.Forbidden()
        return res
