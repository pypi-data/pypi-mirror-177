"""pynetsys is a collection of tools and malicious packets."""

from .error import PYNETSYS
from .constants import Protocol, Packets
from . import _tool, _packet
from requests import get
from socket import getfqdn

ERROR = PYNETSYS

__version__ = []
__author__ = "Andrea Vaccaro ANDRVV"

tool, packet = _tool, _packet

def hasSSLWebProtocol(Address: str):
    # RETURN
    if "https:\\" in Address:
        return True
    else:
        return False

def hasWebProtocol(Address: str):
    # RETURN
    if "http:\\" in Address:
        return True
    else:
        return False

def addWebProtocol(Address: str, SSL: int = False):
    # RETURN
    if hasWebProtocol(Address):
        raise ERROR("Already have a web protocol.")    
    else:
        if SSL == True:
            return f"https://{Address}/"
        else:
            return f"http://{Address}/"

def removeWebProtocol(Address: str):
    # RETURN
    if hasWebProtocol(Address) or hasSSLWebProtocol(Address):
        return Address.replace("http://", "").replace("https://", "").replace("/", "")
    else:
        raise ERROR("There is not a web protocol.")    

def isOnline(Address: str):
    # RUN & RETURN
    try:
        if get(getfqdn(Address)).status_code == 200:
            return True
        else:
            return False
    except:
        return False
