
_NAME_ASKED = False


def name_asked(bool_value=None):
    global _NAME_ASKED
    if bool_value is not None:
        _NAME_ASKED = bool_value
    return _NAME_ASKED


