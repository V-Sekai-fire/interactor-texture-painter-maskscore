import os

import substance_painter.export
import substance_painter.project
import substance_painter.resource
import substance_painter.textureset

MESH_ENV = "MASKSCORE_MESH"
EXPORT_ENV = "MASKSCORE_EXPORT_DIR"
DEFAULT_EXPORT_DIR = os.path.join(os.path.expanduser("~"), "maskscore", "textures")
DEFAULT_PRESET = substance_painter.resource.ResourceID(
    context="starter_assets", name="PBR Metallic Roughness"
)


def open_garment(mesh_path, reference_image=None):
    if substance_painter.project.is_open():
        substance_painter.project.close()
    substance_painter.project.create(mesh_file_path=mesh_path)
    if reference_image:
        substance_painter.resource.import_project_resource(
            reference_image, substance_painter.resource.Usage.TEXTURE
        )


def export_textures(export_dir=None, preset=DEFAULT_PRESET):
    """Export every texture set of the open project under one preset."""
    if not substance_painter.project.is_open():
        raise RuntimeError("no project is open")
    export_dir = export_dir or os.environ.get(EXPORT_ENV, DEFAULT_EXPORT_DIR)
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


def run_batch(mesh_path, reference_image=None, export_dir=None):
    open_garment(mesh_path, reference_image)
    return export_textures(export_dir)


def start_plugin():
    mesh = os.environ.get(MESH_ENV)
    if not mesh:
        print("texture-painter-maskscore idle: set %s to run a batch" % MESH_ENV)
        return
    for path in run_batch(mesh):
        print("texture-painter-maskscore wrote %s" % path)


def close_plugin():
    pass


if __name__ == "__main__":
    start_plugin()
