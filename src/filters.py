def checkConstraints(context: dict, constraints: dict) -> bool:
    for key, consts in constraints.items():
        val = context[key]

        consts = consts.split(' ')

        dtype = consts[0]

        if dtype == 'int':
            dtype = int
        elif dtype == 'float':
            dtype = float
        elif dtype == 'str':
            dtype = str
        else:
            raise TypeError(f"Invalid data type: {val} - {dtype}")

        # Check data type
        if not isinstance(val, dtype):
            return False
        
        for c in consts[1:]:
            if dtype != 'str':
                if c == 'positive':
                    if val <= 0:
                        return False

                if c == 'negative':
                    if val >= 0:
                        return False

                if c == 'nonnegative':
                    if val < 0:
                        return False

                if c == 'nonpositive':
                    if val > 0:
                        return False
            else:
                if c[0] == 'l':
                    if len(val) < int(c[0][1:]):
                        return False

                if c[0] == 'u':
                    if len(val) > int(c[0][1:]):
                        return False

    return True
