bl_info = {
    "name": "Action Loader",
    "author": "Frederico Martins - Frankenstein",
    "version": (1, 4),
    "blender": (2, 78, 0),
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
    if bpy.context.scene.actionloader_rangemode == "0":
        print("aa")
        if bpy.context.scene.use_preview_range: 
            print("bb")
            ActiveAction["frame_start"] = bpy.context.scene.frame_preview_start
            ActiveAction["frame_end"] = bpy.context.scene.frame_preview_end
        else:
            print("cc")
            ActiveAction["frame_start"] = bpy.context.scene.frame_start
            ActiveAction["frame_end"] = bpy.context.scene.frame_end  
    else:
        #If it is in key range mode there is no need to set frame range properties for the action
        pass

    #then change the action to the picked on the list
    bpy.context.scene.objects.active.animation_data.action = bpy.data.actions[bpy.context.object.action_list_index]
    ActiveAction = bpy.context.scene.objects.active.animation_data.action
    ActiveAction.use_fake_user = True
    
    # Changes the range on the scene
    print ("AA")
    if ActiveAction.get("frame_start") == None:
        print("AB")
        if context.scene.actionloader_rangemode == "0":
            print("ABC")
            
    else:
        if context.scene.actionloader_rangemode == "0":
            print ("DD")
            context.scene.frame_preview_start = ActiveAction["frame_start"]
            context.scene.frame_preview_end = ActiveAction["frame_end"] 
            context.scene.frame_start = ActiveAction["frame_start"]
            context.scene.frame_end = ActiveAction["frame_end"] 
        
        elif context.scene.actionloader_rangemode == "1":
            print ("EE")
            context.scene.frame_preview_start = ActiveAction.frame_range[0]
            context.scene.frame_preview_end = ActiveAction.frame_range[1]
            context.scene.frame_start = ActiveAction.frame_range[0]
            context.scene.frame_end = ActiveAction.frame_range[1]  
        """
        print ("BB")
        if context.scene.use_preview_range: 
            print ("CC")
            if context.scene.actionloader_rangemode == "0":
                print ("DD")
                context.scene.frame_preview_start = ActiveAction["frame_start"]
                context.scene.frame_preview_end = ActiveAction["frame_end"] 
            elif context.scene.actionloader_rangemode == "1":
                print ("EE")
                context.scene.frame_preview_start = ActiveAction.frame_range[0]
                context.scene.frame_preview_end = ActiveAction.frame_range[1]
                
        elif context.scene.use_preview_range == False:
            print ("FF")
            if context.scene.actionloader_rangemode == "0":
                print ("GG")
                context.scene.frame_start = ActiveAction["frame_start"]
                context.scene.frame_end = ActiveAction["frame_end"]
            elif context.scene.actionloader_rangemode == "1":
                print ("HH")
                context.scene.frame_start = ActiveAction.frame_range[0]
                context.scene.frame_end = ActiveAction.frame_range[1]
        """
    # center stuff on dopesheet etc...
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
        self.use_filter_show = True
        ob = data
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False, icon_value=icon)
        elif self.layout_type in {'GRID'}:
            pass
        global filter_name
        filter_name = self.filter_name


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
        animation = True
        
        if bpy.context.scene.objects.active != None:
            layout.label (text = ": "+ob.name, icon = "OBJECT_DATAMODE")
            info2 = "-f. | -s."
            if  ob.animation_data == None or ob.animation_data.action == None:
                info2 = "--f. | -s."
                if ob.animation_data == None:
                    layout.label (text = "NO 'animation_data'", icon = "ACTION")
                elif ob.animation_data.action == None:
                    layout.label (text = "NO 'action'", icon = "ACTION")

                layout.label(text = "Tip: Insert Keyframe" , icon = "INFO")     
            elif ob.animation_data.action:
                AA = ob.animation_data.action ##ActiveAction
                
                row = layout.row(align=True)
                row.label (text = ": "+AA.name, icon = "ACTION")
                row.operator("duplicate.action", icon = "ZOOMIN")
                row.operator("unlinks.action", icon = "X")
                
                if AA.use_fake_user:
                    fakeuser= " [F]" 
                else:
                    fakeuser= " [x]"
                if AA.get("frame_end") == None:
                    durationf = 0
                    durations = 0
                else:
                    durationf = AA["frame_end"] - AA["frame_start"]
                    #durationf = 666

                durations = durationf / bpy.context.scene.render.fps 
                info1 = AA.name 
                info2 = str(durationf)+ " f. | "+ str(round(durations,6))+ " s. "
                
                layout.label(text = "Users: "+ str(AA.users)+fakeuser , icon = "INFO")   
            
            layout.label (text = ": "+info2, icon = "PREVIEW_RANGE")

        #UIlist
        layout.template_list("ACTION_UL_list", "", bpy.data, "actions", ob, "action_list_index")
        
        
        action_names= []
        for x in range (len(bpy.data.actions)):
            action_names.append(bpy.data.actions[x].name.lower())

        filtered_actions = [k for k in action_names if filter_name.lower() in k]
        
        total_anims=len(bpy.data.actions.items())
        listed_anims =len(filtered_actions)
        
        if filter_name == "":
            layout.label(text = "Total: "+ str(total_anims) +" anims", icon = "INFO")        
        else:
            layout.label(text = "Listed: "+ str(listed_anims)+ " of " +str(total_anims) +" anims", icon = "INFO")        
     
        
        layout.label(text = "Action range by:")
        enum_items = (('0',' Current range','Sets Frame Range of action by the current Frame Range'),('1',' Key range',"Sets Frame Range by action's first and last keyframe"))
        bpy.types.Scene.actionloader_rangemode = bpy.props.EnumProperty(items = enum_items)
      
        layout.prop(context.scene, 'actionloader_rangemode', expand=True )
        
        #layout.operator("ttt.action")
        layout.label (text = "Other Tools: ")
        row = layout.row(align=True)
        row.label (text = "Danger: ")
        row.operator("delete.action")
        
      
