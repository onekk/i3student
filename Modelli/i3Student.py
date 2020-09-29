"""
 i3Student Model

 copyright 2020 Carlo Dormeletti (onekk)
 carlo.dormeletti@yahoo.com

 Version: 0.01
 License CC-BY-SA-NC  

"""

import sys
import os
import datetime
import time
import importlib

import FreeCAD
import FreeCADGui
from FreeCAD import Rotation, Vector
import Part
import Draft
#import Mesh
#import MeshPart

# BEGIN DOC Settings
DEBUG = True
DBG_LOAD = False
DOC_NAME = "i3Student"
CMPN_NAME = None

HOME_PATH = os.path.dirname(os.path.realpath(__file__))
# location of the library
MODULE_PATH = HOME_PATH + u"/Componenti/"
# END DOC Settings

if not MODULE_PATH in sys.path:
    if DBG_LOAD is True:    
        print("no module path")
    sys.path.insert(-1,MODULE_PATH)
else:
    if DBG_LOAD is True:    
        print("module path is present")

if DBG_LOAD is True:    
    print(sys.path)

#from math import pi cos, sin, pi, sqrt
import numpy as np

import motors
importlib.reload(motors)

from motors import nema17

import hw
importlib.reload(hw)

from hw import telaio, m_mount


def activate_doc():
    """activate document"""
    FreeCAD.setActiveDocument(DOC_NAME)
    FreeCAD.ActiveDocument = FreeCAD.getDocument(DOC_NAME)
    FreeCADGui.ActiveDocument = FreeCADGui.getDocument(DOC_NAME)
    if DBG_LOAD is True:    
        print("{0} activated".format(DOC_NAME))


def setview():
    """Rearrange View"""
    DOC.recompute()
    VIEW.viewAxometric()
    VIEW.setAxisCross(True)
    VIEW.fitAll()


def clear_doc():
    """Clear the active document deleting all the objects"""
    for obj in DOC.Objects:
        DOC.removeObject(obj.Name)

if FreeCAD.ActiveDocument is None:
    FreeCAD.newDocument(DOC_NAME)
    if DBG_LOAD is True:    
        print("Document: {0} Created".format(DOC_NAME))

# test if there is an active document with a "proper" name
if FreeCAD.ActiveDocument.Name == DOC_NAME:
    if DBG_LOAD is True:    
        print("DOC_NAME exist")
else:
    if DBG_LOAD is True:    
        print("DOC_NAME is not active")
    # test if there is a document with a "proper" name
    try:
        FreeCAD.getDocument(DOC_NAME)
    except NameError:
        if DBG_LOAD is True:    
            print("No Document: {0}".format(DOC_NAME))
        FreeCAD.newDocument(DOC_NAME)
        if DBG_LOAD is True:    
            print("Document {0} Created".format(DOC_NAME))

DOC = FreeCAD.getDocument(DOC_NAME)
GUI = FreeCADGui.getDocument(DOC_NAME)
VIEW = GUI.ActiveView    
if DBG_LOAD is True:    
    print("DOC : {0} GUI : {1}".format(DOC, GUI))

activate_doc()

if DBG_LOAD is True:   
    print(FreeCAD.ActiveDocument.Name)

clear_doc()

if CMPN_NAME is None:
    pass
else:
    DOC.addObject("App::DocumentObjectGroup", CMPN_NAME)

EPS = 0.005
EPS_C = EPS * -0.5
VZOR = Vector(0,0,0)
ROT0 = Rotation(0, 0, 0)
ROTX90 = Rotation(0, 0, 90)
ROTXN90 = Rotation(0, 0, -90)
ROTY90 = Rotation(0, 90, 0)
ROTZ180 = Rotation(180, 0, 0)
#Used to shorten most Placements
PL0 = FreeCAD.Placement(VZOR, ROT0)

# DOCUMENT START HERE

mot1 = nema17(DOC, "motore_z_dx")
mot2 = nema17(DOC, "motore_z_sx")

tel_h = 230
tel_w = 250
tel_th = 4
tel_width = 20

motor_offset = (tel_w - tel_width) * 0.5

z_mount_th = 6

mot1.Placement = FreeCAD.Placement(Vector(motor_offset *-1,-35,0), ROT0)
mot2.Placement = FreeCAD.Placement(Vector(motor_offset,-35,0), ROT0)

mounting = telaio(DOC, "telaio", tel_h, tel_w, tel_th, tel_width)

m_mot_zsx = m_mount(DOC, "mount_zsx", z_mount_th, 0)
m_mot_zdx = m_mount(DOC, "mount_zdx", z_mount_th, 0)

m_mot_zsx.Placement = FreeCAD.Placement(Vector(motor_offset *-1,-35, z_mount_th), ROT0)
m_mot_zdx.Placement = FreeCAD.Placement(Vector(motor_offset,-35, z_mount_th), ROT0)

setview()