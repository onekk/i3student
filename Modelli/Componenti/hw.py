"""
 i3Student motors
 copyright 2020 Carlo Dormeletti (onekk)
 carlo.dormeletti@yahoo.com

 Version:   

"""

__all__ = ["telaio"]

from FreeCAD import Vector, Rotation
import Part

EPS = 0.001
EPS_N = EPS * -1

def telaio(doc, o_name, tel_h, tel_w, tel_th, tel_width):
    o_body = Part.makeBox(
        tel_w, tel_th, tel_h,
        Vector(tel_w * -0.5, tel_th * -0.5, 0))

    i_tel_w = tel_w - (tel_width * 2)
    i_tel_h = tel_h - (tel_width * 2)
    i_tel_th = tel_th + EPS *2
    i_body = Part.makeBox(
        i_tel_w, i_tel_th, i_tel_h,
        Vector(i_tel_w * -0.5, i_tel_th * -0.5, tel_width))

    obj_r = doc.addObject("Part::Feature", o_name)
    obj_r.Shape = o_body.cut(i_body)
    
    doc.recompute()

    return obj_r

