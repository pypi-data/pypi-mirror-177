class Comparator:
    TEMPLATE = NotImplemented

    def __init__(self, value):
        self.value = value

    def calculate(self, field_name, field_type, *args, **kwargs):
        return self.TEMPLATE.format(field_name=field_name, value=self.value)


class NumericComparator(Comparator):
    OPERATOR = NotImplemented
    TEMPLATE = '{field_name} {operator}{equal} {value}'

    def __init__(self, value, equal=False):
        super().__init__(value)
        self.__equal = equal

    def calculate(self, field_name, field_type, *args, **kwargs):
        return self.TEMPLATE.format(
            field_name=field_name, operator=self.OPERATOR, equal='=' if self.__equal else '', value=self.value)


class Grater(NumericComparator):
    OPERATOR = '>'


class Lower(NumericComparator):
    OPERATOR = '<'


class Not(Comparator):
    TEMPLATE = '{field_name} {operator} {value}'

    def calculate(self, field_name, field_type, *args, **kwargs):
        if isinstance(field_type, bool):
            if self.value:
                operator = 'is'
            else:
                operator = 'not'

        else:
            operator = '!='

        return self.TEMPLATE.format(field_name=field_name, operator=operator, value=self.value)
