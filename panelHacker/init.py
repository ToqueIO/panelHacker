import nuke
import os

# This just ensures that the current directory is in the nuke path and that we don't add it multiple times
currentDir = os.path.dirname(__file__)
# Check if the current directory is not already in Nuke's plugin path
if currentDir not in nuke.pluginPath():
    nuke.tprint(f'Adding {currentDir} to Nuke path')
    nuke.pluginAddPath(currentDir)
