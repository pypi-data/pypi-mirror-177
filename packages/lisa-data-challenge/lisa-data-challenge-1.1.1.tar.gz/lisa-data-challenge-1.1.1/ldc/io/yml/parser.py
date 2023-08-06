from pint import UnitRegistry, UndefinedUnitError

UNITS = UnitRegistry()
def nested_parser(params: dict):
    for key, value in params.items():
        if isinstance(value, str):
            try:
                value = units.Quantity(value)
            except UndefinedUnitError:
                pass
            yield key, value
        if isinstance(value, dict):
            if value.keys() == {'values', 'units'}:
                yield key, [i * UNITS(value['units']) for i in value['values']]
            else:
                yield key, dict(nested_parser(value))
        if isinstance(value, list):
            values, unit = value

            yield key, [i * UNITS(unit) for i in values]
