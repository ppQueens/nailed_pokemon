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
def kk():
    try:
        z = l[1]
    except IndexError as e:
        print(z)
    else:
        return True
    finally:
        print(2)

print(kk())