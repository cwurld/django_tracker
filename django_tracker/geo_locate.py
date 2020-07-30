from importlib import import_module

from django.conf import settings

if hasattr(settings, 'IPINFO_TOKEN'):
    import ipinfo  # https://ipinfo.io/

if hasattr(settings, 'GEO_LOCATE_FUNC'):
    mod = import_module(settings.GEO_LOCATE_FUNC)
else:
    mod = None


class GeoLocate:
    """
    A wrapper for geo-locating IP addresses.

    If you do not want geo-locating, then this class takes care of that.

    If you want to use the ipinfo.io geo-locating service, then just set settings. To the token you get from
    them.

    If you want to write your own geo-locating function, then create a python module to do that.
    Set settings.GEO_LOCATE_FUNC to the import path (e.g. xxx.yyy) to that module. In that module include a
    function called geo_locate(ip) that takes the ip address as an argument and returns the location
    as a string. If the ip address = 'help', then return the name of the geo-locating method. Also include a
    function geo_located_details(ip). It should return the details as an HTML snippet.
    """
    def __init__(self):
        # Set this setting to define your own geo-locate function. If the ip address = 'help', then return
        # the name of the geo-locating method.
        self.func = self.null_func
        self.func_details = self.null_func

        if mod:
            self.func = mod.geo_locate
            self.func_details = mod.geo_locate_details
        else:
            # If you want to use ipinfo.io, then define the token in your settings.
            token = getattr(settings, 'IPINFO_TOKEN', None)
            if token:
                try:
                    self.ip_info_getter = ipinfo.getHandler(token)
                except:
                    pass
                else:
                    self.func = self.ipinfo_func
                    self.func_details = self.ipinfo_details_func
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

    def ipinfo_details_func(self, ip):
        try:
            details = self.ip_info_getter.getDetails(ip).all
        except:
            return 'no details'

        s = []
        if 'org' in details:
            s.append('ORG: {}'.format(details['org']))

        if 'hostname' in details:
            s.append('HOST: {}'.format(details['hostname']))

        if s:
            return '\n'.join(s)
        else:
            return 'no details'

    def geo_locate(self, ip):
        if ip in self._cache:
            return self._cache[ip]
        geo = self.func(ip)
        self._cache[ip] = geo
        return geo

    def geo_locate_details(self, ip):
        return self.func_details(ip)


geo_locate = GeoLocate().geo_locate
geo_locate_details = GeoLocate().geo_locate_details
