bl_info = {
    "name": "Action Loader",
    "author": "Frederico Martins - Frankenstein",
    "version": (1, 3),
    "blender": (2, 78, 3),
    "location": "View3D > Tools > Animation",
    "description": "Lists all Actions and assigns it to active object",
    "warning": "",
    "wiki_url": "",
    "category": "Animation",
    }

import bpy


def update_action_list(self, context):
    #updates every time you pick action in the list
    ActiveAction = bpy.context.scene.objects.active.animation_data.action
    ActiveAction.use_fake_user = True
    ## First assign start and end frame props to current action
    ActiveAction["frame_start"] = bpy.context.scene.frame_preview_start
    ActiveAction["frame_end"] = bpy.context.scene.frame_preview_end
        
    ##then change the action to the picked on the list
    #object.animation_data.action = bpy.data.actions.get("anotheraction")
    #bpy.context.scene.actions_group.index
    bpy.context.scene.objects.active.animation_data.action = bpy.data.actions[bpy.context.object.action_list_index]
    ActiveAction = bpy.context.scene.objects.active.animation_data.action
    ActiveAction.use_fake_user = True
    
        
    if ActiveAction.get("StartFrame") == None:
        pass
    else:
        bpy.context.scene.frame_preview_start = ActiveAction["frame_start"]
        bpy.context.scene.frame_preview_end = ActiveAction["frame_end"] 
    bpy.context.scene.use_preview_range = True
    print("Ole compicha")
        
    ## center stuff on dopesheet etc...
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
    """Creates a Panel in the Animation tab of the 3D View's Tools"""
    bl_label = "Action Loader !"
    bl_idname = "OBJECT_PT_ui_list_example"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Animation"

    def draw(self, context):
        layout = self.layout
        ob = context.object
        
        indice = bpy.context.object.action_list_index     
            
        print ("INDEX SELECTED: ", indice)
        
        if  bpy.context.object.animation_data == None or bpy.context.object.animation_data.action == None:
            #print ("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOO -1")
            
            if bpy.context.object.animation_data == None:info1 = "NO 'animation_data'"
            elif bpy.context.object.animation_data.action == None:info1 = "NO 'action'"
            else: info1 = "OBJECT HAS NO ACTION"
            print ("NO ACTION------------")
            info2 = "Tip: Insert Keyframe"

        elif bpy.context.object.animation_data.action:
            #print ("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOO -2")
            AA = bpy.context.object.animation_data.action ##ActiveAction
            
            if AA.get("frame_end") == None:
                durationf = 0
                durations = 0
            else:
                durationf = AA["frame_end"] - AA["frame_start"]
                #durationf = 666

                durations = durationf / bpy.context.scene.render.fps 
            info1 = AA.name 
            info2 = ": " + str(durationf)+ " f. | "+ str(round(durations,6))+ " s. "
     
        else:
            print ("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOO -3")
            info1 = "---"
            info2 = ": ---"
        
        layout.label (text = ": "+ob.name, icon = "OBJECT_DATAMODE")
        layout.label (text = ": "+info1, icon = "ACTION")
        layout.label (text = info2, icon = "PREVIEW_RANGE")
        layout.template_list("ACTION_UL_list", "", bpy.data, "actions", ob, "action_list_index")
        #layout.label (text = str(bpy.data.actions))
        if bpy.context.object.animation_data.action:
            AA = bpy.context.object.animation_data.action ##ActiveAction
            layout.label(text = "Extra Action info:")
            if AA.use_fake_user: fakeuser= " [F]" 
            else: fakeuser= " [x]"
            layout.label(text = "Users: "+ str(AA.users)+fakeuser)
            layout.operator("duplicate.action")
        
        """
        layout.label(text="Active object:")
        #layout.operator("set.actionrange")
        """
        #layout.operator("ttt.action")
        """
        layout.label (text= "   ")
        layout.label (text= "---Danger Zone!---")
        layout.operator("delete.action")
        """
        
        
class OBJECT_OT_SetActionRange(bpy.types.Operator):
    """Sets current timeline range to action"""
    bl_idname = "set.actionrange"
    bl_label = "Set Action range by timeline"
 
    def execute(self, context):
        ActiveAction = bpy.context.scene.objects.active.animation_data.action
        print(ActiveAction)
        
        ActiveAction.use_fake_user = True
        ActiveAction["frame_start"] = bpy.context.scene.frame_preview_start
        ActiveAction["frame_end"] = bpy.context.scene.frame_preview_end
        print ("Actio frame_start: ", ActiveAction["frame_start"], " Action frame_end: ", ActiveAction["frame_end"])
        return{'FINISHED'} 
  
  
class OBJECT_OT_tttAction(bpy.types.Operator):
    """Load Action to Active Object"""
    bl_idname = "duplicate.action"
    bl_label = "Duplicate Action"
    
    def execute(self, context):
        print("TTT2: ")
        newAnim = bpy.data.actions[bpy.context.object.action_list_index].copy()
        bpy.context.object.animation_data.action = newAnim
        #bpy.context.object.action_list_index = 3

        #bpy.context.scene.objects.active.animation_data.action = 
        return{'FINISHED'}   


class OBJECT_OT_tttAction(bpy.types.Operator):
    """Load Action to Active Object"""
    bl_idname = "ttt.action"
    bl_label = "ttt Action"
    
    def execute(self, context):
        print("TTT: ")
        
        return{'FINISHED'}   
    
    
class OBJECT_OT_DeleteAction(bpy.types.Operator):
    """Load Action to Active Object"""
    bl_idname = "delete.action"
    bl_label = "Delete Action"
    def execute(self, context):
        ActionNR = bpy.context.object.action_list_index
        print(bpy.data.actions[ActionNR])
        
        #use_fake_user = True
        
        #bpy.ops.outliner.id_operation(type='DELETE')
        #bpy.data.actions[bpy.context.object.action_list_index].user_clear()
        #bpy.data.actions.remove(bpy.data.actions[ActionNR])
        return{'FINISHED'} 


def register():
    bpy.types.Object.action_list_index = bpy.props.IntProperty(update=update_action_list)
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Object.action_list_index


if __name__ == "__main__":
    register()
    
