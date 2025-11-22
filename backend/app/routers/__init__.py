# This file makes the routers directory a Python package
# and allows easy imports

from . import products_router
from . import users_router
from . import previews_router

__all__ = [
    "products_router",
    "users_router",
    "previews_router"
]

