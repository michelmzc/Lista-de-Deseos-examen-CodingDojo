import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/ubuntu/exam')
from . import app as application