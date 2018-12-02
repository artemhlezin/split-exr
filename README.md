## Split .exr layers in nuke 


### Issues
The script doesn't work in nuke >= 11!

### How it works

Link to video:
[![Split exr layers]()](https://vimeo.com/248760837 "Split exr layers")

### Installation

- Download or clone this repo
`git clone https://github.com/artemhlezin/split-exr.git`

- add `split-exr` folder to your nuke plugin path

For example, modify init.py 
```python
import nuke

nuke.pluginAddPath("./python/split-exr")
```
