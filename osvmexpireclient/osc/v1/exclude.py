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

from osvmexpireclient._i18n import _
from osvmexpireclient import exc as osvmexpire_exc

SERVICE_TYPE = 'vmexpire'

EXCLUDE_COLUMNS = [
    'id',
    'exclude_id',
    'exclude_type',
    ]


def get_endpoint(client_manager):
    service = SERVICE_TYPE
    config = client_manager.get_configuration()
    if 'osvmexpire_service_type' in config:
        service = config['osvmexpire_service_type']
    return client_manager.get_endpoint_for_service_type(service)


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


class CreateExclude(command.Command):
    """Extend osvmexpire"""

    def get_parser(self, prog_name):
        parser = super(ExtendExpire, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<osvmexclude-object-id>',
            help=_('Id of the element to exclude (domain, project, user)')
        )
        parser.add_argument(
            'type',
            metavar='<osvmexclude-object-type>',
            help=_('Type of the element to exclude [domain, project, user]')
        )
        return parser

    def take_action(self, parsed_args):
        # Client manager interfaces are available to plugins.
        # This includes the OSC clients created.
        columns = EXCLUDE_COLUMNS
        return pretty_print(columns, [self._create(parsed_args.id, parsed_args.type)])

    def _create(self, exclude_id, exclude_type):
        exclude_type_int = -1
        if exclude_type == 'domain':
            exclude_type_int = 0
        elif exclude_type == 'project':
            exclude_type_int = 1
        elif exclude_type == 'user':
            exclude_type_int = 2
        endpoint = get_endpoint(self.app.client_manager)
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.app.client_manager.auth_ref.auth_token
            }
        req = requests.post(
            endpoint + '/vmexcludes/' + expire_id,
            headers=headers,
            json={
                'id': exclude_id,
                'type': exclude_type_int
                }
            )
        if not req.status_code == 202:
            raise osvmexpire_exc.HTTPNotFound('creation failed')
        res = req.json()
        if 'vmexclude' not in res:
            raise osvmexpire_exc.HTTPNotFound('no exclude created')
        return res['vmexclude']


class DeleteExclude(command.Command):
    """Delete osvmexpire"""

    def get_parser(self, prog_name):
        parser = super(DeleteExpire, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<osvmexclude-id>',
            help=_('Id of the exclude')
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
            endpoint + '/vmexcludes/' + expire_id,
            headers=headers
            )
        if req.status_code == 404:
            raise osvmexpire_exc.HTTPNotFound('no exclude found')
        elif req.status_code == 403:
            raise osvmexpire_exc.HTTPUnauthorized('not authorized')
        elif req.status_code != 204:
            raise osvmexpire_exc.HTTPInternalServerError('Error')
        return


class ShowExclude(command.Command):
    """Show osvmexpire"""

    log = logging.getLogger(__name__ + '.ShowVMExclude')

    def get_parser(self, prog_name):
        parser = super(ShowExpire, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<osvmexclude-id>',
            help=_('Id of the exclude')
        )
        return parser

    def take_action(self, parsed_args):
        # Client manager interfaces are available to plugins.
        # This includes the OSC clients created.
        columns = EXCLUDE_COLUMNS
        return pretty_print(columns, [self._show(parsed_args.id)])

    def _show(self, exclude_id):
        endpoint = get_endpoint(self.app.client_manager)
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.app.client_manager.auth_ref.auth_token
            }
        req = requests.get(
            endpoint + '/vmexcludes/' + exclude_id,
            headers=headers
            )
        if not req.status_code == 200:
            raise osvmexpire_exc.HTTPNotFound()
        res = req.json()
        if 'vmexclude' not in res:
            raise osvmexpire_exc.HTTPNotFound()
        return res['vmexclude']


class ListExclude(command.Command):
    """List osvmexclude"""

    log = logging.getLogger(__name__ + '.ListVMExclude')

    def take_action(self, parsed_args):
        # Client manager interfaces are available to plugins.
        # This includes the OSC clients created.

        columns = EXCLUDE_COLUMNS
        return pretty_print(columns, self._list())

    def _list(self):
        endpoint = get_endpoint(self.app.client_manager)
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.app.client_manager.auth_ref.auth_token
            }
        req = requests.get(endpoint + '/vmexcludes/', headers=headers)
        if not req.status_code == 200:
            raise osvmexpire_exc.HTTPNotFound()
        res = req.json()
        if 'vmexcludes' not in res:
            raise osvmexpire_exc.HTTPNotFound()
        for exclude in res['vmexcludes']:
            if exclude['exclude_type'] == 0:
                exclude['exclude_type'] = 'domain'
            if exclude['exclude_type'] == 1:
                exclude['exclude_type'] = 'project'
            if exclude['exclude_type'] == 2:
                exclude['exclude_type'] = 'user'
        return res['vmexcludes']
