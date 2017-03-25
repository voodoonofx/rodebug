# rodebug
ROPlus debug window.

## Installation
Just checkout this project into your `ROPlus\Scripts` folder.

## Usage
In game, open the Python Editor. `import rodebug` will open the GUI window. If it has a problem, use `Python -> Reload Context` to reset everything and try again.

Please make an issue about it also!

## Descriptions
This plugin monitors all attributes of a player, or if the checkbox is ticket, the target you're locked onto. Simply look through the list of items, or search for an attribute.

In a script, you'd be able to access any player attribute like this:

``` import BigWorld
player = BigWorld.player()
player.attribute_name  # <-- Right here
```

## Screenshots:
![main window screenshot](https://github.com/voodoonofx/rodebug/blob/master/screenshots/main_window.jpg)
