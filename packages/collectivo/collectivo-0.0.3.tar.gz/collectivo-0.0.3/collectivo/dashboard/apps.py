"""Configuration file for the dashboard extension."""
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from collectivo.version import __version__


def post_migrate_callback(sender, **kwargs):
    """Initialize extension after database is ready."""
    from collectivo.extensions.utils import register_extension
    from collectivo.menus.utils import register_menuitem

    name = 'dashboard'

    register_extension(
        name=name,
        version=__version__,
        description='An extension to provide a starting page.'
    )

    register_menuitem(
        item_id='dashboard_menu_item',
        menu_id='main_menu',
        label='Dashboard',
        extension=name,
        action='component',
        component_name='dashboard',
    )


class MembersConfig(AppConfig):
    """Configuration class for the dashboard extension."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collectivo.dashboard'

    def ready(self):
        """
        Initialize app when it is ready.

        Database calls are performed after migrations, using the post_migrate
        signal. This signal only works if the app has a models.py module.
        """
        post_migrate.connect(post_migrate_callback, sender=self)
