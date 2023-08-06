from . import (
    LiteLog,
    LiteTasks,
    LiteMixin,
    LitePGL,
    LiteEvent,
    LiteConfig,
    LiteResource,
    LiteI18n,
    LiteThread,
    base,
    utils,
    )

__all__=[
    "LiteLog",
    "LiteMixin",
    "LiteThread",
    "LitePGL",
    "LiteResource",
    "LiteTasks",
    "LiteEvent",
    "LiteConfig",
    "LiteI18n",
    "base",
    "utils",
    ]

__version__="2022.11.20.02.22.39"

def __REQUIREMENTS__():
    '''
## if you want to use some class in our lib,you must install the lib below
### utils/cli
- #### click >= 8.0
- #### prompt_toolkit >= 3.0.31

### utils/net/pixiv
- #### pixivpy_async >= 1.2.14
    '''
    info="".join(__import__("inspect").getsourcelines(__REQUIREMENTS__)[0][2:-4])
    print(info)
    return info