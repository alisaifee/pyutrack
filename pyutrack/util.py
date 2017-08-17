import collections
import functools

import dpath
import six
import pprint

import stringcase


def print_friendly(value, sep=', '):
    if isinstance(value, six.string_types):
        return value
    if isinstance(value, collections.Iterable):
        return sep.join(str(k) for k in value)
    return str(value)


class Response(dict):
    def __init__(self, data={}, aliases={}):
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
            {
                self.__aliases.get(k, k): v
                for k, v in other.items() if k != 'field'
            }
        )
        for f in other.get('field', []):
            super(Response, self).update({f['name']: f['value']})

    def __getitem__(self, item):
        return super(Response,
                     self).__getitem__(self.__aliases.get(item, item))

    def __setitem__(self, item, value):
        return super(Response,
                     self).__setitem__(self.__aliases.get(item, item), value)


class Type(type):
    class Association(collections.Iterable):
        def __init__(self, type, parent, get_config, add_config, del_config):
            self.type = type
            self.parent = parent
            self.get_config = get_config
            self.add_config = add_config
            self.del_config = del_config
            self._cache = None

        def __iadd__(self, other):
            if not self.add_config:
                raise NotImplementedError
            url = self.add_config.get('url')
            fields = self.parent.fields.copy()
            method = getattr(
                self.parent.connection, self.add_config.get('method')
            )
            for item in other:
                fields.update({self.add_config.get('key'): item})
                method(url % fields, {}, parse=False)
            return self

        def __len__(self):
            return len(list(self.__iter__()))

        def __isub__(self, other):
            if not self.del_config:
                raise NotImplementedError
            url = self.del_config.get('url')
            fields = self.parent.fields.copy()
            for item in other:
                fields.update({self.del_config.get('key'): item})
                self.parent.connection.delete(url % fields)
            return self

        def __iter__(self):
            if self._cache is None:
                assoc = self()
                hydrate = self.get_config.get('hydrate', False)
                if not isinstance(assoc, collections.Iterable):
                    raise TypeError(
                        '%s->%s is not iterable' %
                        (self.parent.__class__.__name__, self.type.__name__)
                    )
                else:
                    self._cache = (
                        self.type(
                            self.parent.connection, hydrate=hydrate, **v
                        ) for v in assoc
                    )
            return self._cache

        def __call__(self):
            fields = self.parent.fields.copy()
            fields.update(self.get_config.get('kwargs', {}))
            url = self.get_config.get('url') % fields
            return self.get_config.get('callback', lambda r: r
                                       )(self.parent.connection.get(url))

    class AssociationProperty(object):
        def __init__(self, binding):
            self.binding = binding

        def __get__(self, instance, obj_type):
            return self.binding(instance)

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
            super(Type.Base,
                  self).__setattr__('fields', Response(fields, aliases))
            if hydrate:
                self._get(
                    self.__get__.get('callback', lambda response: response)
                )

        def _get_attribute(self, lookup):
            try:
                return dpath.util.get(self.fields, lookup)
            except KeyError:
                return None

        def _update(self, callback, **kwargs):
            resource_data = self.__update_data(kwargs)
            self.connection.post(
                self.__update_endpoint(), resource_data, parse=False
            )
            self.fields.update(resource_data)

        def _delete(self, callback):
            return callback(
                self.connection.delete(self.__delete_endpoint(), parse=False)
            )

        @classmethod
        def _create(cls, connection, callback, **kwargs):
            return cls(
                connection,
                **callback(
                    connection.put(cls.__create_endpoint(**kwargs), kwargs)
                )
            )

        @classmethod
        def _list(cls, connection, callback, **kwargs):
            hydrate = cls.__list__.get('hydrate', False)
            data = [
                cls(connection, hydrate=hydrate, **obj)
                for obj in
                callback(connection.get(cls.__list_endpoint(**kwargs)))
            ]
            return data

        def _get(self, callback):
            self.fields.update(
                Response(
                    callback(self.connection.get(self.__get_endpoint())),
                    self.__aliases__
                )
            )

        def _get_association(self, params, **kwargs):
            if 'kwargs' in params['get']:
                params['get']['kwargs'].update(kwargs)
            return Type.Association(
                params['type'], self, params['get'],
                params.get('add', {}), params.get('remove', {})
            )

        def __get_endpoint(self):
            return self.__get__.get('url') % self.fields

        @classmethod
        def __create_endpoint(cls, **kwargs):
            return cls.__create__.get('url') % kwargs

        def __update_endpoint(self):
            return self.__update__.get('url') % self.fields

        def __update_data(self, kwargs):
            data = kwargs.copy()
            fields = kwargs.keys()
            data.update(
                {
                    k: self.fields[k]
                    for k in fields if not kwargs[k] and self.fields.get(k)
                }
            )
            return data

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
            data_source = self.fields
            if oneline:
                fields = getattr(self, '__render_min__', self.__render__)
                return '\t'.join(
                    str(data_source.get(k, getattr(self, k))) for k in fields
                )
            else:
                fields = template or self.__render__
                resp = ''
                for k in fields:
                    label = stringcase.sentencecase(k).ljust(20)
                    value = data_source.get(k, getattr(self, k, None))
                    resp += "%s : %s\n" % (label, print_friendly(value))
                return resp

        def __repr__(self):
            return pprint.pformat(self.fields)

        def __str__(self):
            return (
                getattr(self, '__label__', None)
                or ' '.join('%%(%s)s' % k for k in self.__render__)
            ) % self.fields

    def __new__(mcs, name, bases, dct):
        for verb in ['get', 'delete', 'update']:
            if '__%s__' % verb in dct:
                info = dct['__%s__' % verb]
                fn = Type.__build_func(
                    verb,
                    info.get('args', (())),
                    info.get('kwargs', {}), {
                        'callback':
                        info.get('callback', lambda response: response)
                    }
                )
                fn.__doc__ = '%s %s' % (verb, name.lower())
                dct[verb] = fn
        for verb in ['create', 'list']:
            if '__%s__' % verb in dct:
                info = dct['__%s__' % verb]
                fn = Type.__build_func(
                    verb, ('connection', ) + info.get('args', ()),
                    info.get('kwargs', {}), {
                        'callback':
                        info.get('callback', lambda response: response)
                    }
                )
                fn.__doc__ = '%s %s' % (verb, name.lower())
                dct[verb] = classmethod(fn)

        for association, params in dct.get('__associations__', {}).items():
            fn = Type.__build_func(
                'get_association', (),
                params.get('get', {}).get('kwargs', {}), {'params': params}
            )
            fn.__doc__ = 'get %s %s' % (name.lower(), association)
            dct[association] = Type.AssociationProperty(fn)
            dct[association].__doc__ = '%s %s' % (name.lower(), association)
            dct["get_%s" % association] = fn

        for attribute, lookup in dct.get('__attributes__', {}).items():
            getter = functools.partial(Type.Base._get_attribute, lookup=lookup)
            getter.__doc__ = attribute
            dct[attribute] = property(getter)

        return super(Type, mcs).__new__(mcs, name, (mcs.Base, ) + bases, dct)

    @staticmethod
    def __build_func(verb, args, kwargs, _locals):
        params = ['self']
        params += ['%s' % stringcase.snakecase(k) for k in args]
        params += [
            '%s=%s' % (
                stringcase.snakecase(k), "'%s'" % v
                if isinstance(v, six.string_types) else v
            ) for k, v in kwargs.items()
        ]
        largs = list(_locals.keys()) + list(args) + list(kwargs.keys())
        fn = eval(
            'lambda %s: self._%s(%s)' % (
                ','.join(params), verb, ','.join(
                    ['%s=%s' % (k, stringcase.snakecase(k)) for k in largs]
                )
            ), _locals
        )
        return fn
