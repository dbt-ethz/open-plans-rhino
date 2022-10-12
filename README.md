# open-plans-rhino
Rhino3D plugin to interact with open plans

## Getting started
The [documentation](https://dbt-ethz.gitbook.io/open-plans/) is a good place to start.

## Installation
1. Rhino should be closed when “installing” new plugins, otherwise it will need to be restarted before it recognizes any new commands.
2. Go to [releases](https://github.com/dbt-ethz/open-plans-rhino/releases) and download the source code (.zip). 
3. Unpack this folder on your computer. 
4. In order for this to run as a command in Rhino, the script location needs to be exactly right so that Rhino knows where to look. From the unpacked zip file, drop the folder OPENPLANS (with the crazy string of numbers!) in the Rhino Plug-ins folder without changing the name! This folder is different for Windows and Mac users:

### Windows
On Windows (and Rhino 7.0), the path to a command script looks like this: 
```sh
%APPDATA%\McNeel\Rhinoceros\7.0\Plug-ins\PythonPlugIns\
```
### Mac
On Mac the path to the open plans plugin looks like this. NOTE: If the PythonPlugIns folder does not yet exist, you’ll have to create it.
```sh
~/Library/Application Support/McNeel/Rhinoceros/6.0/Plug-ins/PythonPlugIns/
```
