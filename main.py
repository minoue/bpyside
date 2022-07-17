import bpy
import sys

from PySide2 import QtWidgets, QtCore
from importlib import reload
from . import window
from . import theme

reload(theme)


class PYSIDE_PT_tools_my_panel(bpy.types.Panel):
    bl_label = "Test Pyside"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        layout.operator('pyside.display_window')


class PYSIDE_OT_display_window(bpy.types.Operator):
    '''  '''
    bl_idname = 'pyside.display_window'
    bl_label = "Display Window"
    bl_options = {'REGISTER'}

    def execute(self, context):
        reload(window)

        self.app = QtWidgets.QApplication.instance()
        if not self.app:
            self.app = QtWidgets.QApplication(sys.argv)
        # self.app = QtWidgets.QApplication(['blender'])

        # Delete old window if exists
        for w in self.app.topLevelWidgets():
            try:
                instName = w.__class__.__name__
                clsName = window.MyWindow.__name__
                if instName == clsName:
                    w.close()
            except Exception:
                # No existing window
                pass

        self.event_loop = QtCore.QEventLoop()

        # sel = bpy.context.selected_objects
        # print(sel)

        self.app.setStyleSheet(theme.STYLE_SHEET)

        self.widget = window.MyWindow()

        return {'FINISHED'}


CLASSES = [PYSIDE_OT_display_window, PYSIDE_PT_tools_my_panel]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