class OBJECT_OT_SetActionRange(bpy.types.Operator):
    """Sets current timeline range to action"""
    bl_idname = "set.actionrange"
    bl_label = "Set Action range by timeline"
 
    def execute(self, context):
        ActiveAction = bpy.context.scene.objects.active.animation_data.action
        print(ActiveAction)
        
        ActiveAction.use_fake_user = True
        
        if bpy.context.scene.use_preview_range:
            ActiveAction["frame_start"] = bpy.context.scene.frame_preview_start
            ActiveAction["frame_end"] = bpy.context.scene.frame_preview_end
        else:
            ActiveAction["frame_start"] = bpy.context.scene.frame_start
            ActiveAction["frame_end"] = bpy.context.scene.frame_end
        return{'FINISHED'} 


class OBJECT_OT_DuplicateAction(bpy.types.Operator):
    """Duplicate Action"""
    bl_idname = "duplicate.action"
    bl_label = ""
    
    def execute(self, context):
        print("TTT2: ")
        newAnim = bpy.data.actions[bpy.context.object.action_list_index].copy()
        bpy.context.object.animation_data.action = newAnim
        #bpy.context.object.action_list_index = 3
        #bpy.context.scene.objects.active.animation_data.action = 
        return{'FINISHED'}   

class OBJECT_OT_UnlinkAction(bpy.types.Operator):
    """Unlinks Action from Active Object"""
    bl_idname = "unlinks.action"
    bl_label = ""
    
    def execute(self, context):
        bpy.context.object.animation_data.action = None
        return{'FINISHED'}   



class OBJECT_OT_tttAction(bpy.types.Operator):
    """Unlinks Action from Active Object"""
    bl_idname = "ttt.action"
    bl_label = ""
    
    def execute(self, context):
        print("TTT: ")
        bpy.context.object.animation_data.action = None
        return{'FINISHED'}   
    
    
class OBJECT_OT_DeleteAction(bpy.types.Operator):
    """ WARNING: Deletes Action from Blender File"""
    bl_idname = "delete.action"
    bl_label = "Delete Action"
    def execute(self, context):
        ActionNR = bpy.context.object.action_list_index
        AA = bpy.data.actions[ActionNR]
        
        bpy.data.actions.remove(AA, True)
        
        #AA.use_fake_user = False
        #AA.user_clear()
        return{'FINISHED'} 


def register():
    bpy.types.Object.action_list_index = bpy.props.IntProperty(update=update_action_list)
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Object.action_list_index


if __name__ == "__main__":
    register()
    
