# moon_alt_phase_illum
repo for http server returning moon altitude phase and percent illum


This uses skyfield.api library.

Usage:
git clone
docker build -t moon .
docker run -d -pext_port:8180 moon

Access with coordonates 
curl "http://localhost:8180/?lat=44.123N&lon=20.123E"
{"alt": 14.35, "phase": 183.01, "percent": 99.87, "seven_seg": 126}