bl_info = {
    "name": "Radial Duplicate",
    "description": "Duplicate selected objects in radial layout",
    "author": "Josh Caratelli and Liam McLachlan",
    "version": (1, 0),
    "blender": (2, 81, 1),
    "location": "View3D > Sidebar > Radial Duplicate",
    "wiki_url": "https://twitter.com/josh_caratelli",
    "support": 'COMMUNITY',
    "category": "Tool"
}

import bpy
import math
from bpy.props import IntProperty, FloatProperty, BoolProperty, PointerProperty
from bpy.types import PropertyGroup, Operator, Panel
from bpy.utils import register_class, unregister_class

class RadialDuplicateSettings(PropertyGroup):
    num_duplicates : IntProperty(
        name="Number of Duplicates",
        min=2,
        max=128,
        default=16
    )
    
    offset : FloatProperty(
        name="Offset",
        min=0.01,
        max=128,
        default=16
    )
    
    linked : BoolProperty(
        name="Linked Duplicates",
        default=True
    )
    
    angle_to_center : BoolProperty(
        name="Angle to Center",
        default=True
    )

    
class RadialDuplicateOperator(Operator):
    bl_idname = "scene.radial_duplicate"
    bl_label  = "Radial Duplicate"
    bl_options = {'REGISTER', 'UNDO'}

    # Undo-Redo dialogue option
    num_duplicates : IntProperty(
        name="Number of Duplicates",
        min=2,
        max=128,
        default=16
    )
    
    offset : FloatProperty(
        name="Offset",
        min=0.01,
        max=128,
        default=16
    )
    
    linked : BoolProperty(
        name="Linked Duplicates",
        default=True
    )
    
    angle_to_center : BoolProperty(
        name="Angle to Center",
        default=True
    )
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.mode == 'OBJECT' and len(context.selected_objects) >= 1

    def execute(self, context):
        # Ensure we have a relative rotation point (e.g. 3D Cursor will generate incorrectly)
        bpy.context.scene.tool_settings.transform_pivot_point = "ACTIVE_ELEMENT"

        ANGLE_STEP = 360 / self.num_duplicates
        
        # Rotate original object 
        if self.angle_to_center:
            bpy.ops.transform.rotate(value=math.radians(-ANGLE_STEP * 0.5), orient_axis='Z')
        
        for i in range( 1, self.num_duplicates):
            object = bpy.ops.object.duplicate(linked=self.linked, mode='TRANSLATION') 
            
            angle_step_rad = math.radians(i * ANGLE_STEP)
            
            x = math.cos(angle_step_rad) * self.offset
            y = math.sin(angle_step_rad) * self.offset
                        
            bpy.ops.transform.translate(value=(x, y, 0))
            
            if self.angle_to_center:
                bpy.ops.transform.rotate(value=math.radians(-ANGLE_STEP), orient_axis='Z')
            
        return {'FINISHED'}


class RadialDuplicatePanel(Panel):
    bl_label = "Radial Duplicate"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "Radial Duplicate"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        op = layout.operator(RadialDuplicateOperator.bl_idname, text="Duplicate")
        
        op.num_duplicates = scene.radial_duplicate.num_duplicates
        layout.prop(scene.radial_duplicate, "num_duplicates")
        
        op.offset = scene.radial_duplicate.offset
        layout.prop(scene.radial_duplicate, "offset")
        
        op.linked = scene.radial_duplicate.linked
        layout.prop(scene.radial_duplicate, "linked")
        
        op.angle_to_center = scene.radial_duplicate.angle_to_center
        layout.prop(scene.radial_duplicate, "angle_to_center")

        
def register():
    register_class(RadialDuplicateSettings)

    bpy.types.Scene.radial_duplicate = PointerProperty(type=RadialDuplicateSettings)
    register_class(RadialDuplicateOperator)
    register_class(RadialDuplicatePanel)

    
def unregister():
    unregister_class(RadialDuplicateSettings)
    unregister_class(RadialDuplicateOperator)
    unregister_class(RadialDuplicatePanel)
    del(bpy.types.Scene.radial_duplicate)

    
if __name__ == "__main__":
    register()
