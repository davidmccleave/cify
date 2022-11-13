"""
The base classes package contains all general classes used by the algorithms and components in CIFY.
One of the most notable classes is the :class:`Algorithm` class. This class is used by the user to create their
own novel algorithms that are not variants of the algorithms supplied in CIFY. For more detail on implementing
your own algorithms, check out the algorithms tutorial.
"""

from cify.core.base_classes.algorithm import *
from cify.core.base_classes.agent import *
from cify.core.base_classes.collection import *
