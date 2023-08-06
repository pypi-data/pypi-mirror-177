"""Configuration file for the test_extension app."""
from django.apps import AppConfig
from django.db.models.signals import post_migrate


def post_migrate_callback(sender, **kwargs):
    """Initialize extension after database is ready."""
    from collectivo.extensions.utils import register_extension
    from .populate import populate_keycloak_with_test_data
    from collectivo.menus.utils import register_menuitem

    register_extension(
        name=sender.name,
        version='0.0.1',
        description='A test extension.'
    )

    register_menuitem(
        item_id='show_nothing',
        menu_id='main_menu',
        label='Do nothing',
        extension=sender.name,
    )

    register_menuitem(
        item_id='show_HelloSingle2',
        menu_id='main_menu',
        label='Open test webcomponent',
        extension=sender.name,
        action='component',
        component_name='HelloSingle2'
    )

    register_menuitem(
        item_id='show_iframe',
        menu_id='main_menu',
        label='Open test iframe',
        extension=sender.name,
        action='link',
        link_source='http://example.com'
    )

    populate_keycloak_with_test_data()


class TestExtensionConfig(AppConfig):
    """Configuration class for the test_extension app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_extension'

    def ready(self):
        """
        Initialize app when it is ready.

        Database calls are performed after migrations, using the post_migrate
        signal. This signal only works if the app has a models.py module.
        """
        post_migrate.connect(post_migrate_callback, sender=self)
