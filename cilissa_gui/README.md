# CILISSA GUI

## Basic usage

1. Add images to Explorer via open files / open folder
2. Choose image pairs by selecting 2 images with the CTRL key and then pressing the "Add pair" button in the toolbar
3. Select metrics and transformations to use from the Explorer, configure them in the Properties widget
4. Press the "Run" button in the toolbar
5. The results will be displayed in the Console widget at the bottom, double click for more information

## Development

### Generating Qt resources file

```
$ pyside6-rcc resources/resources.qrc -o resources/resources.py
```
