# -*- python -*-
#
#       Copyright INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
# ==============================================================================


import pkg_resources
__version__ = "0.1.0"
try:
    version = pkg_resources.require("agroservice")[0].version
    __version__ = version
except:
    version = __version__

import colorlog
logger = colorlog.getLogger("agroservices")

from .extern.easydev.config_tools import CustomConfig

# Initialise the config directory if not already done
configuration = CustomConfig("agroservices", verbose=False)
bspath = configuration.user_config_dir

from . import settings
from .settings import *

from . import services
from .services import *

from . import ipm
from .ipm import *


# sub packages inside bioservices.

#import mapping
#from . import apps





