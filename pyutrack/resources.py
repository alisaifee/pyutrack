import six

from pyutrack.util import Type


@six.add_metaclass(Type)
class Issue(object):
    __get__ = {'url': 'issue/%(id)s'}
    __create__ = {
        'url': 'issue/',
        'args': ('project',),
        'kwargs': {
            'summary': None,
            'description':None
        }
    }

    __delete__ = {'url': 'issue/%(id)s'}
    __update__ = {'url':'issue/%(id)s/', 'kwargs': {'summary': None, 'description':None}}
    __list__ = {
        'url': 'issue?%(filter)s', 'args': ('filter',), 'hydrate': False,
        'callback': lambda response: response['issue']
    }
    __aliases__ = {'project': 'projectShortName'}
    __render__ = ('id', 'summary', 'reporterName', 'updaterName', 'Priority')
    __render_min__ = ('id', 'summary')

# Admin types

@six.add_metaclass(Type)
class User(object):
    __get__ = {'url': 'admin/user/%(login)s'}
    __create__ = {'url': 'admin/user/', 'args': ('login', 'fullName', 'email', 'password')}
    __delete__ = {'url': 'user/%(login)s'}
    __update__ = {'url': 'admin/user/%(login)s', 'args': ('login',), 'kwargs': {'fullName': None, 'email': None, 'password': None}}
    __list__ = {'url': 'admin/user', 'hydrate': True}
    __render__ = ('login', 'email')

@six.add_metaclass(Type)
class Group(object):
    __get__ = {'url': 'admin/group/%(name)s'}
    __create__ = {'url': 'admin/group/', 'args': ('description', 'autoJoin')}
    __delete__ = {'url': 'group/%(name)s',}
    __update__ = {'url': 'admin/group/%(name)s', 'args': ('description', 'autoJoin', 'newName')}
    __list__ = {'url': 'admin/group', 'hydrate': True}
    __render__ = ('name', 'description')


@six.add_metaclass(Type)
class Project(object):
    __get__ = {'url': 'admin/project/%(projectId)s',}
    __create__ = {
        'url': 'admin/project/%(projectId)s', 'args': ('projectId', 'projectName', 'projectLeadLogin'),
        'kwargs': {'startingNumber': 1, 'description': None} }
    __delete__ = {'url': 'admin/project/%(projectId)s'}
    __list__ = {'url': 'project/all', 'hydrate': True}
    __aliases__ = {'id': 'projectId', 'shortName': 'projectId'}
    __render__ = ('id', 'name', 'lead')
    __render_min__ = ('id', 'name')

    def issues(self):
        return [
            Issue(self.connection, **issue) for issue in
            self.connection.get('issue/byproject/%(id)s' % self.fields)
        ]

