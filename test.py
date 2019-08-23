from timezonefinder import TimezoneFinder

# coordinates = (30, 40)
# tf = TimezoneFinder()
# tf.closest_timezone_at(lat=coordinates[0], lng=coordinates[1])

from geopy.geocoders import Nominatim
geolocator = Nominatim()
l = 0, 0
# location = geolocator.reverse(l, language='en')
# print(location.raw['address'])

l = [2,3]

try:
    z = l[3]
except IndexError as e:
    print(z)