import collections
import six
import pprint

import stringcase


class Field(object):
    def __init__(self, data):
        """

        :param data:
        """
        self.name = data['name']
        self.value = data['value']
        self.extras = {k: v for k, v in data.items() if k not in ['name', 'value']}

    def __repr__(self):
        return self.value.__repr__()

    def __str__(self):
        if isinstance(self.value, six.string_types):
            return self.value
        elif isinstance(self.value, collections.Iterable):
            return ','.join(self.value)
        else:
            return str(self.value)


class Response(dict):
    def __init__(self, data, aliases={}):
        """

        :param data:
        :param aliases:
        """
        super(Response, self).__init__()
        self.__aliases = aliases
        self.update(data)

    def update(self, other):
        """

        :param other:
        :return:
        """
        if not other: return
        super(Response, self).update(
            {self.__aliases.get(k, k): v for k, v in other.items() if k != 'field'}
        )
        for field in other.get('field', []):
            f = Field(field)
            super(Response, self).update({f.name: f})

    def __getitem__(self, item):
        return super(Response, self).__getitem__(self.__aliases.get(item, item))

    def __setitem__(self, item, value):
        return super(Response, self).__setitem__(self.__aliases.get(item, item), value)


class Type(type):
    class Base(object):
        __aliases__ = {}

        def __init__(self, connection, hydrate=False, **fields):
            """

            :param connection:
            :param hydrate:
            :param fields:
            """
            aliases = super(Type.Base, self).__getattribute__('__aliases__')
            super(Type.Base, self).__setattr__('connection', connection)
            super(Type.Base, self).__setattr__('fields', Response(fields, aliases))
            if hydrate:
                self._get()

        def __getattribute__(self, item):
            data = super(Type.Base, self).__getattribute__('fields')
            try:
                return data[item]
            except (KeyError,):
                return super(Type.Base, self).__getattribute__(item)

        def __setattr__(self, key, value):
            data = super(Type.Base, self).__getattribute__('fields')
            data[key] = value

        def _update(self, **kwargs):
            self.fields.update(self.connection.post(self.__update_endpoint(), kwargs))
            self.fields.update(kwargs)

        def _delete(self):
            self.connection.delete(self.__delete_endpoint())

        @classmethod
        def _create(cls, connection, **kwargs):
            return cls(
                **connection.put(
                    cls.__create_endpoint(**kwargs),
                    kwargs
                )
            )

        @classmethod
        def _list(cls, connection, **kwargs):
            collection = connection.get(cls.__list_endpoint(**kwargs))
            hydrate = cls.__list__.get('hydrate', False)
            return [
                cls(
                    connection, hydrate=hydrate, **obj
                ) for obj in collection
            ]

        def _get(self):
            self.fields.update(
                Response(
                    self.connection.get(self.__get_endpoint()),
                    self.__aliases__
                )
            )

        def _params(self, args):
            return dict(
                {
                    k: v for k, v in
                    args.items() if v
                }.items() + {
                    k: v for k, v in
                    self.fields.items() if k in args and v
                }.items()
            )

        def __get_endpoint(self):
            return self.__get__.get('url') % self.fields

        @classmethod
        def __create_endpoint(cls, **kwargs):
            return cls.__create__.get('url') % kwargs

        def __update_endpoint(self):
            return self.__update__.get('url') % self.fields

        def __delete_endpoint(self):
            return self.__delete__.get('url') % self.fields

        @classmethod
        def __list_endpoint(cls, **kwargs):
            return cls.__list__.get('url') % kwargs

        def format(self, template=None, oneline=False):
            """

            :param template:
            :param oneline:
            :return:
            """
            if oneline:
                fields = getattr(self, '__render_min__', self.__render__)
                return '\t'.join(
                    self.fields[k] for k in fields
                )
            else:
                if template=='all':
                    fields = self.fields.keys()
                else:
                    fields = self.__render__
                resp = ''
                for k in fields:
                    label = stringcase.sentencecase(k).ljust(20)
                    value = self.fields[k]
                    resp += "%s : %s\n" % (label, value)
                return resp

        def __repr__(self):
            return pprint.pformat(self.fields)

    def __new__(mcs, name, bases, dct):
        for verb in ['get', 'delete', 'update']:
            if '__%s__' % verb in dct:
                info = dct['__%s__' % verb]
                dct[verb] = Type.__build_func(
                    verb,
                    info.get('args', (())),
                    info.get('kwargs', {})
                )
        for verb in ['create', 'list']:
            if '__%s__' % verb in dct:
                info = dct['__%s__' % verb]
                dct[verb] = classmethod(Type.__build_func(
                    verb,
                    ('connection',) + info.get('args', ()),
                    info.get('kwargs', {})
                ))
        return super(Type, mcs).__new__(mcs, name, (mcs.Base,) + bases, dct)

    @staticmethod
    def __build_func(verb, args, kwargs={}, callback = None):
        params = ['self']
        params += ['%s' % stringcase.snakecase(k) for k in args]
        params += ['%s=%s' % (stringcase.snakecase(k), v) for k, v in kwargs.items()]
        largs = list(args) + list(kwargs.keys())
        return eval(
            'lambda %s: self._%s(%s)' % (
                ','.join(params), verb, ','.join(['%s=%s' % (k, stringcase.snakecase(k)) for k in largs])
            )
        )
