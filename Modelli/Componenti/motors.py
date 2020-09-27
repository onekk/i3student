"""
 i3Student motors
 copyright 2020 Carlo Dormeletti (onekk)
 carlo.dormeletti@yahoo.com

 Version:   

"""

__all__ = ["nema17"]

from FreeCAD import Vector, Rotation
import Part

EPS = 0.001
EPS_N = EPS * -1

def nema17(doc, o_name, lung=48, tipo=0):
    body_dim = 42.3
    hole_space = 31.0 * 0.5
    c_dia = 22 * 0.5
    sh_dia = 5 * 0.5
    sh_len = 24
    hole_dia = 3 * 0.5
    m_body = Part.makeBox(body_dim, body_dim, lung, Vector(body_dim * -0.5, body_dim * -0.5, -lung))
    c_dia = Part.makeCylinder(11,2 + EPS, Vector(0, 0, EPS_N), Vector(0, 0, 1))
    shaft = Part.makeCylinder(sh_dia, sh_len, Vector(0, 0, 0), Vector(0, 0, 1))

    h_pos = (
            Vector(hole_space, hole_space),
            Vector(hole_space, hole_space * -1),
            Vector(hole_space * -1, hole_space),
            Vector(hole_space * -1, hole_space * -1)
            )

    holes = []

    for pos in h_pos:
        holes.append(
            Part.makeCylinder(hole_dia, 5, pos, Vector(0, 0, 1))
            )

    body = m_body.cut(holes)

    obj_r = doc.addObject("Part::Feature", o_name)
    obj_r.Shape = body.fuse(c_dia.fuse(shaft))
    
    doc.recompute()
    return obj_r

