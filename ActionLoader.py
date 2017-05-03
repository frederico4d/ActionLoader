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

def set_normal_speed():
    print ("RESET SPEED")
    ActiveAction = bpy.context.scene.objects.active.animation_data.action
    if ActiveAction.get("frame_start") != None:
        bpy.context.scene.frame_start = ActiveAction["frame_start"]
        bpy.context.scene.frame_end = ActiveAction["frame_end"]
    bpy.context.scene.render.frame_map_new = 100

def update_rangemode(self, context):
    
    ActiveAction = context.object.animation_data.action
    print (ActiveAction.frame_range[0])
    print ("RM: "+context.scene.actionloader_rangemode)
    #if ActiveAction.get("frame_start") == None:
    
    if context.scene.actionloader_rangemode == "0":
        if ActiveAction.get("frame_start") == None:
            pass
        else:
            context.scene.frame_preview_start = ActiveAction["frame_start"]
            context.scene.frame_preview_end = ActiveAction["frame_end"]
            context.scene.frame_start = ActiveAction["frame_start"]
            context.scene.frame_end = ActiveAction["frame_end"]  
    elif context.scene.actionloader_rangemode == "1":
        context.scene.frame_preview_start = ActiveAction.frame_range[0]
        context.scene.frame_preview_end = ActiveAction.frame_range[1]
        context.scene.frame_start = ActiveAction.frame_range[0]
        context.scene.frame_end = ActiveAction.frame_range[1]  
    
def quickfix_index():
    print("QUICKFIX")    
    for x in range(len(bpy.data.actions)): 
        if bpy.data.actions[x] == bpy.context.object.animation_data.action:
            print(x)
            bpy.context.object.action_list_index = x
        else:
            pass

def update_action_list_noObj(self, context):
    pass
    
def update_action_list(self, context):
    #updates every time you pick action in the list
    ob = context.object
    
    if context.scene.render.frame_map_new != 100:
        set_normal_speed()
    
    if ob.animation_data == None:
        action = 0 # No Animation data
    elif ob.animation_data.action == None:
        action = 1 # No Action
    else:
        action = 2 # Has Action
    
    if action == 2: # Has action
        ActiveAction = context.scene.objects.active.animation_data.action
        ActiveAction.use_fake_user = True
       
        ## First assign start and end frame props to current action
        if context.scene.actionloader_rangemode == "0":
            if context.scene.use_preview_range: 
                print("bb")
                ActiveAction["frame_start"] = context.scene.frame_preview_start
                ActiveAction["frame_end"] = context.scene.frame_preview_end
            else:
                print("cc")
                ActiveAction["frame_start"] = context.scene.frame_start
                ActiveAction["frame_end"] = context.scene.frame_end   
        else:
            #If it is in key range mode there is no need to set frame range properties for the action
            pass
    elif action == 0:
        
        ob.animation_data_create()

    #then change the action to the picked on the list
    ob.animation_data.action = bpy.data.actions[context.object.action_list_index]
    
    ActiveAction = context.scene.objects.active.animation_data.action
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

    #center stuff on dopesheet etc...
    for area in context.screen.areas:
        if area.type == 'DOPESHEET_EDITOR':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = {'area': area, 'region': region, 'edit_object': context.edit_object}
                    bpy.ops.action.view_all(override)
                        
        elif area.type == 'GRAPH_EDITOR':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = {'area': area, 'region': region, 'edit_object': context.edit_object}
                    bpy.ops.graph.view_all(override)
            
        elif area.type == 'TIMELINE':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = {'area': area, 'region': region, 'edit_object': context.edit_object}
                    bpy.ops.time.view_all(override)    


