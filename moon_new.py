from skyfield.api import Topos, load, utc
from skyfield.api import N,S,E,W, wgs84
from skyfield.api import utc
from skyfield.framelib import ecliptic_frame
from datetime import datetime
from pytz import timezone

cardinals_dict = {'N': N, 'S': S, 'E': E, 'W': W}

def parse_coords(lat, lon):
	_lat = False
	_lon = False
	for i in cardinals_dict:
		_lat = lat[:lat.find(i)]
		_lon = lon[:lon.find(i)]
		if lat.find(i)>0:
			_lat = float(_lat)*cardinals_dict[i]
		if lon.find(i)>0:
			_lon = float(_lon)*cardinals_dict[i]
	return float(_lat), float(_lon)

def get_moon_data(lat, lon):
    ts = load.timescale()
    planets = load('de421.bsp')
    t = ts.utc(datetime.now().replace(tzinfo=utc))
    earth, moon, sun = planets['earth'], planets['moon'], planets['sun']
    location = earth + wgs84.latlon(parse_coords(lat, lon)[0], parse_coords(lat, lon)[1], elevation_m=81)
    astrometric = location.at(t).observe(moon)
    alt, az, distance = astrometric.apparent().altaz()

    e = location.at(t)
    s = e.observe(sun).apparent()
    m = e.observe(moon).apparent()

    _, slon, _ = s.frame_latlon(ecliptic_frame)
    _, mlon, _ = m.frame_latlon(ecliptic_frame)
    phase = (mlon.degrees - slon.degrees) % 360.0

    percent = 100.0 * m.fraction_illuminated(sun)

    return round(alt.degrees, 2), round(phase, 2), round(percent, 2)

def format7seg(alt_phase_percent_tuple):
    (alt, phase, percent) = alt_phase_percent_tuple
    seven_seg_values = [0, 16, 32, 8, 64, 4, 2] #values to display, ie display.buff[x] = seven_segs[1] or sum(seven_segs)
    seven_seg_value = sum(seven_seg_values[-round(percent/(100/6)):len(seven_seg_values)]) if phase > 180 else sum(seven_seg_values[0:round(percent/(100/6))+1])
    if alt < 0:
        seven_seg_value += 1
    return seven_seg_value

#alt, phase, percent = format7seg(get_moon_data(lat, lon))
