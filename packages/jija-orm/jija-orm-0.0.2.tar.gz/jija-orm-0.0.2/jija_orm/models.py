import inspect

from jija_orm import fields
from jija_orm.executors import query, executors, templates


class Model:
    id = fields.IntegerField(pk=True)

    manager = query.QueryManager

    def __init__(self, *, from_query=False, **kwargs):
        self.__from_query = from_query
        self.__state = {}
        for kwarg in kwargs:
            if hasattr(self, kwarg):
                setattr(self, kwarg, kwargs[kwarg])
                self.__state[kwarg] = kwargs[kwarg]
            else:
                raise NotImplementedError()

    @classmethod
    def init_managers(cls, real_class=None):
        for name, attr in cls.__dict__.items():
            if inspect.isclass(attr) and issubclass(attr, query.QueryManager):
                setattr(real_class, name, attr(real_class or cls))

        if hasattr(cls.__base__, 'init_managers'):
            cls.__base__.init_managers(cls)

    @classmethod
    def get_fields(cls):
        model_fields = {}

        for name, attr in cls.__dict__.items():
            if isinstance(attr, fields.Field):
                model_fields[name] = attr

        if hasattr(cls.__base__, 'get_fields'):
            model_fields.update(cls.__base__.get_fields())

        return model_fields

    @classmethod
    def get_constraints(cls) -> dict[str, fields.RelatedField]:
        model_fields = {}

        for name, attr in cls.__dict__.items():
            if isinstance(attr, fields.RelatedField):
                model_fields[name] = attr

        if hasattr(cls.__base__, 'get_constraints'):
            model_fields.update(cls.__base__.get_constraints())

        return model_fields

    async def save(self):
        to_update = {}
        for arg in self.__state:
            real_arg = getattr(self, arg)
            if self.__state[arg] != real_arg:
                to_update[arg] = real_arg

        if not to_update:
            return

        executor = executors.Executor(
            self.__class__,
            templates.Update(**to_update),
            templates.Where(id=self.id)
        )

        return await executor.execute()

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()

    @classmethod
    def select(cls, *args, **kwargs):
        return cls.manager.select(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return cls.manager.update(*args, **kwargs)

    @classmethod
    def where(cls, *args, **kwargs):
        return cls.manager. where(*args, **kwargs)

    @classmethod
    def multiple_create(cls, rows):
        return cls.manager.multiple_insert(rows)

    def __await__(self):
        return self.manager.insert()

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'