class ACTION_UL_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        self.use_filter_show = True
        ob = data
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if bpy.context.scene.actionloader_showicons:
                layout.prop(item, "name", text="", emboss=False, icon_value=icon)
            else: 
                layout.prop(item, "name", text="", emboss=False)
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
        
        if context.scene.objects.active != None:
            # Sets icon depending on what is selected and the current mode.
            if context.mode == "OBJECT":
                object_icon = "OUTLINER_OB_"+ str(ob.type)
                
            elif context.mode == "POSE":
                object_icon = "POSE_HLT"
            else:
                object_icon = str(ob.type) + "_DATA"
            
            row = layout.row()
            row.label (text = ob.name, icon = object_icon)
            row.operator ("unselect.object", icon = "X")
            
            """
            if ob.animation_data == None or ob.animation_data.action == None:
                pass
            elif ob.action_list_index > (len(bpy.data.actions)-1) and ob.animation_data.action: 
                #layout.operator ("fix.action", icon = "ERROR")
                pass
            """      
                  
            info2 = "-f. | -s."
            
            if  ob.animation_data == None or ob.animation_data.action == None:
                info2 = "--f. | -s."
                if ob.animation_data == None:
                    layout.label (text = "NO 'animation_data'")
                elif ob.animation_data.action == None:
                    layout.label (text = "NO 'action'")

                layout.label(text = "Tip: Insert Keyframe" , icon = "INFO")     
            elif ob.animation_data.action:
                if ob.action_list_index > (len(bpy.data.actions)-1):
                    action_icon = "ERROR" 
                elif bpy.data.actions[ob.action_list_index] != ob.animation_data.action:
                    # When the active object's action is different than the one listed on the index
                    print("DISTINTODIFERENTE")
                    action_icon = "ERROR"                     
                else: 
                    action_icon = "ACTION"
                
                AA = ob.animation_data.action ##ActiveAction
                
                row = layout.row(align=True)
                row.label (text = AA.name, icon = action_icon)
                    
                if action_icon == "ERROR":
                    row.operator("fix.action", icon = "FILE_TICK")
                else:
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

                durations = durationf / bpy.context.scene.render.fps 
                info1 = AA.name 
                info2 = str(durationf)+ " f. | "+ str(round(durations,6))+ " s. "
            
                layout.label(text =  str(AA.users)+"Users "+fakeuser  , icon = "INFO")   
        
            if context.scene.actionloader_rangemode == '1':
                rangemode_icon = "SPACE2"
            else:
                rangemode_icon = "SPACE3"
              
            row = layout.row(align=True)
            row.label (text = info2, icon = "PREVIEW_RANGE")  
            row.label(icon = rangemode_icon)        
            
            #UIlist
            layout.template_list("ACTION_UL_list", "", bpy.data, "actions", ob, "action_list_index")
        
        elif context.scene.objects.active == None:
            layout.label(text = "Select an Object", icon = "INFO")
            layout.template_list("ACTION_UL_list", "", bpy.data, "actions", context.scene, "action_list_index")
        
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

        if context.scene.actionloader_rangemode == '1':
            rangemode_icon = "SPACE2"
        else:
            rangemode_icon = "SPACE3"
        
        row = layout.row(align=True)
        row.label(text = "Prev Speed:")
        
        if context.scene.render.frame_map_new == 100:
            speednext = "Normal"
        elif context.scene.render.frame_map_new == 200:
            speednext = "1/2x"
        elif context.scene.render.frame_map_new == 400:
            speednext = "1/4x"
        elif context.scene.render.frame_map_new == 800:
            speednext = "1/8x"
        else:
            speednext = "Reset"
        
        row.operator("speeddown.action", text =speednext)
           
        layout.label(text = "Set Frame Range:")
        row = layout.row(align=True)
        row.prop(context.scene, 'actionloader_rangemode', expand=True )
        row.label(icon = rangemode_icon)
        layout.operator("setcustombyrange.action")
        
        #layout.operator("ttt.action", text ="Testa-mos")
        layout.label (text = "Other Tools: ")
        layout.operator("delete.action", icon = "ERROR")
        
        layout.label(text= "Options:")
        layout.prop(bpy.context.scene, "actionloader_showicons", text="Show Icons")
    
      
class OBJECT_OT_SetActionRange(bpy.types.Operator):
    """Sets current timeline range to action"""
    bl_idname = "set.actionrange"
    bl_label = "Set Action range by timeline"
    def execute(self, context):
        scn = context.scene
        ActiveAction = context.scene.objects.active.animation_data.action
        print(ActiveAction)
        ActiveAction.use_fake_user = True
        
        if bpy.context.scene.use_preview_range:
            ActiveAction["frame_start"] = scn.frame_preview_start
            ActiveAction["frame_end"] = scn.frame_preview_end
        else:
            ActiveAction["frame_start"] = scn.frame_start
            ActiveAction["frame_end"] = scn.frame_end
        return{'FINISHED'} 
    
    
class OBJECT_OT_UnselectObject(bpy.types.Operator):
    """Makes Object not active, but you can keep editing the action list"""
    bl_idname = "unselect.object"
    bl_label = ""
    
    def execute(self, context):
        context.scene.objects.active = None
        return{'FINISHED'}   


class OBJECT_OT_DuplicateAction(bpy.types.Operator):
    """Duplicate Action"""
    bl_idname = "duplicate.action"
    bl_label = ""
    
    def execute(self, context):
        newAnim = bpy.data.actions[context.object.action_list_index].copy()
        context.object.animation_data.action = newAnim
        quickfix_index()
        return{'FINISHED'}   

