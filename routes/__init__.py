"""Route registration.

Maps URL paths to handler functions from the individual route
modules.  Imported by ``app.py`` to build the dispatch table.
"""

from routes.users import handle_users, handle_user_detail
from routes.settings import handle_settings, handle_setting_key
from routes.notifications import handle_notifications

ROUTES = {
    "/users": handle_users,
    "/users/": handle_user_detail,
    "/settings/": handle_settings,
    "/settings/key/": handle_setting_key,
    "/notifications/": handle_notifications,
}
