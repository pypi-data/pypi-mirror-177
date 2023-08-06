import xarray as xr
import xarrayuvecs.uvecs as xu
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import mahotas as mh
import ipywidgets as widgets
import scipy
import datetime
import skimage
import pickle as pk

from IPython import get_ipython
if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm


def craft(self, nameId, res=0, m3d=0):
    '''
    Export 'vtk' file and the phase file. 

    :param res: resolution for the vtk export
    :type res: float
    :param nameId: name of manipulation
    :type nameTd: string
    :param m3d: 0 for 2 dimensional data, 1 for 3 dimensional data
    :type m3d: int
    '''
    zoom = self._obj.step_size/res

    # Copy and compute mean grain
    ds = self._obj.copy()
    ds['orientation_mg'] = ds.aita.mean_grain()
    # Remove hole in grainId
    new_g = scipy.ndimage.maximum_filter(np.array(ds.grainId), 3)
    # Resize grainId for wrting vtk
    new_g_rs = scipy.ndimage.interpolation.zoom(
        new_g, zoom, order=0, mode='nearest')
    # extract euler angle for phase file
    euler_ori = ds.orientation_mg.uvecs.bunge_euler()

    if m3d != 0:
        new_g_rs_3d = np.copy(new_g_rs)
        for i in range(int(m3d/res-1)):
            new_g_rs_3d = np.dstack([new_g_rs_3d, new_g_rs])
        new_g_rs = new_g_rs_3d

    ################################
    # Write the microstructure input
    ################################
    # size of the map
    ss = np.shape(new_g_rs)
    # open micro.vtk file
    micro_out = open(nameId+'_micro.vtk', 'w')
    # write the header of the file
    micro_out.write('# vtk DataFile Version 3.0 ' +
                    str(datetime.date.today()) + '\n')
    micro_out.write('craft output \n')
    micro_out.write('ASCII \n')
    micro_out.write('DATASET STRUCTURED_POINTS \n')
    if m3d == 0:
        micro_out.write('DIMENSIONS ' + str(ss[1]) + ' ' + str(ss[0]) + ' 1\n')
    else:
        micro_out.write(
            'DIMENSIONS ' + str(ss[1]) + ' ' + str(ss[0]) + ' ' + str(ss[2])+'\n')

    micro_out.write('ORIGIN 0.000000 0.000000 0.000000 \n')
    if m3d == 0:
        micro_out.write('SPACING ' + str(res) + ' ' +
                        str(res) + ' 1.000000 \n')
    else:
        micro_out.write('SPACING ' + str(res) + ' ' +
                        str(res) + ' ' + str(res) + '\n')

    micro_out.write('POINT_DATA ' + str(np.prod(ss)) + '\n')
    micro_out.write('SCALARS scalars float \n')
    micro_out.write('LOOKUP_TABLE default \n')

    if m3d == 0:
        for i in list(range(ss[0]))[::-1]:
            for j in list(range(ss[1])):
                micro_out.write(str(int(new_g_rs[i, j]))+' ')
            micro_out.write('\n')
    else:
        for k in list(range(ss[2])):
            for i in list(range(ss[0]))[::-1]:
                for j in list(range(ss[1])):
                    micro_out.write(str(int(new_g_rs_3d[i, j, k]))+' ')
            micro_out.write('\n')

    micro_out.close()

    # -----------------------------------------------------------------------------------------------
    phase_out = open(nameId+'.phase', 'w')
    phase_out.write(
        '#------------------------------------------------------------\n')
    phase_out.write('# Date ' + str(datetime.date.today()) +
                    '      Manip: ' + nameId + '\n')
    phase_out.write(
        '#------------------------------------------------------------\n')
    phase_out.write(
        '# This file give for each phase \n# *the matetial \n# *its orientation (3 euler angles)\n')
    phase_out.write(
        '#\n#------------------------------------------------------------\n')
    phase_out.write('# phase    material       phi1    Phi   phi2\n')
    phase_out.write(
        '#------------------------------------------------------------\n')
    for i in tqdm(np.unique(new_g_rs)):
        sub_ds = ds.where(ds.grainId == i)
        if int(sub_ds.grainId.sum()) != 0:
            id1, id2 = np.where(np.array(ds.grainId) == i)
            phi1 = float(euler_ori[id1[0], id2[0], 0])
            phi = float(euler_ori[id1[0], id2[0], 1])
            phi2 = float(np.random.rand(1)*2*np.pi)
            if np.isnan(phi1):
                phi1 = float(np.random.rand(1)*2*np.pi)
                phi = float(np.random.rand(1)*2*np.pi)
            phase_out.write(str(i) + '          0              ' +
                            str(phi1) + ' ' + str(phi) + ' ' + str(phi2) + '\n')
    phase_out.close()

# ----------------------------------------------------


def save(self, path):
    """
    Save xarray craft data using pickle

    :param path: path to save pickle file
    :type path: string
    """

    ds = self._obj.copy()
    pk.dump(ds, open(path, "wb"))

# ----------------------------------


xr.Dataset.aita.craft = craft
xr.Dataset.aita.save = save
