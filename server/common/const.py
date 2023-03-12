import enum


class ChoiceBase(object):
    __choices__ = ()

    def get_choices(self):
        return self.__choices__

    @classmethod
    def get_display_name(cls, value):
        _names = dict(cls.__choices__)
        return _names.get(value) or ""

    @classmethod
    def get_enum(cls, name):
        _dict = dict(cls.__choices__)
        for key, value in _dict.items():
            if value == name:
                return key

    @classmethod
    def all_elements(cls):
        _dict = dict(cls.__choices__)
        return _dict.keys()


class ReturnCode(ChoiceBase, enum.Enum):
    Success = 0
    Error = -1
    # General Error
    GETMethodError = 101
    POSTMethodError = 102
    GetDataError = 103
    # User Error
    UserNameExist = 21
    UserNameNotExist = 22
    UserNameCheckError = 23
    UserPwdWrong = 24
    # Create User Error
    CreateUserError = 201
    EmptyNameOrPwd = 2011
    # Update Username Error
    UpdateUsernameError = 202
    EmptyOldnameOrNewname = 2021
    # Update Gender Error
    UpdateGenderError = 203
    EmptyNewGenderOrUsername = 2031
    # Update Passwd Error
    UpdatePasswdError = 204
    EmptyData = 2041
    # Login Error
    LoginError = 205
    PwdIncorrect = 2051
    EmptyUsernameOrPwd = 2052
    # Greeting Error
    # Get Greeting List Error
    GetListError = 301
    EmptyPostcode = 3011
    # Create new greeting Error
    SendGreetingError = 302


    __choices__ = (
        (Success, 'success'),
        (Error, 'fail'),
        (GETMethodError, 'not support for GET method'),
        (POSTMethodError, 'not support for POST method'),
    )