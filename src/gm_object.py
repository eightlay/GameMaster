class Object:
    table = ''

    def __init__(self) -> None:
        pass

    def get_data(self):
        data = {'table': self.table}
        data['fields'] = [
            field for field in dir(self)
            if not field.startswith('__') and
            field != 'table' and
            getattr(self, field) != None and
            not callable(getattr(self, field))
        ]
        data['values'] = [
            getattr(self, field)
            for field in data['fields']
        ]
        return data

    def __str__(self):
        data = self.get_data()
        return """Database table: {0}\nFields:\n {1}""".format(
            data['table'],
            "\n ".join(
                [
                    f"{field} = {value}"
                    for field, value in zip(data['fields'], data['values'])
                ]
            )
        )
