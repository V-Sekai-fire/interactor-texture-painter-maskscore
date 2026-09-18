import json
import os

from PySide2 import QtWidgets

import substance_painter.event
import substance_painter.export
import substance_painter.project
import substance_painter.resource
import substance_painter.ui
import substance_painter.textureset

BATCH_CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maskscore.json")
DEFAULT_EXPORT_DIR = os.path.join(os.path.expanduser("~"), "maskscore", "textures")
PRESET_NAME = "PBR Metallic Roughness"


def batch_config(path=BATCH_CONFIG):
    """Read the batch to run. Absent file means idle, which is how the tool opens by hand."""
    if not os.path.exists(path):
        return {}
    with open(path) as handle:
        return json.load(handle)


def default_preset():
    # Resolved on call: a ResourceID built at import time runs before the shelf
    # is loaded.
    return substance_painter.resource.ResourceID(
        context="starter_assets", name=PRESET_NAME
    )


def open_garment(mesh_path, reference_image=None):
    if substance_painter.project.is_open():
        substance_painter.project.close()
    substance_painter.project.create(mesh_file_path=mesh_path)
    if reference_image:
        substance_painter.resource.import_project_resource(
            reference_image, substance_painter.resource.Usage.TEXTURE
        )


def export_textures(export_dir=None, preset=None):
    """Export every texture set of the open project under one preset."""
    if not substance_painter.project.is_open():
        raise RuntimeError("no project is open")
    preset = preset or default_preset()
    export_dir = export_dir or DEFAULT_EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)

    config = {
        "exportShaderParams": False,
        "exportPath": export_dir,
        "defaultExportPreset": preset.url(),
        "exportList": [
            {"rootPath": texture_set.name()}
            for texture_set in substance_painter.textureset.all_texture_sets()
        ],
        "exportParameters": [
            {"parameters": {"fileFormat": "png", "bitDepth": "8", "dithering": True}}
        ],
    }
    result = substance_painter.export.export_project_textures(config)
    if result.status != substance_painter.export.ExportStatus.Success:
        raise RuntimeError(result.message)
    return [path for paths in result.textures.values() for path in paths]


def run_batch(mesh_path, reference_image=None, export_dir=None, on_written=None):
    """Create the project, then export once it stops being busy.

    Project creation is asynchronous: exporting straight after it raises
    ValueError because the document is not there yet.
    """
    def _on_created(_event=None):
        substance_painter.event.DISPATCHER.disconnect(
            substance_painter.event.ProjectCreated, _on_created
        )
        substance_painter.project.execute_when_not_busy(_export)

    def _export():
        written = export_textures(export_dir)
        for path in written:
            print("texture-painter-maskscore wrote %s" % path)
        if on_written:
            on_written(written)

    # Creation is asynchronous: ProjectCreated says the document exists, and the
    # not-busy callback then waits for its texture sets to be built.
    substance_painter.event.DISPATCHER.connect(
        substance_painter.event.ProjectCreated, _on_created
    )
    open_garment(mesh_path, reference_image)


_ACTION = None


def _run_configured_batch():
    config = batch_config()
    if not config.get("mesh"):
        print("texture-painter-maskscore idle: no mesh in %s" % BATCH_CONFIG)
        return
    run_batch(config["mesh"], config.get("reference_image"), config.get("export_dir"))


def start_plugin():
    """Add the menu action. The batch does not run here: a project created while
    plugins load yields a document the API cannot query."""
    global _ACTION
    _ACTION = QtWidgets.QAction("MaskScore batch")
    _ACTION.triggered.connect(_run_configured_batch)
    menus = substance_painter.ui.ApplicationMenu
    target = next(name for name in ("Python", "Window", "Edit", "File")
                  if hasattr(menus, name))
    substance_painter.ui.add_action(getattr(menus, target), _ACTION)
    print("texture-painter-maskscore ready: %s > MaskScore batch" % target)


def close_plugin():
    if _ACTION is not None:
        substance_painter.ui.delete_ui_element(_ACTION)


if __name__ == "__main__":
    start_plugin()
