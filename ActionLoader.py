bl_info = {
    "name": "Action Loader",
    "author": "Frederico Martins",
    "version": (1, 8),
    "blender": (2, 81, 0),
    "location": "View3D > Tools > Animation",
    "description": "Lists all Actions and assigns it to active object",
    "warning": "",
    "wiki_url": "https://github.com/frederico4d/ActionLoader",
    "tracker_url": "https://github.com/frederico4d/ActionLoader/issues",
    "category": "Animation",
    }

## TODO

### novas funcoes
## meter mais paineis duplicaveis em vez de so 2?

## meter o action loader nas properties ou em outro lado 
#para se puder ver num painel separado, em outro ecra etc...

### optimizações

import bpy
import inspect
import sys
import os
global extra_info
extra_info = False

filter_name = ''
filter_name2 = ''


def set_prevspeed(self, value):
    global prev_mode 
    global old_prevspeed 
    old_prevspeed = bpy.context.scene.actionloader_speedprev
    if bpy.context.scene.actionloader_speedprev == "0":
        print ("ZERO")
        prev_mode = bpy.context.scene.use_preview_range
    self["testprop"] = value
    
  
def get_prevspeed(self):
    #print("get")
    try:
        return self["testprop"];
    except:
        return 0;
    


def update_prevspeed(self, context):
    speed = bpy.context.scene.actionloader_speedprev
    
    print("SPEEDCHANGE")
    ob = context.active_object
    scn = context.scene
    ActiveAction = ob.animation_data.action
        
    if scn.actionloader_rangemode == "0":
        sframe = ActiveAction["frame_start"]
        eframe = ActiveAction["frame_end"]
    else:
        sframe = ActiveAction.frame_range[0]
        eframe = ActiveAction.frame_range[1]
    
    print("OLD: ",old_prevspeed)
    
    if speed == "0":
        scn.frame_start = sframe
        scn.frame_end = eframe
        scn.render.frame_map_new = 100
        if old_prevspeed == "1":
            scn.frame_current = scn.frame_current / 2 
        elif old_prevspeed == "2":
            scn.frame_current = scn.frame_current / 4 
        elif old_prevspeed == "3":
            scn.frame_current = scn.frame_current / 8
        scn.use_preview_range = prev_mode
        
    elif speed == "1":
        scn.frame_start = sframe*2
        scn.frame_end = eframe*2
        scn.render.frame_map_new = 200
        if old_prevspeed == "0":
            scn.frame_current = scn.frame_current * 2
        elif old_prevspeed == "2":
            scn.frame_current = scn.frame_current / 2 
        elif old_prevspeed == "3":
            scn.frame_current = scn.frame_current / 4 
        scn.use_preview_range = False
    
    elif speed == "2":
        scn.frame_start = sframe*4
        scn.frame_end = eframe*4
        scn.render.frame_map_new = 400
        if old_prevspeed == "0":
            scn.frame_current = scn.frame_current * 4
        elif old_prevspeed == "1":
            scn.frame_current = scn.frame_current * 2
        elif old_prevspeed == "3":
            scn.frame_current = scn.frame_current / 2
        scn.use_preview_range = False
    
    elif speed == "3":
        scn.frame_start = sframe*8
        scn.frame_end = eframe*8
        scn.render.frame_map_new = 800
        if old_prevspeed == "0":
            scn.frame_current = scn.frame_current * 8
        elif old_prevspeed == "1":
            scn.frame_current = scn.frame_current * 4
        elif old_prevspeed == "2":
            scn.frame_current = scn.frame_current * 2
        scn.use_preview_range = False
    

def set_normal_speed():
    scn = bpy.context.scene
    if bpy.context.object == None or bpy.context.object.animation_data == None or bpy.context.object.animation_data.action == None:
        pass
    else:
        ActiveAction = bpy.context.active_object.animation_data.action
        if ActiveAction.get("frame_start") != None:
            scn.frame_start = ActiveAction["frame_start"]
            scn.frame_end = ActiveAction["frame_end"]
        else:
            scn.frame_start = ActiveAction.frame_range[0]
            scn.frame_end = ActiveAction.frame_range[1]

    scn.use_preview_range = prev_mode
    scn.actionloader_speedprev = '0'
    scn.render.frame_map_new = 100
 

