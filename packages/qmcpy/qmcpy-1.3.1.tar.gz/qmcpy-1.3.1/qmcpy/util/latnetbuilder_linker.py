import os
from ..util import ParameterError
from numpy import *


def latnetbuilder_linker(lnb_dir ='./', out_dir='./', fout_prefix='lnb4qmcpy'):
    """
    >>> from ..discrete_distribution import Lattice,DigitalNetB2
    >>> _ = os.system('docker run --name lnb -dit -p 4243:4243 umontrealsimul/latnetbuilder:light > /dev/null')
    >>> _ = os.system('docker exec -it lnb latnetbuilder -t lattice -c ordinary -s 2^16 -d 100 -f CU:P2 -q 2 -w product:0.1 -e fast-CBC -o lnb.lattice')
    >>> _ = os.system('docker cp lnb:lnb.lattice/ ./')
    >>> lnb_qmcpy_f = latnetbuilder_linker(
    ...     lnb_dir = './lnb.lattice/',
    ...     out_dir = './lnb_lattice',
    ...     fout_prefix = 'mylattice')
    >>> lat = Lattice(dimension = 5,randomize=False,order='linear',generating_vector=lnb_qmcpy_f)
    >>> lat.gen_samples(8,warn=False)
    >>> _ = os.system('docker rm -f lnb > /dev/null')

    #>>> _ = os.system('docker exec -it lnb latnetbuilder -t net -c sobol -s 2^16 -d 10 -f projdep:t-value -q inf -w order-dependent:0:0,1,1 -e random-CBC:70 -o lnb.lattice -o lnb.net')


    Args:
        lnb_dir (str): relative path to directory where `outputMachine.txt` is stored 
            e.g. 'my_lnb/poly_lat/'
        out_dir (str): relative path to directory where output should be stored
            e.g. 'my_lnb/poly_lat_qmcpy/'
        fout_prefix (str): start of output file name. 
            e.g. 'my_poly_lat_vec' 
    
    Return:
        str: path to file which can be passed into QMCPy's Lattice or Sobol' in order to use 
             the linked latnetbuilder generating vector/matrix
             e.g. 'my_poly_lat_vec.10.16.npy'
    
    Adapted from latnetbuilder parser:
        https://github.com/umontreal-simul/latnetbuilder/blob/master/python-wrapper/latnetbuilder/parse_output.py#L74
    """
    with open(lnb_dir+'/outputMachine.txt') as f:
        Lines = f.read().split("\n")
    sep = '  //'
    if Lines[0].split(sep)[0] == 'Ordinary':
        nb_points = int(Lines[1].split(sep)[0])
        dim = int(Lines[2].split(sep)[0])
        gen_vector = []
        for i in range(dim):
            gen_vector.append(int(Lines[5+i].split(sep)[0]))
        v = array(gen_vector, dtype=uint64)
        f_out = '%s/%s.%d.%d.npy'%(out_dir,fout_prefix,dim,log2(nb_points))
        save(f_out,v)
        return f_out
    else:
        nb_cols = int(Lines[0].split(sep)[0])
        nb_rows = int(Lines[1].split(sep)[0])
        nb_points = int(Lines[2].split(sep)[0])
        dim = int(Lines[3].split(sep)[0])
        set_type = Lines[5].split(sep)[0]
        line = 6
        if set_type == 'Polynomial':
            line += dim + 1
        elif set_type == 'Sobol':
            line += dim
        mint = []
        pows2 = 2**arange(nb_rows-1,-1,-1)[:,None]
        for c in range(dim):
            line += 1
            M = []
            for i in range(nb_rows):
                M.append(array([int(x) for x in Lines[line+i].split(' ')]))
            line += nb_rows
            mint.append((array(M)*pows2).sum(0))
        mint = array(mint,dtype=uint64)
        f_out = '%s/%s.%d.%d.%d.msb.npy'%(out_dir,fout_prefix,dim,nb_rows,nb_cols)
        save(f_out,mint)
        return f_out

    