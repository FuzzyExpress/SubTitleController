import bpy

bpy.app.handlers.frame_change_pre.clear()
DBG = bpy.data.node_groups["SubTitleController"].nodes["SubTitleDBG"]
DBG2 = bpy.data.node_groups["SubTitleController"].nodes["SubTitleDBG.001"]

def write(*args, sep=' ', end='\n', data=bpy.data.node_groups["SubTitleController"].nodes["SubTitleMain"]):
    string = "";
    for each in args:
        string += str(each) + sep;
    
    data.string = string;

def color(Color, data=bpy.data.node_groups["SubTitleController"].nodes["Color"]):
    data.color = hex_to_rgb(Color)


global name, killFrame
name  = ""
killFrame = 0

# Define your pre-frame callback function
def my_pre_frame_callback(scene):
    global name, killFrame
    frame = bpy.data.scenes["Scene"].frame_current
    titles = bpy.data.texts["Text"].as_string().split('\n')


    if frame == bpy.data.scenes["Scene"].frame_start: write()
    
    for x in range(len(titles)):
        noName = False
        if titles[x].startswith(":"):

            FrCl = titles[x+1].split(' ')
            FrCl[0] = eval(FrCl[0])
            if FrCl[1] == '-':
                FrCl[1] = -1
            else:
                FrCl[1] = eval(FrCl[1])
            
            if frame == killFrame: write()
            
            if int(FrCl[0]) == frame:
            
                if titles[x].startswith("::"):
                    pass # Keep last name
                if titles[x].startswith(":;"):
                    noName = True # keep last name but don't show it
                else:
                    name = titles[x][2:]
                
                if titles[x-1].startswith(';'):
                    color( titles[x-1].split(' ')[1] )
                    
                
                
                if int(FrCl[0]) == frame:
                    killFrame = int(FrCl[0]) + int(FrCl[1])
                    if not noName:
                        write(f"[{name}]", titles[x+2])
                    else:
                        write(titles[x+2])
    
            
            
    n = "\n"
    write("DBug: frame:", frame, data=DBG, )
    # write('\n'.join(titles), frame, killFrame, noName, data=DBG2)
# Add the pre-frame callback function to the pre_frame list

bpy.app.handlers.frame_change_pre.append(my_pre_frame_callback)
write("Pre-frame callback added", data=DBG)


class CustomProcessInputOperator(bpy.types.Operator):
    """Custom Operator to process input while Control key is pressed."""
    bl_idname = 'object.custom_process_input'
    bl_label = 'Custom Process Input'
    bl_options = {'REGISTER'}

    def modal(self, context, event):
        # print(event, event.type)
        if event.type == 'ESC':
            bpy.app.handlers.frame_change_pre.remove(my_pre_frame_callback)
            write("Pre-frame callback removed", data=DBG)
            return {'FINISHED'}
        elif event.ctrl:
            # Input processing code goes here
            pass

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

# Register the operator
def register():
    bpy.utils.register_class(CustomProcessInputOperator)

# Unregister the operator
def unregister():
    bpy.utils.unregister_class(CustomProcessInputOperator)

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')  # Remove '#' if present
    if len(hex_code) != 6:
        raise ValueError("Invalid hexadecimal color code")

    r = int(hex_code[0:2], 16) / 255.0
    g = int(hex_code[2:4], 16) / 255.0
    b = int(hex_code[4:6], 16) / 255.0

    return [r, g, b, 1]


# Test the operator
if __name__ == "__main__":
    register()
    bpy.ops.object.custom_process_input('INVOKE_DEFAULT')
    
