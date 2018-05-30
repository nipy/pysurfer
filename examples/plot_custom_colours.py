"""
=================================
Plot RGBA values on brain surface
=================================

"""
import mne
import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab
from copy import deepcopy
from tvtk.api import tvtk
from tvtk.common import configure_input_data
from surfer.utils import smoothing_matrix, mesh_edges
from surfer import Brain

print(__doc__)

###############################################################################
# define helper functions

def norm(x):
	'''
	Normalise array betweeen 0-1
	'''
	return (x - np.min(x)) / (np.max(x) - np.min(x))

###############################################################################
# load surface

surf_fname = '/Users/lauragwilliams/Documents/programming/PySurfer/examples/example_data/lh.white'
rr, tris = nibabel.freesurfer.io.read_geometry(surf_fname)
tris = tris.astype(np.uint32)
x, y, z = rr.T

###############################################################################
# generate an rgba matrix, of shape n_vertices x 4

# define color map
cmap = plt.cm.rainbow

# change colour based on position on the x axis
hue = norm(x)
colors = cmap(hue)[:, :3]

# change alpha based on position on the z axis
alpha = norm(z)

# combine hue and alpha into a Nx4 matrix
rgba_vals = np.concatenate((colors, alpha[:, None]), axis=1)


###############################################################################
# plot

# init figure
fig = mlab.figure()
b = Brain('fsaverage', hemi, surf, subjects_dir=subjects_dir,
          background='white', alpha=0, figure=fig)

# plot points in x,y,z
mesh = mlab.pipeline.triangular_mesh_source(
    x, y, z, tris, figure=fig)
mesh.data.point_data.scalars.number_of_components = 4  # r, g, b, a
mesh.data.point_data.scalars = (rgba_vals * 255).astype('ubyte')

# tvtk for vis
mapper = tvtk.PolyDataMapper()
configure_input_data(mapper, mesh.data)
actor = tvtk.Actor()
actor.mapper = mapper
fig.scene.add_actor(actor)

