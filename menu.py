import nuke

from split_layers import split_layers
nuke.menu('Nuke').addCommand('Scripts/Split Layers', lambda: split_layers.main())
