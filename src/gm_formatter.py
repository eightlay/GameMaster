from string import Formatter


class ExtendedFormatter(Formatter):
    """An extended format string formatter

    Formatter with extended conversion symbol
    """

    def convert_field(self, value, conversion):
        """ Extend conversion symbol
        Following additional symbol has been added
        * f: convert list of fields to string for query
        * v: convert list of values to string for query
        * u: convert zip of (fields, values) to string for query

        default are:
        * s: convert with str()
        * r: convert with repr()
        * a: convert with ascii()
        """

        if conversion == "f":
            return ', '.join(value)
        elif conversion == "v":
            return ', '.join([
                f"'{val}'" if type(val) == str else f"{val}"
                for val in value
            ])
        elif conversion == "u":
            return ', '.join([
                f"{key} = '{val}'" if type(val) == str else f"{key} = {val}"
                for key, val in value
            ])
        # Do the default conversion or raise error if no matching conversion found
        return super(ExtendedFormatter, self).convert_field(value, conversion)


formatter = ExtendedFormatter()
