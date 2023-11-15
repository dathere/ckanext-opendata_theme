# encoding: utf-8
import logging
import ckan.lib.helpers as h
import ckan.model as model
from sqlalchemy import func


from ckan.model.package import Package
from ckan.model.tracking import TrackingSummary
from ckan.model.package_extra import PackageExtra


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

def get_all_dataset_views():
    """
    Returns a sum of all dataset views
    """
    all_dataset_views = 0
    try:
        session = model.Session  

        all_dataset_views = (
            session.query(func.coalesce(func.sum(TrackingSummary.count), 0).label('total_views'))
            .join(TrackingSummary, TrackingSummary.package_id == Package.id)
            .filter(Package.state == 'active')  
            .group_by(Package.id)
            .scalar()
        )
    except Exception as e:
        logging.error('Error getting all dataset views: %s', e)
    return all_dataset_views