```python
class APIException(Exception):
    """Base API Exception class with default status code and payload."""
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class AuthenticationError(APIException):
    """Exception raised for errors in the authentication."""
    status_code = 401

    def __init__(self, message="Authentication failed", status_code=None, payload=None):
        APIException.__init__(self, message, status_code, payload)


class ValidationError(APIException):
    """Exception raised for errors in the validation of data."""
    status_code = 422

    def __init__(self, message="Data validation failed", status_code=None, payload=None):
        APIException.__init__(self, message, status_code, payload)


class PaymentProcessingError(APIException):
    """Exception raised for errors during payment processing."""
    status_code = 402

    def __init__(self, message="Payment processing failed", status_code=None, payload=None):
        APIException.__init__(self, message, status_code, payload)
```