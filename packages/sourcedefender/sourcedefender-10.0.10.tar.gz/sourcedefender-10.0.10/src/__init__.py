__version__ = "10.0.10"
import msgpack,tgcrypto,boltons,pendulum,datetime,environs
try:
    from . import loader, tools
except ModuleNotFoundError:
    pass
