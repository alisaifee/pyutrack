import six

from pyutrack.util import Type


# Admin types
@six.add_metaclass(Type)
class Permission(object):
    __list__ = {'url': 'admin/permission', 'hydrate': False}
    __render__ = ('name', 'description')
    __label__ = '%(name)s'


@six.add_metaclass(Type)
class Role(object):
    __get__ = {'url': 'admin/role/%(name)s'}
    __create__ = {
        'url': 'admin/role/%(name)s',
        'args': ('name', ),
        'kwargs': {
            'description': ''
        }
    }
    __delete__ = {
        'url': 'admin/role/%(name)s',
    }
    __update__ = {
        'url': 'admin/role/%(name)s',
        'args': ('description', 'newName')
    }
    __list__ = {'url': 'admin/role', 'hydrate': True}
    __label__ = '%(name)s'
    __render__ = ('name', 'description')
    __associations__ = {
        'permissions': {
            'type': Permission,
            'get': {
                'url': 'admin/role/%(name)s/permission',
                'hydrate': False
            },
            'add': {
                'url': 'admin/role/%(name)s/permission/%(permission)s',
                'key': 'permission',
                'method': 'post'
            },
            'remove': {
                'url': 'admin/role/%(name)s/permission/%(permission)s',
                'key': 'permission'
            }
        }
    }


@six.add_metaclass(Type)
class Group(object):
    __get__ = {'url': 'admin/group/%(name)s'}
    __create__ = {
        'url': 'admin/group/%(name)s',
        'args': ('name', ),
        'kwargs': {
            'autoJoin': False,
            'description': ''
        }
    }
    __delete__ = {
        'url': 'admin/group/%(name)s',
    }
    __update__ = {
        'url': 'admin/group/%(name)s',
        'args': ('description', 'autoJoin', 'newName')
    }
    __list__ = {'url': 'admin/group', 'hydrate': True}
    __render__ = ('name', 'description', 'autoJoin')
    __label__ = '%(name)s'
    __associations__ = {
        'roles': {
            'type': Role,
            'get': {
                'url': 'admin/group/%(name)s/role',
                'hydrate': True
            },
            'add': {
                'url': 'admin/group/%(name)s/role/%(role)s',
                'key': 'role',
                'method': 'put'
            },
            'remove': {
                'url': 'admin/group/%(name)s/role/%(role)s',
                'key': 'role'
            }
        }
    }


@six.add_metaclass(Type)
class User(object):
    __get__ = {'url': 'admin/user/%(login)s'}
    __create__ = {
        'url': 'admin/user/%(login)s',
        'args': ('login', 'fullName', 'email', 'password')
    }
    __delete__ = {'url': 'admin/user/%(login)s'}
    __update__ = {
        'url': 'admin/user',
        'kwargs': {
            'login': '',
            'fullName': '',
            'email': '',
            'password': ''
        }
    }
    __list__ = {
        'url':
        'admin/user?q=%(query)s&role=%(role)s&permission=%(permission)s&group=%(group)s',
        'hydrate':
        True,
        'kwargs': {
            'project': '',
            'role': '',
            'permission': '',
            'query': '',
            'group': ''
        }
    }
    __render__ = ('login', 'email', 'fullName')
    __label__ = '%(name)s'
    __aliases__ = {'name': 'fullName'}
    __associations__ = {
        'groups': {
            'type': Group,
            'get': {
                'url': 'admin/user/%(login)s/group',
                'hydrate': False
            },
            'add': {
                'url': 'admin/user/%(login)s/group/%(group)s',
                'key': 'group',
                'method': 'post'
            },
            'remove': {
                'url': 'admin/user/%(login)s/group/%(group)s',
                'key': 'group'
            }
        },
        'roles': {
            'type': Role,
            'get': {
                'url': 'admin/user/%(login)s/role',
                'hydrate': True
            },
        }
    }


@six.add_metaclass(Type)
class IssueLinkType(object):
    __get__ = {'url': 'admin/issueLinkType/%(name)s'}
    __create__ = {
        'url': 'admin/issueLinkType/%(name)s',
        'args': ('outwardName', 'inwardName'),
        'kwargs': {
            'directed': False
        }
    }
    __delete__ = {'url': 'admin/issueLinkType/%(name)s'}
    __update__ = {
        'url': 'admin/issueLinkType/%(name)s',
        'kwargs': {
            'newName': '',
            'outwardName': '',
            'inwardName': '',
            'directed': ''
        }
    }
    __list__ = {'url': 'admin/issueLinkType', 'hydrate': False}
    __render__ = ('name', 'inwardName', 'outwardName')
    __label__ = '[%(name)s] X->%(inwardName)s->Y, Y->%(outwardName)s->X'


@six.add_metaclass(Type)
class IssueLink(object):
    __render__ = ('source', 'typeOutward', 'target')
    __label__ = '%(typeOutward)s %(target)s'
    pass


@six.add_metaclass(Type)
class Issue(object):
    __get__ = {'url': 'issue/%(id)s'}
    __create__ = {
        'url': 'issue/',
        'args': ('project', ),
        'kwargs': {
            'summary': '',
            'description': ''
        }
    }

    __delete__ = {'url': 'issue/%(id)s'}
    __update__ = {
        'url': 'issue/%(id)s/',
        'kwargs': {
            'summary': '',
            'description': ''
        }
    }
    __list__ = {
        'url': 'issue?filter=%(filter)s&max=%(max)d',
        'args': ('filter', ),
        'kwargs': {
            'max': 100
        },
        'hydrate': False,
        'callback': lambda response: response['issue']
    }
    __aliases__ = {'project': 'projectShortName'}
    __label__ = '%(id)s'
    __attributes__ = {
        'id': 'id',
        'assignee': 'Assignee/0/value',
        'reporter': 'reporterName',
        'updater': 'updaterName',
        'priority': 'Priority',
    }
    __render__ = (
        'id', 'summary', 'assignee', 'reporter', 'updater', 'priority'
    )
    __render_min__ = ('id', 'summary')
    __associations__ = {
        'issue_links': {
            'type': IssueLink,
            'get': {
                'url': 'issue/%(id)s/link'
            }
        }
    }

    def command(self, command):
        """
        executes a command for the given issue.

        :param str command: The youtrack command to execute. See
         https://www.jetbrains.com/help/youtrack/standalone/Commands.html
         for command grammar.
        """
        url = 'issue/%(id)s/execute' % {
            'id': self.id,
        }
        self.connection.post(url, {'command': command}, parse=False)
        self.get()


@six.add_metaclass(Type)
class Project(object):
    __get__ = {
        'url': 'admin/project/%(projectId)s',
    }
    __create__ = {
        'url': 'admin/project/%(projectId)s',
        'args': ('projectName', 'projectLeadLogin'),
        'kwargs': {
            'projectId': None,
            'startingNumber': 1,
            'description': ''
        }
    }
    __delete__ = {'url': 'admin/project/%(projectId)s'}
    __list__ = {'url': 'project/all', 'hydrate': True}

    __associations__ = {
        'issues': {
            'type': Issue,
            'get': {
                'url':
                'issue/byproject/%(projectId)s?filter=%(filter)s&max=%(max)d',
                'kwargs': {
                    'filter': '',
                    'max': 100
                }
            }
        }
    }
    __aliases__ = {
        'id': 'projectId',
        'shortName': 'projectId',
        'lead': 'projectLeadLogin'
    }
    __label__ = '%(id)s'
    __render__ = ('id', 'name', 'lead')
    __render_min__ = ('id', 'name')
