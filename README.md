# Texture Painter MaskScore

Paints a garment mesh in the texture-painting tool and exports its map set, so MaskScore and EditScore score textures rather than flat renders.

## Purpose
Turn the meshes produced upstream into MaskScore/EditScore texture datasets. The
plugin drives the painting tool's Python API, so a run is reproducible from a mesh
path and an export preset rather than from a recorded click sequence.

## Workflow
1. Create a project from a garment mesh.
2. Import the reference image as a project resource.
3. Export the texture set under a named preset.
4. Score the exported maps with EditScore/MaskScore.

## Install
Copy `painter_plugin.py` into `~/Documents/Adobe/Adobe Substance 3D Painter/python/startup/`
and restart the application. Modules under `plugins/` are enabled by hand in the UI;
modules under `startup/` always load.

`maskscore.json` beside the module selects the batch:

    {"mesh": "/path/garment.obj", "export_dir": "/path/textures"}

## The batch does not run at load
`start_plugin` only reports that it is ready. A project created while plugins are
loading yields a document the API cannot query — `all_texture_sets()` raises
`ValueError: Failed to get the document`, and chaining `ProjectCreated` and
`execute_when_not_busy` does not change it, because the application is not up yet.
Call `run_batch()` from the Python console once the application has started.
