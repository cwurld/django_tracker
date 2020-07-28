from importlib import import_module

from django.conf import settings

if hasattr(settings, 'IPINFO_TOKEN'):
    import ipinfo  # https://ipinfo.io/

if hasattr(settings, 'GEO_LOCATE_FUNC'):
    mod = import_module(settings.GEO_LOCATE_FUNC)
else:
    mod = None


class GeoLocate:
    """A wrapper for geo-locating IP addresses."""

    def __init__(self):
        # Set this setting to define your own geo-locate function. If the ip address = 'help', then return
        # the name of the geo-locating method.
        if mod:
            self.func = mod.geo_locate
        else:
            # If you want to use ipinfo.io, then define the token in your settings.
            token = getattr(settings, 'IPINFO_TOKEN', None)
            if token:
                try:
                    self.ip_info_getter = ipinfo.getHandler(token)
                except:
                    self.func = self.null_func
                else:
                    self.func = self.ipinfo_func
            else:
                self.func = self.null_func
        self._cache = {}

    # noinspection PyUnusedLocal
    @staticmethod
    def null_func(ip):
        return ''

    def ipinfo_func(self, ip):
        # For determining how geo-locating is done.
        if ip == 'help':
            return 'ipinfo'

        try:
            details = self.ip_info_getter.getDetails(ip)
            geo = '{}, {} {}'.format(details.city, details.region, details.country_name)
        except:
            geo = ''
        return geo

    def geo_locate(self, ip):
        if ip in self._cache:
            return self._cache[ip]
        geo = self.func(ip)
        self._cache[ip] = geo
        return geo


geo_locate = GeoLocate().geo_locate
