from jsonpath_ng import parse
from .paginate import ec_paginate

#####################################

class describe_cache_clusters(ec_paginate):
    def name(self): return __class__.__name__        
    def jsonpath_expression(self): return parse('CacheClusters[*]')
