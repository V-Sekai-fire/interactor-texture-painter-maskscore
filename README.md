# interactor-texture-painter-maskscore

A plugin that makes a project from a garment mesh and exports its texture maps, so MaskScore and EditScore score textures, not flat renders.

## What it is for

The plugin drives the painting application's Python API, so a run is reproducible from a mesh path and an export preset rather than from recorded clicks. It creates a project from the mesh, imports the reference image, exports the texture set under a named preset, and leaves the maps for scoring.

## Install and run

Copy `painter_plugin.py` into the application's Python `startup` folder and restart the application. A `maskscore.json` beside the module names the mesh and the export folder, and the batch runs from the menu action the plugin registers once the application is up.

## Licence

The licence is not stated.
