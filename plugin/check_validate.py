import os

from netsim import __version__
from netsim.utils import log
from box import Box

def init(topology: Box) -> None:
  if __version__ < '1.6.4':
    log.fatal('BGP labs require netlab version 1.6.4 or higher')

  if not topology.get('validate',None):
    return

  v_version = topology.get('_validate_version','1.7.0')
  if __version__ >= v_version:
    return

  topology.pop('validate',None)
  if 'message' not in topology:
    topology.message = ''

  topology.message += f'''
Upgrade to netlab release {v_version} to use 'netlab validate' command to
check the results of your configuration work.
'''

  return

def post_transform(topology: Box) -> None:
  if not topology.get('validate',None):
    return

  if 'message' not in topology:
    topology.message = ''

  x_device = topology.get('groups.external.device',None)
  if x_device is None:
    return

  v_dlist = topology.validate[0].devices
  if x_device in v_dlist:
    topology.message += '''
You can use the 'netlab validate' command to check whether you successfully
completed the lab exercise.
'''
    return
  
  topology.message += f'''
You're using {x_device} on external routers. Lab validation is not yet
supported on that device. If you want to use 'netlab validate' command,
use one of these devices on external routers: {", ".join(v_dlist)}
'''
