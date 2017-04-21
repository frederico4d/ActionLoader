bl_info = {
    "name": "Action Loader",
    "author": "Frederico Martins - Frankenstein",
    "version": (1, 1),
    "blender": (2, 78, 3),
    "location": "View3D > Tools > Animation",
    "description": "Lists all Actions and assigns it to active object",
    "warning": "",
    "wiki_url": "",
    "category": "Animation",
    }

import bpy

def update_action_list(self, context):
    ActiveAction = bpy.context.scene.objects.active.animation_data.action
    ActiveAction.use_fake_user = True
    ## First assign start and end frame props to current action
    ActiveAction["StartFrame"] = bpy.context.scene.frame_preview_start
    ActiveAction["EndFrame"] = bpy.context.scene.frame_preview_end
        
    ##then change the action to the picked on the list
    #object.animation_data.action = bpy.data.actions.get("anotheraction")
    #bpy.context.scene.actions_group.index
    bpy.context.scene.objects.active.animation_data.action = bpy.data.actions[bpy.context.object.action_list_index]
    ActiveAction = bpy.context.scene.objects.active.animation_data.action
    ActiveAction.use_fake_user = True
        
    if ActiveAction.get("StartFrame") == None:
        pass
    else:
        bpy.context.scene.frame_preview_start = ActiveAction["StartFrame"]
        bpy.context.scene.frame_preview_end = ActiveAction["EndFrame"] 
    bpy.context.scene.use_preview_range = True
    print("Ole compicha")
        
    ## center stuff on dopesheet
    for area in bpy.context.screen.areas:
        if area.type == 'DOPESHEET_EDITOR':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = {'area': area, 'region': region, 'edit_object': bpy.context.edit_object}
                    bpy.ops.action.view_all(override)
                        
        elif area.type == 'GRAPH_EDITOR':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = {'area': area, 'region': region, 'edit_object': bpy.context.edit_object}
                    bpy.ops.graph.view_all(override)
            
        elif area.type == 'TIMELINE':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = {'area': area, 'region': region, 'edit_object': bpy.context.edit_object}
                    bpy.ops.time.view_all(override)
    
    

class ACTION_UL_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False, icon_value=icon)
        elif self.layout_type in {'GRID'}:
            pass

class UIListPanelExample(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Action Loader"
    bl_idname = "OBJECT_PT_ui_list_example"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Animation"

    def draw(self, context):
        layout = self.layout
        ob = context.object
        
        indice = bpy.context.object.action_list_index 
        if bpy.data.actions[indice].get("EndFrame") == None:
            durationf = 0
            durations = 0
        else:
            durationf = bpy.data.actions[indice]["EndFrame"] - bpy.data.actions[indice]["StartFrame"]
            durations = durationf / bpy.context.scene.render.fps 
        
        #info = str(indice+1)+". "+bpy.data.actions[indice].name+ " | "+ str(durationf)+"f | "+ str(round(durations,4))+"s"
        info1 = "Name: "+bpy.data.actions[indice].name
        info2 = "Duration: " + str(durationf)+ " f. | "+ str(round(durations,6))+ "s. "
        layout.label (text = info1)
        layout.label (text = info2)
        layout.template_list("ACTION_UL_list", "", bpy.data, "actions", ob, "action_list_index")
        layout.label(text="Active object:")
        layout.operator("set.actionrange")
        layout.label (text= "   ")
        layout.label (text= "---Danger Zone!---")
        layout.operator("delete.action")

class OBJECT_OT_SetActionRange(bpy.types.Operator):
    """Sets current timeline range to action"""
    bl_idname = "set.actionrange"
    bl_label = "Set Action range by timeline"
 
    def execute(self, context):
        ActiveAction = bpy.context.scene.objects.active.animation_data.action
        print(ActiveAction)
        
        ActiveAction.use_fake_user = True
        ActiveAction["StartFrame"] = bpy.context.scene.frame_preview_start
        ActiveAction["EndFrame"] = bpy.context.scene.frame_preview_end
        print ("Actio StartFrame: ", ActiveAction["StartFrame"], " Action EndFrame: ", ActiveAction["EndFrame"])
        return{'FINISHED'} 
    
    
class OBJECT_OT_AssignAction(bpy.types.Operator):
    """Load Action to Active Object"""
    bl_idname = "delete.action"
    bl_label = "Delete Action"
    def execute(self, context):
        ActionNR = bpy.context.object.action_list_index
        bpy.data.actions[bpy.context.object.action_list_index].user_clear()
        bpy.data.actions.remove(bpy.data.actions[ActionNR])
        return{'FINISHED'} 

def register():
    bpy.types.Object.action_list_index = bpy.props.IntProperty(update=update_action_list)
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Object.action_list_index

if __name__ == "__main__":
    register()
    
