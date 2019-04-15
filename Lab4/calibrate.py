import ugradio
import leuschner
import astropy
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import FK5
import time
import numpy as np

def calibrate():

    #connect to equipment
    LeuschTelescope = ugradio.leusch.LeuschTelescope()
    spec = leuschner.Spectrometer('10.0.1.2')
    agilent = ugradio.agilent.SynthDirect()
    #LO = ugradio.agilent.SynthClient(host='127.0.0.1')

    #get coordinates
    alt, az = get_coords(120,0)
    LeuschTelescope.point(alt,az)
    agilent.set_frequency(636.25, 'MHz')
    spec.check_connected()
    spec.read_spec('Calibrateupper.fits',20,(120,0),'ga')


def get_coords(l,b):
    #get coordinates
    gal = SkyCoord(l=l*u.degree, b=b*u.degree, frame='galactic')
    eq  = gal.fk5
    eq.transform_to(FK5(equinox='J2019'))
    Ra = eq.ra.degree
    Dec = eq.dec.degree
    print(Ra)
    print(Dec)
    lat = ugradio.leo.lat
    lon = ugradio.leo.lon
    alt = ugradio.leo.alt
    t = astropy.time.Time(time.time(),format='unix')
    l = astropy.coordinates.EarthLocation(lat=lat*u.deg,
                        lon=lon*u.deg,height=alt*u.m)
    f = astropy.coordinates.AltAz(obstime=t,location=l)
    equinox='J2019'
    c = astropy.coordinates.SkyCoord(Ra, Dec, frame='fk5',unit='deg',equinox=equinox)
    altaz = c.transform_to(f)


    return altaz.alt.degree, altaz.az.degree
