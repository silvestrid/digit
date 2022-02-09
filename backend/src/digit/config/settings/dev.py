from .base import *  # noqa: F403, F401


DEBUG = True
ALLOWED_HOSTS = ["*"]

try:
    from .local import *  # noqa: F403, F401
except ImportError:
    pass
