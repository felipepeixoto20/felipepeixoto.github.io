bl_info = {
    "name": "Advanced STL Mesh Repair",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

class STLRepair(bpy.types.Operator):
    """Advanced STL Mesh Repair Tool"""
    bl_idname = "object.stl_repair"
    bl_label = "Advanced STL Repair"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}

        # Enter Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Deselect all first
        bpy.ops.mesh.select_all(action='DESELECT')

        # Recalculate outside normals
        bpy.ops.mesh.normals_make_consistent(inside=False)
        
        # Select non-manifold edges
        bpy.ops.mesh.select_non_manifold()
        
        # Try to fill holes
        bpy.ops.mesh.fill_holes(sides=0)

        # Remove non-manifold elements by dissolving
        bpy.ops.mesh.dissolve_limited(angle_limit=0.0872665)  # 5 degrees

        # Return to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # in the future repair and not just delete stl tools

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(STLRepair.bl_idname)

def register():
    bpy.utils.register_class(STLRepair)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(STLRepair)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
