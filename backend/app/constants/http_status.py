"""HTTP Status Code Constants

Centralized constants for HTTP status codes used throughout the application.
This improves maintainability and reduces magic numbers.
"""

# Client Error Status Codes (4xx)
BAD_REQUEST = 400
UNAUTHORIZED = 401
NOT_FOUND = 404
NOT_ACCEPTABLE = 406
CONFLICT = 409

# Server Error Status Codes (5xx)
INTERNAL_SERVER_ERROR = 500
SERVICE_UNAVAILABLE = 503
GATEWAY_TIMEOUT = 504
