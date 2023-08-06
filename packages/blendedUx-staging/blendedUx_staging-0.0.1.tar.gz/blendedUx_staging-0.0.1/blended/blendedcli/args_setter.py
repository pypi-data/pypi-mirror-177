class PackageInfo(object):
    """
    """
    def __init__(self, **kwargs):
        """
        Initialization of package info.
        """
        self.package_name = kwargs.get('package_name', None)
        self.package_id = kwargs.get('package_id', None)
        self.label = kwargs.get('label', None)
        self.draft = kwargs.get('draft', False)
        self.update = kwargs.get('update', None)
        self.force = kwargs.get('force', None)
        self.files = kwargs.get('files', None)
        self.package_type = kwargs.get('package_type', None)
        self.package_description = kwargs.get('package_description', None)
        self.package_type_name = kwargs.get('package_type_name', None)
        self.license_name = kwargs.get('license_name', None)
        self.new_name = kwargs.get('new_name', None)
        self.no_download = kwargs.get('no_download', None)
        self.replace_from_local_list = kwargs.get('replace_from_local_list', None)
        self.replace_from_hub_list = kwargs.get('replace_from_hub_list', None)
        self.cloned_package_name = kwargs.get('cloned_package_name', None)
        self.source_package = kwargs.get('source_package', None)
        self.canonical = kwargs.get('canonical', False)
        self.tweak_json = kwargs.get('tweak_json', False)
        self.is_licenses = kwargs.get('is_licenses', False)
        self.is_description = kwargs.get('is_description', False)
        self.share = kwargs.get('share')
        self.transfer = kwargs.get('transfer')
        self.transfer_by_me = kwargs.get('transfer_by_me')
        self.transfer_to_me = kwargs.get('transfer_to_me')
        self.license_name = kwargs.get('license_name')
        self.license_type = kwargs.get('license_type')
        self.allow_listed = kwargs.get('allow_listed')
        self.allow_bundled = kwargs.get('allow_bundled')
        self.allow_auto_add = kwargs.get('allow_auto_add')
        self.license_price = kwargs.get('license_price')
        self.upgrades = kwargs.get('upgrades')
        self.validate = kwargs.get('validate')
        self.get = kwargs.get('get')
        self.package_title = kwargs.get('package_title', None)
        self.organization = kwargs.get('organization', None)
        self.published = kwargs.get('published', None)
        self.purchased = kwargs.get('purchased', None)
        self.skip_validation = kwargs.get('skip_validation', False)
        self.secondary_category = kwargs.get('secondary_category', None)
        self.primary_category = kwargs.get('primary_category', None)


class AccountInfo(object):
    """
    """
    def __init__(self, **kwargs):
        self.blended_dir = kwargs.get('blended_dir', None)
        self.current_dir = kwargs.get('current_dir', None)
        self.current_account = kwargs.get('current_account', None)
        self.account_name = kwargs.get('account_name', None)
        self.email = kwargs.get('email', None)
        self.last_active = kwargs.get('last_active', None)
        self.user_slug = kwargs.get('user_slug', None)