def update_rangemode(self, context):
    ob = context.active_object
    ActiveAction = ob.animation_data.action
    
    if context.scene.actionloader_rangemode == "0":
        if ActiveAction.get("frame_start") == None:
            pass
        else:
            context.scene.frame_preview_start = ActiveAction["frame_start"]
            context.scene.frame_preview_end = ActiveAction["frame_end"]
            context.scene.frame_start = ActiveAction["frame_start"]
            context.scene.frame_end = ActiveAction["frame_end"]  
    elif context.scene.actionloader_rangemode == "1":
        if ActiveAction == None:
            pass
        else:
            context.scene.frame_preview_start = ActiveAction.frame_range[0]
            context.scene.frame_preview_end = ActiveAction.frame_range[1]
            context.scene.frame_start = ActiveAction.frame_range[0]
            context.scene.frame_end = ActiveAction.frame_range[1]  
    
def update_action_list_noObj(self, context):
    pass

def save_action_extras():
    scn = bpy.context.scene
    ob = bpy.context.active_object
    if ob:
        ActiveAction = ob.animation_data.action
    else:
        ActiveAction = bpy.data.actions[scn.action_list_index]
    
    ActiveAction.use_fake_user = True
       
    ## Assign start and end frame props to current action
    if scn.actionloader_rangemode == "0" and scn.actionloader_autorange:
        if scn.use_preview_range: 
            ActiveAction["frame_start"] = scn.frame_preview_start
            ActiveAction["frame_end"] = scn.frame_preview_end
        else:
            ActiveAction["frame_start"] = scn.frame_start
            ActiveAction["frame_end"] = scn.frame_end   
    
    #Saves current markers to action
    if scn.actionloader_markers and ob:
        save_markers_to_action()    

def update_action_list(self, context):
    #updates every time you pick action in the list
    ob = context.active_object
    #ob = context.object
    scn = context.scene
    if scn.render.frame_map_new != 100:
        set_normal_speed()
    
    if ob.animation_data == None:
        action = 0 # No Animation data
    elif ob.animation_data.action == None:
        action = 1 # No Action
    else:
        action = 2 # Has Action
    
    if action == 2: # Has action
        save_action_extras()
    elif action == 0: # No Animation data
        ob.animation_data_create()

    #then change the action to the picked on the list
    ob.animation_data.action = bpy.data.actions[ob.action_list_index]
    
    ActiveAction = context.active_object.animation_data.action
    ActiveAction.use_fake_user = True
    
    # Changes the range on the scene
    
    if ActiveAction.get("frame_start") != None and scn.actionloader_autorange:
        if context.scene.actionloader_rangemode == "0":
            scn.frame_preview_start = ActiveAction["frame_start"]
            scn.frame_preview_end = ActiveAction["frame_end"] 
            scn.frame_start = ActiveAction["frame_start"]
            scn.frame_end = ActiveAction["frame_end"] 
        
        elif context.scene.actionloader_rangemode == "1":
            scn.frame_preview_start = ActiveAction.frame_range[0]
            scn.frame_preview_end = ActiveAction.frame_range[1]
            scn.frame_start = ActiveAction.frame_range[0]
            scn.frame_end = ActiveAction.frame_range[1]  

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
    
    if scn.actionloader_markers == True:
        change_timelinemarkers_from_action()


