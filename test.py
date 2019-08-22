from timezonefinder import TimezoneFinder

# coordinates = (30, 40)
# tf = TimezoneFinder()
# tf.closest_timezone_at(lat=coordinates[0], lng=coordinates[1])

from geopy.geocoders import Nominatim
geolocator = Nominatim()
l = 46.865431, 35.390549
location = geolocator.reverse(l, language='en')
# print(location.raw['address'])