class OBJECT_OT_UnlinkAction(bpy.types.Operator):
    """Unlinks Action from Active Object"""
    bl_idname = "unlinks.action"
    bl_label = ""
    
    def execute(self, context):
        context.object.animation_data.action = None
        return{'FINISHED'}   


class OBJECT_OT_fixsync(bpy.types.Operator):
    """Quick fix for unmaching action in Action Loader list"""
    bl_idname = "fix.action"
    bl_label = "fix"
    
    def execute(self, context):
        quickfix_index()
        return{'FINISHED'}  


class OBJECT_OT_speedup(bpy.types.Operator):
    """Toggles between, 1/2x - 1/4x - 1/8x and Normal speeds for preview only - uses the 'Time Remapping' values"""
    bl_idname = "speeddown.action"
    bl_label = ""
    
    def execute(self, context):
        bpy.context.scene.use_preview_range = False
        #context.scene.frame_preview_end = ActiveAction["frame_end"] 
        ActiveAction = context.object.animation_data.action
        
        if context.scene.render.frame_map_new == 100:
            context.scene.frame_start = ActiveAction["frame_start"]*2
            context.scene.frame_end = ActiveAction["frame_end"]*2
            context.scene.render.frame_map_new = 200
            context.scene.frame_current = context.scene.frame_current*2
        elif context.scene.render.frame_map_new == 200:
            context.scene.frame_start = ActiveAction["frame_start"]*4
            context.scene.frame_end = ActiveAction["frame_end"]*4
            context.scene.render.frame_map_new = 400
            context.scene.frame_current = context.scene.frame_current*2
        elif context.scene.render.frame_map_new == 400:
            context.scene.frame_start = ActiveAction["frame_start"]*8
            context.scene.frame_end = ActiveAction["frame_end"]*8
            context.scene.render.frame_map_new = 800
            context.scene.frame_current = context.scene.frame_current*2
        else:
            set_normal_speed()
        return{'FINISHED'} 


class OBJECT_OT_customByRange(bpy.types.Operator):
    """Sets the custom range by the action's frame_range (first and last keyframes)"""
    bl_idname = "setcustombyrange.action"
    bl_label = "Set Frame Range"
    
    def execute(self, context):
        ActiveAction = context.object.animation_data.action
        ActiveAction["frame_start"] = ActiveAction.frame_range[0]
        ActiveAction["frame_end"] = ActiveAction.frame_range[1]
        update_rangemode(self, bpy.context)
        return{'FINISHED'} 
    
class OBJECT_OT_ttt(bpy.types.Operator):
    """Unlinks Action from Active Object"""
    bl_idname = "ttt.action"
    bl_label = ""
    
    def execute(self, context):
        bpy.context.scene.use_preview_range = False
        #context.scene.frame_preview_end = ActiveAction["frame_end"] 
        ActiveAction = context.object.animation_data.action
        if context.scene.render.frame_map_new == 200:
            context.scene.render.frame_map_new = 100
            context.scene.frame_start = ActiveAction["frame_start"] 
            context.scene.frame_end = ActiveAction["frame_end"] 
        else:
            print("conversa")
            context.scene.frame_start = ActiveAction["frame_start"]*2
            context.scene.frame_end = ActiveAction["frame_end"]*2
            context.scene.render.frame_map_new = 200
            context.scene.frame_current = context.scene.frame_current*2
        return{'FINISHED'}   

    
class OBJECT_OT_DeleteAction(bpy.types.Operator):
    """ WARNING: Deletes Action from Blender File"""
    bl_idname = "delete.action"
    bl_label = "Delete Action"
    def execute(self, context):
        if context.scene.objects.active == None:
            ActionNR = context.scene.action_list_index
        else:
            ActionNR = context.object.action_list_index
        AA = bpy.data.actions[ActionNR]
        
        bpy.data.actions.remove(AA, True)
        
        #AA.use_fake_user = False
        #AA.user_clear()
        return{'FINISHED'} 


def register():
    bpy.types.Object.action_list_index = bpy.props.IntProperty(update=update_action_list)
    bpy.types.Scene.action_list_index = bpy.props.IntProperty(update=update_action_list_noObj)
    
    enum_items = (
    ('0',' Custom','Sets Frame Range of action by the current Frame Range'),
    ('1','Keyframes',"Sets Frame Range by action's first and last keyframe")
    )
    bpy.types.Scene.actionloader_rangemode = bpy.props.EnumProperty(items = enum_items, update=update_rangemode)
    
    bpy.types.Scene.actionloader_showicons = bpy.props.BoolProperty(name="Show icons", description="Show icons in Action Loader Addon",default = True)
    
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Object.action_list_index
    del bpy.types.Scene.action_list_index
    del bpy.types.Scene.actionloader_showicons
    
if __name__ == "__main__":
    register()
    
