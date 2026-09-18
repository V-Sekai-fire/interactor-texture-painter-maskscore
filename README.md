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
Copy `painter_plugin.py` into the user plugin directory
(`~/Documents/Adobe/Adobe Substance 3D Painter/python/plugins/`) and restart the
application. `start_plugin` runs a batch when `MASKSCORE_MESH` names a mesh, and
otherwise stays idle so opening the tool by hand does not start a run.
