import datetime
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
import ckan.model as model
import ckan.lib.helpers as h

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
            'opendata_theme_get_featured_datasets': get_featured_datasets
            }



def get_featured_datasets():
    """
    Returns a list of featured datasets
    """
    featured_datasets = []
    try:
        featured_datasets = model.Session.query(Package)\
            .join(PackageExtra)\
            .filter(PackageExtra.key == 'featured_dataset')\
            .filter(PackageExtra.value == 'yes')\
            .filter(Package.state == 'active')\
            .order_by(PackageExtra.value) \
            .all()
    except Exception as e:
        logging.error('Error getting featured datasets: %s', e)
    featured_datasets_dict_list = h.convert_to_dict('package',featured_datasets)
    return featured_datasets_dict_list

# def get_all_dataset_views():
#     """
#     Returns a list of all dataset views
#     """
#     all_dataset_views = []
#     try:
#         all_dataset_views = model.Session.query(Package)\
#             .join(PackageExtra)\
#             .filter(PackageExtra.key == 'featured_dataset')\
#             .filter(PackageExtra.value == 'yes')\
#             .filter(Package.state == 'active')\
#             .order_by(PackageExtra.value) \
#             .all()
#     except Exception as e:
#         logging.error('Error getting featured datasets: %s', e)
#     all_dataset_views_dict_list = h.convert_to_dict('package',all_dataset_views)
#     return all_dataset_views_dict_list