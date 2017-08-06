import six

from pyoutrack.util import Type


@six.add_metaclass(Type)
class Issue(object):
    __get__ = ('issue/%(id)s',)
    __create__ = ('issue/', ('project',), {'summary': None, 'description': None})
    __delete__ = ('issue/%(id)s',)
    __update__ = ('issue/%(id)s/', (), {'summary': None, 'description': None})
    __aliases__ = {'project': 'projectShortName'}


# Admin types

@six.add_metaclass(Type)
class User(object):
    __get__ = ('admin/user/%(login)s',)
    __create__ = ('admin/user/', ('login', 'fullName', 'email', 'password'))
    __delete__ = ('user/%(login)s',)
    __update__ = ('admin/user/%(login)s', ('login',), {'fullName': None, 'email': None, 'password': None})
    __list__ = ('admin/user',)


@six.add_metaclass(Type)
class Group(object):
    __get__ = ('admin/group/%(name)s',)
    __create__ = ('admin/group/', ('description', 'autoJoin'))
    __delete__ = ('group/%(name)s',)
    __update__ = ('admin/group/%(name)s', ('description', 'autoJoin', 'newName'))
    __list__ = ('admin/group',)


@six.add_metaclass(Type)
class Project(object):
    __get__ = ('admin/project/%(projectId)s',)
    __create__ = (
        'admin/project/%(projectId)s', ('projectId', 'projectName', 'projectLeadLogin'),
        {'startingNumber': 1, 'description': None})
    __delete__ = ('admin/project/%(projectId)s',)
    __list__ = ('project/all',)
    __aliases__ = {'id': 'projectId', 'shortName': 'projectId'}

    def issues(self):
        return [
            Issue(**issue) for issue in self.connection.get('issue/byproject/%(id)s' % self.fields)
            ]
