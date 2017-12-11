#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
import datetime
import logging
import prettytable
import requests
import six

from osc_lib.command import command

from oslo_utils import encodeutils

from osvmexpire._i18n import _
from osvmexpire import exc as osvmexpire_exc

SERVICE_TYPE = 'vmexpire'

EXPIRE_COLUMNS = [
    'id',
    'instance_id',
    'instance_name',
    'project_id',
    'user_id',
    'expire',
    'notified',
    'notified_last'
    ]


def get_endpoint(client_manager):
    return client_manager.get_endpoint_for_service_type(SERVICE_TYPE)


def pretty_print(columns, data):
    pt = prettytable.PrettyTable(columns)
    for d in data:
        row = []
        for column in columns:
            if column == 'expire':
                row.append(str(datetime.datetime.fromtimestamp(d[column])))
            else:
                row.append(str(d[column]))
        pt.add_row(row)

    if six.PY3:
        return encodeutils.safe_encode(pt.get_string()).decode()
    else:
        return encodeutils.safe_encode(pt.get_string())


class ExtendExpire(command.Command):
    """Extend osvmexpire"""

    def get_parser(self, prog_name):
        parser = super(ExtendExpire, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<osvmexpire-id>',
            help=_('Name of the osvmexpire')
        )
        return parser

    def take_action(self, parsed_args):
        # Client manager interfaces are available to plugins.
        # This includes the OSC clients created.
        columns = EXPIRE_COLUMNS
        return pretty_print(columns, [self._extend(parsed_args.id)])

    def _extend(self, expire_id):
        endpoint = get_endpoint(self.app.client_manager)
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.app.client_manager.auth_ref.auth_token
            }
        req = requests.put(
            endpoint + '/vmexpires/' + expire_id,
            headers=headers
            )
        if not req.status_code == 202:
            raise osvmexpire_exc.HTTPNotFound('no expiration found')
        res = req.json()
        if 'vmexpire' not in res:
            raise osvmexpire_exc.HTTPNotFound('no expiration found')
        return res['vmexpire']


class DeleteExpire(command.Command):
    """Delete osvmexpire"""

    def get_parser(self, prog_name):
        parser = super(DeleteExpire, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<osvmexpire-id>',
            help=_('Name of the osvmexpire')
        )
        return parser

    def take_action(self, parsed_args):
        # Client manager interfaces are available to plugins.
        # This includes the OSC clients created.
        self._delete(parsed_args.id)
        return "Deleted"

    def _delete(self, expire_id):
        endpoint = get_endpoint(self.app.client_manager)
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.app.client_manager.auth_ref.auth_token
            }
        req = requests.delete(
            endpoint + '/vmexpires/' + expire_id,
            headers=headers
            )
        if req.status_code == 404:
            raise osvmexpire_exc.HTTPNotFound('no expiration found')
        elif req.status_code == 403:
            raise osvmexpire_exc.HTTPUnauthorized('not authorized')
        elif req.status_code != 204:
            raise osvmexpire_exc.HTTPInternalServerError('Error')
        return


class ShowExpire(command.Command):
    """Show osvmexpire"""

    log = logging.getLogger(__name__ + '.ShowVMExpire')

    def get_parser(self, prog_name):
        parser = super(ShowExpire, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<osvmexpire-id>',
            help=_('Name of the osvmexpire')
        )
        return parser

    def take_action(self, parsed_args):
        # Client manager interfaces are available to plugins.
        # This includes the OSC clients created.
        columns = EXPIRE_COLUMNS
        return pretty_print(columns, [self._show(parsed_args.id)])

    def _show(self, expire_id):
        endpoint = get_endpoint(self.app.client_manager)
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.app.client_manager.auth_ref.auth_token
            }
        req = requests.get(
            endpoint + '/vmexpires/' + expire_id,
            headers=headers
            )
        if not req.status_code == 200:
            raise osvmexpire_exc.HTTPNotFound()
        res = req.json()
        if 'vmexpire' not in res:
            raise osvmexpire_exc.HTTPNotFound()
        return res['vmexpire']


class ListExpire(command.Command):
    """Delete osvmexpire"""

    log = logging.getLogger(__name__ + '.ListVMExpire')

    def take_action(self, parsed_args):
        # Client manager interfaces are available to plugins.
        # This includes the OSC clients created.

        columns = EXPIRE_COLUMNS
        return pretty_print(columns, self._list())

    def _list(self):
        endpoint = get_endpoint(self.app.client_manager)
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.app.client_manager.auth_ref.auth_token
            }
        req = requests.get(endpoint + '/vmexpires/', headers=headers)
        if not req.status_code == 200:
            raise osvmexpire_exc.HTTPNotFound()
        res = req.json()
        if 'vmexpires' not in res:
            raise osvmexpire_exc.HTTPNotFound()
        return res['vmexpires']
