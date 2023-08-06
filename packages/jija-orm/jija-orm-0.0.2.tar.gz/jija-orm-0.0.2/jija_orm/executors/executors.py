import asyncio

from jija_orm import config, fields


class Param:
    def __init__(self, name):
        self.name = name


class __BaseExecutor:
    def __init__(self, model, *args, use_model=True, serializer=None):
        self.__model = model
        self.__use_model = use_model
        self.__serializer = model if use_model else serializer

        self.__params = set()
        self.templates = {}

        self.__parse_templates(args)
        self.__query = self.__generate_query()

    def __parse_templates(self, args):
        templates_list = sorted(args, key=lambda arg: arg.PRIORITY)

        for template in templates_list:
            if self.__use_model:
                template.set_model(model=self.__model)
            else:
                template.set_model(table=self.__model)

            self.templates[template.NAME] = template.calculate()
            self.__params.update(template.params)

    def __generate_query(self):
        return "\n".join(self.templates.values())

    @property
    def query(self):
        return self.__query

    def sync_execute(self, **kwargs):
        result = asyncio.run(self.execute(**kwargs))
        return result

    async def execute(self, **kwargs):
        if self.__params != set(kwargs.keys()):
            raise ValueError()

        connection = await self.get_connection()

        for key in kwargs.keys():
            kwargs[key] = fields.get_validator(kwargs[key]).to_sql(kwargs[key])

        query = self.__query.format(**kwargs)
        print(query)
        return self.__serialize(await connection.fetch(query))

    @staticmethod
    async def get_connection():
        return await config.JijaORM.get_connection()

    def __serialize(self, query_set):
        if not self.__serializer:
            return query_set

        return list(map(lambda record: self.__serializer(**record), query_set))


class Executor(__BaseExecutor):
    pass
