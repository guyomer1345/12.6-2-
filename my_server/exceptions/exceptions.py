class ProtocolError(BaseException):
    '''Raise this error when protocol is broken'''
    pass

class ValidationError(BaseException):
    '''Raise this error when a client fails to validiate'''
    pass

class BadRequst(BaseException):
    '''Raise this error when a request was invalid'''
    pass

class NoPermissions(BadRequst):
    '''
    Raise this error when a client tried to do something that 
    requires greater permissions than he has
    '''
    pass