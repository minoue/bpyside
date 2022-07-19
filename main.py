import bpy
import sys
import platform

from PySide2 import QtWidgets, QtCore
from importlib import reload
from . import window
from . import theme

reload(theme)

OS = platform.system()


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

    def modal(self, context, event):
        # bpy.context.window_manager
        wm = context.window_manager

        if not self.widget.isVisible():
            # if widget is closed
            wm.event_timer_remove(self._timer)
            return {'FINISHED'}
        else:
            self.event_loop.processEvents()
            self.app.sendPostedEvents(None, 0)

        return {'PASS_THROUGH'}

    def execute(self, context):
        reload(window)

        self.app = QtWidgets.QApplication.instance()
        if not self.app:
            self.app = QtWidgets.QApplication(sys.argv)

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
        self.app.setStyleSheet(theme.STYLE_SHEET)
        self.widget = window.MyWindow()

        if OS == "Darwin":
            pass
        elif OS == "Linux":
            wm = context.window_manager
            self._timer = wm.event_timer_add(1 / 120, window=context.window)
            context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}


CLASSES = [PYSIDE_OT_display_window, PYSIDE_PT_tools_my_panel]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
