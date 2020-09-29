"""
 i3Student motors
 copyright 2020 Carlo Dormeletti (onekk)
 carlo.dormeletti@yahoo.com

 Version:   

"""

__all__ = ["telaio", "m_mount"]

from FreeCAD import Vector, Rotation
import Part

EPS = 0.001
EPS_N = EPS * -1
EPS_C = EPS * -0.5

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

def m_mount(doc, o_name, mount_th, tipo=0):
    """
    Create motor mounts
    Keywords Arguments:
      doc       Document reference
      o_name    Component name
      tipo      type of mounting
            0 = standard motor Z
    """
    if tipo == 0:
        mount_dim = 45
        hole_space = 31.0 * 0.5  # for Nema17
        c_dia = 22 * 0.5
        c_th = 2.5
        hole_dia = 3.15 * 0.5
        shaft_hole_d = 6
        h_z_off = -mount_th + EPS_C

        m_body = Part.makeBox(
                    mount_dim, mount_dim, mount_th,
                    Vector(mount_dim * -0.5, mount_dim * -0.5, -mount_th))
        c_dia = Part.makeCylinder(
                    c_dia, c_th, Vector(0, 0, -mount_th), Vector(0, 0, 1))

        shaft_hole = Part.makeCylinder(
                shaft_hole_d, mount_th + EPS,
                Vector(0, 0, h_z_off), Vector(0, 0, 1)
                )
        # Part.show(shaft_hole)
        

        h_pos = (
                Vector(hole_space, hole_space, h_z_off),
                Vector(hole_space, hole_space * -1, h_z_off),
                Vector(hole_space * -1, hole_space, h_z_off),
                Vector(hole_space * -1, hole_space * -1, h_z_off)
                )

        holes = []

        for pos in h_pos:
            holes.append(
                Part.makeCylinder(hole_dia, mount_th + EPS, pos, Vector(0, 0, 1))
                )

        holes.append(c_dia)
        holes.append(shaft_hole)

        body = m_body.cut(holes)

        obj_r = doc.addObject("Part::Feature", o_name)
        obj_r.Shape = body
        
        doc.recompute()
        return obj_r
    else:
        return None
