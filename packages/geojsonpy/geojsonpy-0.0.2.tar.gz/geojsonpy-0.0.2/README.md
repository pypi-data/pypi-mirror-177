<p align="center">
  <h2 align="center">GeoJsonPy</h2>

  <p align="center">Open GeoJSON data on geojson.io from Python.</p>
</p>
<br>


## Table of contents
- [Description](#description)
- [Requirement](#requirements)
- [Folder](#folder)
- [Setup](#setup)
- [Usage](#usage)
- [Contributors](#contributors)

### Description

There are two methods by which `geojsonpy.py` gets geojson.io to render the data:

Embedding the GeoJSON contents in the geojson.io URL directly
Creating an anonymous Github gist and embedding the gist id in the geojson.io URL.
`geojsonpy.py` automatically determines which method is used based on the length of the GeoJSON contents. If the contents are small enough, they will be embedded in the URL. Otherwise geojsonio.py creates an anonymous Gist on Github with the GeoJSON contents. Note: when an anonymous gist is created, the data is uploaded to Github and a unique gist ID is created. If anyone else is able to obtain the gist ID, they will be able to see your data.

### Folder
```
geojsonpy
├── geojsonpy
│   ├── geojsonpy.py
├── README.md
├── setup.cgf

```

### Requirements
For running each sample code:
- `python:` >= 3.7 


### Setup
Install with `pip`:
```
$ pip install geojsonpy
```

### Usage
Send data to geojson.io and open a browser within python:
```
from geojsonpy import display

with open('map.geojson') as f:
    contents = f.read()
    display(contents)
```

It can also be used on the command line. Read or pipe a file
```
$ geojsonpy map.geojson
$ geojsonpy < run.geojson

```

### Contributors

- Pietro Lechthaler 
- GitHub: https://github.com/pietrolechthaler