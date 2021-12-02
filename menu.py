import nuke
import sys
import os
sys.path.append(os.path.dirname(__file__) + "/split_layers")

from split_layers import split_layers
nuke.menu('Nuke').addCommand('Scripts/Split Layers', lambda: split_layers.main())