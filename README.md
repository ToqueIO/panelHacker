

# Panel Hacker
A system for collecting and modifying existing panels inside of nuke.

Author: Joshua Robertson  
Active Version: 1.0.0  
Dev Version: 1.0.0  
GitHub: [github.com/toqueio/panelHacker]()  
Discord: [https://discord.gg/E2bqCuwwHv]()

### TODO:
- [ ] Create a `panelHacker` logo
- [ ] Create utilities to help in finding existing panels
- [ ] Create documentation for the `panelHacker` module and how to use/expand it.
- [ ] Re-work how the preferences are stored and loaded.  Current implementation is not ideal.


## Installation

1. Clone the repository to your local machine or download the zip file and extract the contents
   1. I recommend that you place the panelHacker directory in a subdirectory called toqueIO ie: ~/.nuke/toqueIO/panelHacker
   2. Then create an init.py in the toqueIO folder with the following code
    ```python
      import nuke
      import os
      
      toqueIODir = os.path.dirname(__file__)
      for subDir in os.listdir(toqueIODir):
        subDirPath = os.path.join(toqueIODir, subDir)
        if os.path.isdir(subDirPath):
           nuke.tprint(f"[ToqueIO] Adding {subDirPath} to plugin path")
           nuke.pluginAddPath(subDirPath)
    ```
       The folder sturcture would then look something like this:
       - .nuke
         - toqueIO
           - panelHacker
           - init.py   
   3. This will allow you to add more toqueIO tools and have them automatically added to the plugin path as long as they are in the toqueIO directory.

2. Open the init.py file in your .nuke directory and add the following line:
    ```python
    nuke.pluginAddPath('toqueIO')
    ```
   note: Make sure the the toqueIO that you add to the plugin path matches the casing exactly as the folder you created in step 1.
3. Restart nuke and you should be good to go.

## Current Features

* Overhaul of the script editors appearance so it more resembles PyCharms editor.
* Ability to add preferences into the existing tabs of nukes preferences.
* Added in color preferences for the script editor under the script editor tab in the preferences

## Attribution
It is not required at all, but it would be greatly appreciated if the tool becomes a part of your pipeline that you create a pull request to add your studio the studios.md file.  This way I can showcase where my tools are being used out in the industry.
