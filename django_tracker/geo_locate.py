import ipinfo  # https://ipinfo.io/


class GeoLocate:
    """
    This is one way to do geo-location. There are many other ways. You can write your own and add
    the function to settings.GEO_LOCATE_FUNC
    """
    def __init__(self, token):
        try:
            self.ip_info_getter = ipinfo.getHandler(token)
        except:
            self.ip_info_getter = None
        self._cache = {}

    def geo_locate(self, ip):
        if ip in self._cache:
            return self._cache[ip]

        if self.ip_info_getter:
            try:
                details = self.ip_info_getter.getDetails(ip)
                geo = '{}, {} {}'.format(details.city, details.region, details.country_name)
            except:
                geo = ''
        else:
            geo = ''

        self._cache[ip] = geo
        return geo
