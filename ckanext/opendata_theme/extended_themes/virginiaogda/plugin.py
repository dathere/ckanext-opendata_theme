import datetime
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
import ckan.model as model

from ckan.model.package import Package
from ckan.model.package_extra import PackageExtra


class OpenDataThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')

    
    # ITemplateHelpers
    def get_helpers(self):
        return {
            'opendata_theme_get_featured_datasets': get_featured_datasets,
            'opendata_theme_get_stats': get_stats,
        }



def get_featured_datasets():
    """
    Returns a list of featured datasets
    """
    featured_datasets = []
    try:
        featured_datasets = model.Session.query(Package)\
            .join(PackageExtra)\
            .filter(PackageExtra.key == 'featured')\
            .filter(PackageExtra.value == 'true')\
            .filter(Package.state == 'active')\
            .order_by(PackageExtra.value) \
            .all()
    except Exception as e:
        logging.error('Error getting featured datasets: %s', e)
    return featured_datasets


def get_stats():
    '''
    Returns a list of stats
    '''
    stats = []
    # try:
    #     stats = model.Session.query(PackageExtra)\
    #         .filter(PackageExtra.key == 'stats')\
    #         .order_by(PackageExtra.value) \
    #         .all()
    # except Exception as e:
    #     logging.error('Error getting stats: %s', e)
    return stats