from enum import Enum

class SqlError(Enum):
    # common
    REQUIRED = "required"
    UNIQUE = "unique"
    INVALID = "invalid"
    BLANK = "blank"
    # users
    PASSWORD_TOO_SHORT = "password_too_short"
    PASSWORD_TOO_COMMON = "password_too_common"
    PASSWORD_ENTIRELY_NUMERIC = "password_entirely_numeric"


def badActionUser(request, reason):
    request.user.is_active = False
    request.user.msg = reason
    request.user.save()
    return {
        'error' : {
            'code' : 'badActionUser',
            'message' : 'You\'ve been blocked to access the platform due to security violations!'
        }
    }
