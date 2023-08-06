import os, sys, json
from epkernel import epcam, BASE
from epkernel.Action import Information,Selection

def save_eps(job:str, path:str):
    BASE.setJobParameter(job, job)
    return BASE.save_eps(job, path)

def save_gerber( job:str, step:str, layer:str, filename:str,  resize:int, angle:float, scalingX:float, scalingY:float, mirror:bool, rotate:bool, scale:bool, cw:bool,  mirrorpointX:int, mirrorpointY:int, rotatepointX:int, rotatepointY:int, scalepointX:int, scalepointY:int, mirrorX:bool, mirrorY:bool, numberFormatL=2, numberFormatR=4, zeros=2, unit=0):
    try:
        _type = 0
        gdsdbu = 0.01
        profiletop = False
        cutprofile = True
        isReverse = False
        cut_polygon = []
        if mirrorX == True and mirrorY ==True:
            mirrordirection = 'XY'
        elif mirrorX==True and mirrorY ==False:
            mirrordirection = 'Y'
        elif mirrorX==False and mirrorY ==True:
            mirrordirection = 'X'
        else:
            mirrordirection = 'NO'
        BASE.layer_export(job, step, layer, _type, filename, gdsdbu, resize, angle, scalingX, scalingY, isReverse,
                    mirror, rotate, scale, profiletop, cw, cutprofile, mirrorpointX, mirrorpointY, rotatepointX,
                    rotatepointY, scalepointX, scalepointY, mirrordirection, cut_polygon,numberFormatL=2,numberFormatR=4,
                    zeros=2,unit=0)
    except Exception as e:
        print(e)
    return None

def save_drill(job:str, step:str, layer:str, path:str, isMetric:bool, number_format_l=2, number_format_r=4, zeroes=2, unit=0, tool_unit=1, x_scale=1, y_scale=1, x_anchor=0, y_anchor=0):
    try:
        layer_info = Information.get_layer_information(job)
        for i in range(0,len(layer_info)):
            if layer_info[i]['name']==layer and layer_info[i]['context'] == 'board' and layer_info[i]['type'] =='drill':
                BASE.drill2file(job, step, layer,path,isMetric,number_format_l=2,number_format_r=4,
                    zeroes=2,unit=0,tool_unit=1,x_scale=1,y_scale=1,x_anchor=0,y_anchor=0, manufacator = '', tools_order = [])
                return True
    except Exception as e:
        print(e)
    return False


def save_rout(job:str, step:str, layer:str, path:str, number_format_l=2,number_format_r=4,zeroes=2,unit=0,tool_unit=1,x_scale=1,y_scale=1,x_anchor=0,y_anchor=0, break_arcs = False):
    try:
        layer_info = Information.get_layer_information(job)
        for i in range(0,len(layer_info)):
            if layer_info[i]['name'] == layer and layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'rout':
                repeat = BASE.get_all_step_repeat_steps(job,step)
                data = json.loads(repeat)
                step_repeat = data['steps']
                step_repeat.append(step)
                can_back = True
                for j in range(0,len(step_repeat)):
                    _step = step_repeat[j]
                    Selection.reverse_select(job, _step, layer)
                    ret = Information.get_selected_features_infos(job,_step,layer)
                    Selection.clear_select(job, _step, layer)
                    if len(ret) == 0:
                        can_back=False
                        return False
                    for k in range(0,len(ret)):
                        attribute = ret[k]['attributes']
                        has_chain = False
                        for m in range(0,len(attribute)):
                            if  '.rout_chain' in attribute[m]:
                                has_chain = True
                        if  has_chain == False:
                                can_back=False
                                return False
                if can_back==True:
                    BASE.rout2file(job, step, layer,path,number_format_l=2,number_format_r=4,zeroes=2,unit=0,tool_unit=1,x_scale=1,y_scale=1,x_anchor=0,y_anchor=0, partial_order = 0, num_in_x = 0, num_in_y = 0, order_type = 0, serial_no = 0, break_arcs = False)
                return True
    except Exception as e:
        print(e)
    return False
    
def save_job(job:str,path:str)->bool:
    try:
        layers = Information.get_layers(job)
        steps = Information.get_steps(job)
        for step in steps:
            for layer in layers:
                BASE.load_layer(job,step,layer)
        BASE.save_job_as(job,path)
        return True
    except Exception as e:
        print(e)
    return False