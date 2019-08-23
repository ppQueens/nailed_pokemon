from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

_NAME_ASKED = False


def name_asked(bool_value=None):
    global _NAME_ASKED
    if bool_value is not None:
        _NAME_ASKED = bool_value
    return _NAME_ASKED


def get_tz(location):
    tf = TimezoneFinder()
    try:
        tz_str = tf.closest_timezone_at(lat=location.latitude, lng=location.longitude)
    except Exception as e:
        tz_str = 'UTC'
        #log
    return tz_str


def get_address(location):
    geolocator = Nominatim()
    try:
        loc = geolocator.reverse((location.latitude, location.longitude), language='en', timeout=5)
    except GeocoderTimedOut:
        return None
    return loc.raw['address']
