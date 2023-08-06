from jija_orm.executors import templates
from jija_orm.executors import executors


class QueryManager:
    def __init__(self, model_class, class_templates=None):
        self.__model_class = model_class
        self.__templates = self.fix_templates(class_templates)

    @staticmethod
    def fix_templates(class_templates):
        if not class_templates:
            return []

        templates_dict = {}
        for template in class_templates:
            if templates_dict.get(template.PRIORITY):
                if template.COMPARABLE is False:
                    templates_dict[template.PRIORITY] = template
                else:
                    raise NotImplementedError()

            else:
                templates_dict[template.PRIORITY] = template

        return list(templates_dict.values())

    def select(self, *args, **kwargs):
        class_templates = self.__templates.copy()
        class_templates.append(templates.Select(*args, **kwargs))
        return self.__class__(self.__model_class, class_templates)

    def update(self, *args, **kwargs):
        class_templates = self.__templates.copy()
        class_templates.append(templates.Update(*args, **kwargs))
        return self.__class__(self.__model_class, class_templates)

    def insert(self, **kwargs):
        class_templates = self.__templates.copy()
        class_templates.append(templates.Insert(**kwargs))
        return self.__class__(self.__model_class, class_templates)

    def multiple_insert(self, rows):
        # TODO need freeze?
        class_templates = self.__templates.copy()
        class_templates.append(templates.MultipleInsert(rows))
        return self.__class__(self.__model_class, class_templates)

    def where(self, *args, **kwargs):
        if self.__templates:
            class_templates = self.__templates.copy()
        else:
            class_templates = [templates.Select()]

        class_templates.append(templates.Where(*args, **kwargs))
        return self.__class__(self.__model_class, class_templates)

    def __await__(self):
        async def wrapper():
            executor = executors.Executor(self.__model_class, *self.__templates)
            return await executor.execute()

        return wrapper().__await__()
