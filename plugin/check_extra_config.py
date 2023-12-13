import os

from netsim.utils import log
from box import Box

def post_transform(topology: Box) -> None:
  w_header = True

  for ndata in topology.nodes.values():
    if not 'config' in ndata:
      continue

    for cfg in list(ndata.config):
      cdir = f'{ os.path.dirname(__file__) }/{ cfg }'
      if not os.path.exists(cdir):          # Hopefully the extra-config refers to the plugins
        continue

      if os.path.exists(f'{ cdir }/{ ndata.device }.j2'):
        continue
      if os.path.exists(f'{ cdir }/{ ndata.name }.{ ndata.device }.j2'):
        continue

      if not 'message' in topology:
        topology.message = ''

      if w_header:
        w_header = False
        topology.message += '''
WARNING
===============================================================================
'''

      topology.message += f'''
* Lab device {ndata.name} needs extra configuration "{cfg}". That configuration
  is not available for device type "{ndata.device}". Please change the device
  type or configure the device manually.
'''
      
      ndata.config = [ f for f in ndata.config if f != cfg ]
