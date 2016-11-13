#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 11:51:25 2016

@author: dsaunder
"""
import pandas as pd
import os
import numpy as np
import sys

def make_cover_poster(aspect_ratio=None):
    
    if aspect_ratio == None:
        aspect_ratio = 1.2
    book_info = pd.read_csv('downloadtimes.tsv', index_col=0, sep='\t')
    
    # Remove duplicate indices
    gb = book_info.groupby(level=0)
    book_info = gb.min()
    
    coverfiles = os.listdir('covers')
    booknames = [os.path.splitext(a)[0]  for a in coverfiles if '.jpeg' in a]
    n = len(booknames)
    tileheight = 200
    ncols = np.floor(np.sqrt(n) * aspect_ratio)
    nrows = np.ceil(n/ncols)
    tilestr = '-tile %dx%d' % (ncols,nrows)
    sizestr = '%dx%d' % (tileheight, tileheight*1.5)
    
    book_info = book_info.reindex(booknames, fill_value=0)
    book_info = book_info.sort_values(by='downloadtime', ascending=False)
    coverpaths = ['"covers/%s.jpeg"' % a for a in book_info.index]
    coversstr = ' '.join(coverpaths)
    #callstr = 'montage covers/*.jpeg -geometry %s+1+1 %s tiledcovers.jpg' % (sizestr,tilestr)
    callstr = 'montage %s -geometry %s+1+1 %s -trim tiled_covers.jpg' % (coversstr, sizestr,tilestr)

    result = os.system(callstr)
    if result == 0:
        print "Cover poster successfully created"
    else:
        print "Something went wrong with cover poster creation (is ImageMagick installed?)"
        
if __name__ == "__main__":
    aspect_ratio = sys.argv[1:]
    if len(aspect_ratio) == 0:
        aspect_ratio = None
    else:
        aspect_ratio = float(aspect_ratio[0])

    make_cover_poster(aspect_ratio)
    
