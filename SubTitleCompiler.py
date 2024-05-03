import bpy

def SwitchFab(tree, name, type, pos):
    for node in tree.nodes:
        if node.name == name:
            return
    node = tree.nodes.new('GeometryNodeIndexSwitch')
    node.name  = name
    node.label = name
    node.location  = pos
    node.data_type = type
    return node


def ColorFab(hex_code):
    hex_code = hex_code.lstrip('#')  # Remove '#' if present
    if len(hex_code) != 6:
        raise ValueError("Invalid hexadecimal color code")

    r = int(hex_code[0:2], 16) / 255.0
    g = int(hex_code[2:4], 16) / 255.0
    b = int(hex_code[4:6], 16) / 255.0

    return [r, g, b, 1]

global ID
ID = 0

class SubTitleObject():
    def __init__(self, name, content, color, start, end):
        global ID;
        ID          += 1;
        self.ID      = ID
        self.name    = name
        self.content = content        
        self.color   = color
        self.start   = start
        self.end     = end        

    def __str__(self):
        return f"<SubTitleObj ({self.ID}): [{self.name}] <{self.content}> S:{self.start} E:{self.end}>"


if 'SubTitleController' not in bpy.data.node_groups:
    print('please import or link the SubTitleController Nodes')
    exit()

Controller = bpy.data.node_groups["SubTitleController"]


SwitchFab(Controller, 'Frame Controller',    'INT',    (-4020 - 600, 0) )
SwitchFab(Controller, 'Color Controller',    'RGBA',   (-4020 - 400, 0) )
SwitchFab(Controller, 'Name Controller',     'STRING', (-4020 - 200, 0) )
SwitchFab(Controller, 'Contents Controller', 'STRING', (-4020 - 000, 0) )


name  = ""
color = ColorFab('#262626')
killFrame = 0
SubTitles = []

startFrame = bpy.data.scenes["Scene"].frame_start
endFrame   = bpy.data.scenes["Scene"].frame_end
totalFrame = endFrame - startFrame


titles = bpy.data.texts["Text"].as_string().split('\n')

for x in range(len(titles)):
    noName = False

    if titles[x].startswith(":"):
        if titles[x].startswith("::"):
            pass # Keep last name
        elif titles[x].startswith(":;"):
            noName = True # keep last name but don't show it
        else:
            name = titles[x][2:]


        FrCl = titles[x+1].split(' ')
        FrCl[0] = eval(FrCl[0])
        if FrCl[1] == '-':
            FrCl[1] = None
        else:
            FrCl[1] = eval(FrCl[1])


        if titles[x-1].startswith(';'):
            color = ColorFab( titles[x-1].split(' ')[1] )
            

        SubTitleObj = SubTitleObject(
            name,
            titles[x+2],
            color,
            FrCl[0],
            FrCl[0] + FrCl[1] if FrCl[1] != None else None
        )

        SubTitles.append(SubTitleObj)


for each in SubTitles:
    print(each)


def AddSwitchItem(name, index, value):
    try: 
        Controller.nodes[name].inputs[index + 1].default_value = value
    except:
        Controller.nodes[name].index_switch_items.new()
        Controller.nodes[name].inputs[index + 1].default_value = value


index = 0

for frame in range(startFrame, endFrame + 1, 1):


    for each in SubTitles:
        if each.start == frame:
            index = each.ID
        if each.end == frame:
            index = 0
    
    AddSwitchItem('Frame Controller',   frame, index)
    
for item in SubTitles:
    AddSwitchItem('Color Controller',   item.ID, item.color)
    AddSwitchItem('Name Controller',    item.ID, item.name)
    AddSwitchItem('Contents Controller', item.ID, item.content)    



    FCOut = Controller.nodes['Frame Controller'].outputs[0]
    Controller.links.new(FCOut, Controller.nodes['Name Controller'].inputs[0])
    Controller.links.new(FCOut, Controller.nodes['Contents Controller'].inputs[0])
    Controller.links.new(FCOut, Controller.nodes['Color Controller'].inputs[0])



    print(frame, index)