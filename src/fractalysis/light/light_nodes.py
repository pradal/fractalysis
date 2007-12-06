#! /usr/bin/env python
# -*- python -*-
#
#       OpenAlea.Fractalysis : OpenAlea fractal analysis library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
fractalysis.light nodes
"""

__license__= "Cecill-C"
__revision__=" $Id: light_nodes.py $ "

import openalea.fractalysis.light as lit
import openalea.plantgl.all as pgl

from openalea.fractalysis.fractutils.pgl_utils import centerScene

def create_MSS( name, scene, scale_table ):
  scc = centerScene( scene )
  return lit.ssFromDict( name, scc, scale_table)

def generate_pix(mss, light_direction, distrib, img_size, save_path, distfactor):
  
  globScene = mss.genScaleScene(1)
  for i in range(1,mss.depth):
    globScene.add(mss.genScaleScene(i+1))

  az = light_direction[0]
  el = light_direction[1]
  dir = lit.azel2vect(az, el)


  width = img_size[0]
  height = img_size[1]

  lit.prepareScene(globScene, width, height, az, el, distfactor)
  
  b=mss.loadBeams(az, el, save_path)
  if b != None:
    print "beams loaded..."
  else :
    print "computing beams..."
    b=pgl.Viewer.frameGL.castRays2(pgl.Viewer.getCurrentScene())
    mss.saveBeams(az, el,b, save_path)
  mss.beamsToNodes(dir, b)

  sproj=mss.loadSproj(az, el, save_path)
  if sproj != None:
    print "projected surface loaded..."
    mss.sprojToNodes(dir, sproj)
  else :
    print "computing projections..."
    sproj=mss.computeProjections( dir )
    mss.saveSproj(az, el, sproj, save_path)
 
  root_id = mss.get1Scale(1)[0]
  matrix = mss.probaImage(root_id, dir, distrib, width, height)
  pix = mss.makePict(az, el, distrib, matrix, width, height, save_path)
 
  return pix,
 
def light_direction(az, el):
  return (az, el),



