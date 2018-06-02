#!/usr/bin/env python 

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

import os
from argparse import ArgumentParser
import numpy as np
from matplotlib import image
import matplotlib.pyplot as plt
from astropy.table import Table

def fetch_cutout(ra, dec): 
    url = 'http://legacysurvey.org/viewer/jpeg-cutout/?'
    url += 'ra={}&dec={}&layer=decals-dr5&pixscale=0.27&bands=grz'
    return image.imread(urlopen(url.format(ra, dec)), format='jpeg')

if __name__ == '__main__': 
    parser = ArgumentParser()
    parser.add_argument('cat_filename') 
    parser.add_argument('--id_colname', default='id') 
    parser.add_argument('--ra_colname', default='ra')
    parser.add_argument('--dec_colname', default='dec')
    parser.add_argument('--shapeexp_r_colname', default='shapeexp_r')
    parser.add_argument('--csb_colname', default='csb')
    parser.add_argument('--type_colname', default='type')
    parser.add_argument('--ellip_colname', default='ellip')
    parser.add_argument('--out_dir', '-o', default='') 
    parser.add_argument('--no_circle', action='store_true')
    args = parser.parse_args()

    cat = Table.read(args.cat_filename)
    id_col = args.id_colname
    ra_col = args.ra_colname
    dec_col = args.dec_colname
    shape_col = args.shapeexp_r_colname
    csb_col = args.csb_colname
    type_col = args.type_colname
    ellip_col = args.ellip_colname
    
    
    for src in cat:
        img = fetch_cutout(src[ra_col], src[dec_col])
        plt.imshow(img)
        plt.gca().set(xticks=[], yticks=[])
        if not args.no_circle:
            plt.plot(img.shape[1]/2, img.shape[0]/2, mfc='none', 
                     mec='lime', marker='o', markersize=20, mew=1.5)
       #plt.title('id = '+str(src[id_col]))
        plt.text(0.9, 0.9, '$\mu_o(g)$ = '+str('%.2f'%src[csb_col]), transform=plt.gca().transAxes, ha='right', color='w', fontsize=20)
        plt.text(0.5, 0.08, '$\epsilon$ = '+str('%.2f'%src[ellip_col])+'\n'+'$r_{exp}$ = '+str('%.2f'%src[shape_col])+'\"', transform=plt.gca().transAxes, ha='center', color='w', fontsize=20)
        out_fn = os.path.join(args.out_dir, 'src-'+str(src[id_col])+'.png')
        plt.tight_layout()
        plt.savefig(out_fn, bbox_inches='tight')
        plt.close()