class ACTION_UL_list2(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        self.use_filter_show = True
        ob = bpy.context.active_object
        #ob = bpy.context.object
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if bpy.context.scene.actionloader_showicons:
                layout.prop(item, "name", text="", emboss=False, icon_value=icon)
            else: 
                layout.prop(item, "name", text="", emboss=False)
                #layout.operator("delete.action", text="", icon = "ERROR").delaction = bpy.data.actions[ob.action_list_index].name
                #layout.operator("ttt.action", text ="T").nome = str(self._DATA)
                #layout.label(text = "", icon = "ERROR")
        elif self.layout_type in {'GRID'}:
            pass
        global filter_name2
        filter_name2 = self.filter_name
        
class ACTION_UL_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        self.use_filter_show = True
        
        if item.get("frame_end") == None:
                durationf = 0
                durations = 0
        else:
            durationf = item["frame_end"] - item["frame_start"]
            
        # Draw Info!  
        durations = durationf / bpy.context.scene.render.fps 
        info2 = str(durationf)+ " f. | "+ str(round(durations,6))+ " s. "
        
        
        if item.use_fake_user == True:
            fakeuser = "F"
        else:
            fakeuser = "X"
        
        info = str(item.users)+ fakeuser + " | " + str(len(item.pose_markers)) + "m | " + str(durationf) + "f | "+ str(round(durations,6))+ "s"
                        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if bpy.context.scene.actionloader_showicons:
                layout.prop(item, "name", text="", emboss=False, icon_value=icon)
            else: 
                layout.prop(item, "name", text="", emboss=False)
                #layout.operator("delete.action", text="", icon = "ERROR").delaction = bpy.data.actions[ob.action_list_index].name
                #layout.operator("ttt.action", text ="T").nome = str(self._DATA)
            if extra_info:
                layout.label(text = info)
            
        elif self.layout_type in {'GRID'}:
            pass
        global filter_name
        filter_name = self.filter_name


class ActionLoaderPanel(bpy.types.Panel):
    """Creates a Panel in the Animation tab of the 3D View's Tools"""
    bl_label = "Action Loader"
    bl_idname = "OBJECT_PT_action_loader"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Animation"
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        ob = context.active_object
        #ob = context.object
        
        animation = True
        if context.active_object != None:
            # Sets icon depending on what is selected and the current mode.
            if context.mode == "OBJECT":
                object_icon = "OUTLINER_OB_"+ str(ob.type)
                
            elif context.mode == "POSE":
                object_icon = "POSE_HLT"
            else:
                object_icon = str(ob.type) + "_DATA"
            
            row = layout.row(align = True)
            row.label (text = ob.name, icon = object_icon)
                        
            if ob.animation_data and ob.animation_data.action:
                if ob.animation_data.action.fcurves.find('location', index=0):
                    if ob.animation_data.action.fcurves.find('location', index=0).mute == False:
                        mute_ico = "MUTE_IPO_OFF"
                    else:
                        mute_ico = "MUTE_IPO_ON"
                    row.operator("muteloc.action", icon = mute_ico)
            
            row.operator ("object.deselect", icon = "X")
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
                    row.operator("duplicate.action", icon = "DUPLICATE")
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
                
                # Draw Info!            
                row = layout.row(align=True)
                row.label(text =  str(AA.users)+"Users "+fakeuser + " | " + str(len(AA.pose_markers))+"Markers", icon = "INFO")   
                row.operator("renderprev.action", icon = "RENDER_ANIMATION")
                
            if context.scene.actionloader_rangemode == '1':
                rangemode_icon = "KEYTYPE_MOVING_HOLD_VEC"
            else:
                rangemode_icon = "HANDLETYPE_FREE_VEC"
              
            row = layout.row(align=True)
            row.label (text = info2, icon = "PREVIEW_RANGE")  
            row.label(icon = rangemode_icon)        
            list_context = ob

        elif context.active_object == None and len(bpy.data.actions) >=1:
            
            ListedAction = bpy.data.actions[bpy.context.scene.action_list_index]
            layout.label(text = "Tip: Select an Object", icon = "INFO")
            
            row = layout.row(align=True)
            row.label (text = ListedAction.name, icon = "ACTION")
            row.operator("duplicate.action", icon = "DUPLICATE")
                        
            if ListedAction.use_fake_user:
                    fakeuser= " [F]" 
            else:
                    fakeuser= " [x]"
            if ListedAction.get("frame_end") == None:
                durationf = 0
                durations = 0
            else:
                durationf = ListedAction["frame_end"] - ListedAction["frame_start"]
            
            # Draw Info!  
            layout.label(text =  str(ListedAction.users)+"Users "+fakeuser + " | " + str(len(ListedAction.pose_markers))+"Markers", icon = "INFO")   
            
            durations = durationf / bpy.context.scene.render.fps 
            info2 = str(durationf)+ " f. | "+ str(round(durations,6))+ " s. "
            
            if context.scene.actionloader_rangemode == '1':
                rangemode_icon = "KEYTYPE_MOVING_HOLD_VEC"
            else:
                rangemode_icon = "HANDLETYPE_FREE_VEC"
              
            row = layout.row(align=True)
            row.label (text = info2, icon = "PREVIEW_RANGE")  
            row.label(icon = rangemode_icon)              
            
            list_context = scn
   
        else:
            layout.label (text= "Just start animating!", icon = "INFO")  
            list_context = scn
        
        #UIList - no object
        row = layout.row(align=True)
        row.template_list("ACTION_UL_list", "", bpy.data, "actions", list_context, "action_list_index")
        if bpy.context.scene.actionloader_DualView:
            row.template_list("ACTION_UL_list2", "", bpy.data, "actions", list_context, "action_list_index")
        
        ## First View!!!!!!!!!!!!!!!!!!!1
        action_names= []
        for x in range (len(bpy.data.actions)):
            action_names.append(bpy.data.actions[x].name.lower())

        filtered_actions = [k for k in action_names if filter_name.lower() in k]
        
        total_anims=len(bpy.data.actions.items())
        listed_anims =len(filtered_actions)
        
        row = layout.row(align=True)
        
        if filter_name == "":
            row.label(text = str(total_anims) +" anims total", icon = "INFO")        
        else:
            row.label(text = str(listed_anims)+ " of " +str(total_anims) +" anims", icon = "INFO")
        
        ## DualView!!!!!!!!!!!!!!!!!!!!2
        if bpy.context.scene.actionloader_DualView:
            action_names= []
            for x in range (len(bpy.data.actions)):
                action_names.append(bpy.data.actions[x].name.lower())

            filtered_actions = [k for k in action_names if filter_name2.lower() in k]
            
            total_anims=len(bpy.data.actions.items())
            listed_anims =len(filtered_actions)
        
            if filter_name2 == "":
                row.label(text = str(total_anims) +" anims total", icon = "INFO")        
            else:
                row.label(text = str(listed_anims)+ " of " +str(total_anims) +" anims", icon = "INFO")      
        
        # DUAL VIEW ICON BT
        if scn.actionloader_DualView:
            dual_icon = "TRACKING_CLEAR_BACKWARDS"
        else:    
            dual_icon = "MOD_ARRAY"
        row.prop(scn, 'actionloader_DualView', text = "", icon = dual_icon)
        
        #Icons for Rangemode
        if context.scene.actionloader_rangemode == '1':
            rangemode_icon = "KEYTYPE_MOVING_HOLD_VEC"
        else:
            rangemode_icon = "HANDLETYPE_FREE_VEC"
        
        layout.label(text = "Prev Speed:")
        
        layout.prop(context.scene, 'actionloader_speedprev', expand=True)
             
        layout.label(text = "Set Frame Range:")
        row = layout.row(align=True)
        row.prop(context.scene, 'actionloader_rangemode', expand=True )
        row.label(icon = rangemode_icon)
        layout.operator("setcustombyrange.action", icon = "FILE_REFRESH")
        
        #layout.operator("ttt.action", text ="TTTTTT###TTTTTTTT").nome = "conho"
        layout.label (text = "Other Tools: ")
        layout.operator("delete.action", icon = "ERROR")
        #.delaction = bpy.data.actions[ob.action_list_index].name

        #layout.label (text = "Render Preview:")
        #layout.operator("renderprev.action",text = "Render Preview", icon = "RENDER_ANIMATION")
        
        layout.label(text= "Options:")
        
        layout.prop(scn, "actionloader_showicons", text="Show Icons")
        layout.prop(scn, "actionloader_autorange", text="Set Auto Range")
        layout.prop(scn, "actionloader_markers", text="Use Action Markers")


class OBJECT_OT_SetActionRange(bpy.types.Operator):
    """Sets current timeline range to action"""
    bl_idname = "set.actionrange"
    bl_label = "Set Action range by timeline"
    def execute(self, context):
        scn = context.scene
        ActiveAction = context.active_object.animation_data.action
        print(ActiveAction)
        ActiveAction.use_fake_user = True
        
        if bpy.context.scene.use_preview_range:
            ActiveAction["frame_start"] = scn.frame_preview_start
            ActiveAction["frame_end"] = scn.frame_preview_end
        else:
            ActiveAction["frame_start"] = scn.frame_start
            ActiveAction["frame_end"] = scn.frame_end
        return{'FINISHED'} 


class OBJECT_OT_DeselectObject(bpy.types.Operator):
    """Makes Object not active, but you can keep editing the action list"""
    bl_idname = "object.deselect"
    bl_label = ""

    def execute(self, context):
        if context.scene.action_list_index < 0:
            context.scene.action_list_index = 0

        for obj in context.selected_objects:
            obj.select_set(False)
        return {'FINISHED'}


class OBJECT_OT_DuplicateAction(bpy.types.Operator):
    """Duplicate Action"""
    bl_idname = "duplicate.action"
    bl_label = ""
    
    def execute(self, context):
        scn = bpy.context.scene
        ob = context.active_object
        save_action_extras()
        """
        #Saves current markers to action
        if bpy.context.scene.actionloader_markers:
            save_markers_to_action()

        ### Saves extra stuff on current action
        ActiveAction = scn.objects.active.animation_data.action
        ActiveAction.use_fake_user = True
       
        ## Assign start and end frame props to current action
        if scn.actionloader_rangemode == "0" and scn.actionloader_autorange:
            if scn.use_preview_range: 
                print("bb")
                ActiveAction["frame_start"] = scn.frame_preview_start
                ActiveAction["frame_end"] = scn.frame_preview_end
            else:
                print("cc")
                ActiveAction["frame_start"] = scn.frame_start
                ActiveAction["frame_end"] = scn.frame_end   
        """ 
            
        if ob == None:
            newAnim = bpy.data.actions[scn.action_list_index].copy()
        else:
            newAnim = bpy.data.actions[bpy.context.object.action_list_index].copy()
            ob.animation_data.action = newAnim
            quickfix_index()
        return{'FINISHED'}   


class OBJECT_OT_UnlinkAction(bpy.types.Operator):
    """Unlinks Action from Active Object"""
    bl_idname = "unlinks.action"
    bl_label = ""
    
    def execute(self, context):
        ob = context.active_object
        
        save_action_extras()
        ob.animation_data.action = None
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
        ob = context.active_object
        #ob = context.object
        ActiveAction = ob.animation_data.action
        global prev_mode 
        
        if ob == None or ob.animation_data == None or ActiveAction == None:
            bpy.context.scene.render.frame_map_new = 100
        else:
            
            if context.scene.actionloader_rangemode == "0":
                sframe = ActiveAction["frame_start"]
                eframe = ActiveAction["frame_end"]
            else:
                sframe = ActiveAction.frame_range[0]
                eframe = ActiveAction.frame_range[1]
            
            if context.scene.render.frame_map_new == 100:
                context.scene.frame_start = sframe*2
                context.scene.frame_end = eframe*2
                context.scene.render.frame_map_new = 200
                context.scene.frame_current = context.scene.frame_current*2
                
                prev_mode = bpy.context.scene.use_preview_range 
                context.scene.use_preview_range = False
            elif context.scene.render.frame_map_new == 200:
                context.scene.frame_start = sframe*4
                context.scene.frame_end = eframe*4
                context.scene.render.frame_map_new = 400
                context.scene.frame_current = context.scene.frame_current*2
                context.scene.use_preview_range = False
            elif context.scene.render.frame_map_new == 400:
                context.scene.frame_start = sframe*8
                context.scene.frame_end = eframe*8
                context.scene.render.frame_map_new = 800
                context.scene.frame_current = context.scene.frame_current*2
                context.scene.use_preview_range = False
            else:
                bpy.context.scene.use_preview_range = prev_mode
                set_normal_speed()
        return{'FINISHED'} 


class OBJECT_OT_customByRange(bpy.types.Operator):
    """Sets the custom range by the action's frame_range (first and last keyframes)"""
    bl_idname = "setcustombyrange.action"
    bl_label = "Set Frame Range"
    
    def execute(self, context):
        ob = context.active_object
        if not ob.animation_data:
            return {'FINISHED'}

        ActiveAction = ob.animation_data.action
        ActiveAction["frame_start"] = ActiveAction.frame_range[0]
        ActiveAction["frame_end"] = ActiveAction.frame_range[1]
        update_rangemode(self, bpy.context)
        return{'FINISHED'} 


class OBJECT_OT_renderprev(bpy.types.Operator):
    """Render Preview with Action Name (set output path to end in "/", without filename)"""
    bl_idname = "renderprev.action"
    bl_label = ""

    directory: bpy.props.StringProperty(name="Export directory", subtype="DIR_PATH")
    filepath: bpy.props.StringProperty(name="Export filepath", subtype="FILE_PATH")
    filename: bpy.props.StringProperty()

    def execute(self, context):
        scn = context.scene
        original_fp = scn.render.filepath
        original_fformat = scn.render.image_settings.file_format
        scn.render.filepath = os.path.splitext(os.path.join(self.directory, self.filepath))[0]

        scn.render.image_settings.file_format = "FFMPEG"
        scn.render.ffmpeg.format = "MPEG4"
        scn.render.ffmpeg.codec = "H264"

        bpy.ops.render.opengl(animation=True)

        scn.render.filepath = original_fp
        scn.render.image_settings.file_format = original_fformat

        return{'FINISHED'}

    def invoke(self, context, event):
        self.filename = context.object.animation_data.action.name + '.mp4'
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OBJECT_OT_muter(bpy.types.Operator):
    """Mutes Location"""
    bl_idname = "muteloc.action"
    bl_label = ""
    def execute(self, context):
        ob = context.active_object
        AA = ob.animation_data.action
        mute_to = False
        if AA.fcurves.find('location', index=0).mute == False:
            mute_to = True
        # Mutes Location
        AA.fcurves.find('location', index=0).mute = mute_to
        AA.fcurves.find('location', index=1).mute = mute_to
        AA.fcurves.find('location', index=2).mute = mute_to
        # Hides Location
        AA.fcurves.find('location', index=0).hide = mute_to
        AA.fcurves.find('location', index=1).hide = mute_to
        AA.fcurves.find('location', index=2).hide = mute_to
        # Locks Location
        AA.fcurves.find('location', index=0).lock = mute_to
        AA.fcurves.find('location', index=1).lock = mute_to
        AA.fcurves.find('location', index=2).lock = mute_to
        return{'FINISHED'}   


class OBJECT_OT_ttt(bpy.types.Operator):
    """TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"""
    bl_idname = "ttt.action"
    bl_label = ""
    
    nome : bpy.props.StringProperty()
    def execute(self, context):
        print (self.nome)
        return{'FINISHED'}   

    
class OBJECT_OT_DeleteAction(bpy.types.Operator):
    """ WARNING: Deletes Action from Blender File"""
    bl_idname = "delete.action"
    bl_label = "Delete Action"
    #delaction = bpy.props.StringProperty()
    def execute(self, context):
        #set_normal_speed()
        if not bpy.data.actions:
            return {'FINISHED'}

        ob = context.active_object
        if ob == None:
            ActionNR = context.scene.action_list_index
        else:
            ActionNR = context.object.action_list_index
        AA = bpy.data.actions[ActionNR] 
        
        if ob:
            ob.action_list_index = bpy.context.object.action_list_index-1
        else:
            bpy.context.scene.action_list_index = bpy.context.scene.action_list_index-1    
        
        bpy.data.actions.remove(AA, do_unlink=True)
        #bpy.data.actions.remove(bpy.data.actions[self.delaction], True)
        return{'FINISHED'} 


def change_timelinemarkers_from_action():
    ob = bpy.context.object
    scn = bpy.context.scene
    # remove markers from timeline  
    for ai in range(len(scn.timeline_markers)):
        scn.timeline_markers.remove(scn.timeline_markers[0])
    
    #adds action markers to timeline
    for bi in range(len(ob.animation_data.action.pose_markers)):
        scn.timeline_markers.new(ob.animation_data.action.pose_markers[bi].name, ob.animation_data.action.pose_markers[bi].frame)    


def save_markers_to_action():
    ob = bpy.context.active_object
    AA = ob.animation_data.action
    #delete pose markers from the action
    for i in range(len(AA.pose_markers)):
        AA.pose_markers.remove(AA.pose_markers[0])
    # assign pose markers from timeline markers
    for i in range(len(bpy.context.scene.timeline_markers)):
        AA.pose_markers.new(bpy.context.scene.timeline_markers[i].name)
        AA.pose_markers[i].frame = bpy.context.scene.timeline_markers[i].frame
  
    
def quickfix_index():
    for x in range(len(bpy.data.actions)): 
        if bpy.data.actions[x] == bpy.context.object.animation_data.action:
            if bpy.context.scene.actionloader_markers == True:
                change_timelinemarkers_from_action()
            bpy.context.object.action_list_index = x  


def register():
    bpy.types.Scene.actionloader_DualView = bpy.props.BoolProperty(default= False, description = "Two List of the Actions so you can have different filters on each. Doesn't affect or change anything in the scene, just for listing.")
    bpy.types.Object.action_list_index = bpy.props.IntProperty(
        update = update_action_list, 
        description = "Action Loader's highlighted action on list for this object"
        )
    bpy.types.Scene.action_list_index = bpy.props.IntProperty(
        update = update_action_list_noObj, 
        description = "Action Loader's highlighted action on list for this scene when no object selected"
        )
    enum_items = (
        ('0','Custom','Sets Frame Range of action by the current Frame Range'),
        ('1','Keyframes',"Sets Frame Range by action's first and last keyframe")
        )
    bpy.types.Scene.actionloader_rangemode = bpy.props.EnumProperty(
        items = enum_items, 
        update = update_rangemode,
        description = "Set the ranfe for 0: custom or 1: based on keyframes"
        )
    enum_prevspeed = (
        ('0','Normal','Set speed to Normal (Time Remapping "frame_map_new" to 100 and adjusts range)'),
        ('1','1/2', 'Set speed to half (Time Remapping "frame_map_new" to 200 and adjusts range)'),
        ('2','1/4', 'Set speed to a quarter (Time Remapping "frame_map_new" to 400 and adjusts range)'),
        ('3','1/8', 'Set speed to an eighth (Time Remapping "frame_map_new" to 800 and adjusts range)')
        )
    bpy.types.Scene.actionloader_speedprev = bpy.props.EnumProperty(
        items = enum_prevspeed,
        update=update_prevspeed, 
        set = set_prevspeed, 
        get = get_prevspeed
        )
    bpy.types.Scene.actionloader_showicons = bpy.props.BoolProperty(
        name = "Show icons", 
        description = "Show icons in Action Loader Addon",
        default = True
        )
    bpy.types.Scene.actionloader_autorange = bpy.props.BoolProperty(
        name = "Set Auto Range", 
        description = "Automatically set and load Frame Ranges for each Action and zoom in on Loading actions",
        default = False
        )
    bpy.types.Scene.actionloader_markers = bpy.props.BoolProperty(
        name = "Set Action Markers", 
        description = "Automatically assign pose_markers from action to scene timeline_markers (kind of uses scene Markers as Local Markers)",
        default = False
        )

    for cls in module_classes:
        bpy.utils.register_class(cls[1])


def unregister():
    for cls in module_classes:
        bpy.utils.unregister_class(cls[1])

    del bpy.types.Object.action_list_index
    del bpy.types.Scene.action_list_index
    del bpy.types.Scene.actionloader_showicons
    del bpy.types.Scene.actionloader_autorange
    del bpy.types.Scene.actionloader_markers
    del bpy.types.Scene.actionloader_speedprev


module_classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)


if __name__ == "__main__":
    register()
    
