# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 17:11:03 2016

@author: dsaunder
"""

import os
import shutil
import pandas as pd
import lib.kindleunpack
import sys

# Disable
def blockPrint():
    global old_stdout
    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    global old_stdout
    sys.stdout = old_stdout


    
def extract_cover(filename, bookroot):
    if not ((filename.endswith('azw3')) or (filename.endswith('azw')) or (filename.endswith('mobi'))):
        return (None, None)
        
    # Get the name of the book from the filename
    bookname,ext = os.path.splitext(filename)
    
    # Note the time the book was downloaded. Use last modified time 
    bookdownloadtime = os.stat(bookroot + os.sep + filename).st_mtime

    try:
        os.mkdir('covers')
    except OSError:
        pass
    
    cover_out_name = 'covers/' + bookname + '.jpeg'
    if os.path.isfile(cover_out_name):
        print(bookname + " cover file already exists.")
        return (bookname, bookdownloadtime)
    
    try:      
        blockPrint()
        lib.kindleunpack.main(['kindleunpack','%s/%s' % (bookroot, filename), 'temp'])
    except (IndexError, lib.kindleunpack.unpackException):
        print bookname + " index error."
        return (None, None)
    finally:
        pass
        enablePrint()
        
        # Should handle unpack exceptions differently
    
    imgdir = 'temp/mobi7/Images/'
    
    # Look for any file with "cover" in the name 
    cover_found = False
    for imgname in os.listdir(imgdir):
        if 'cover' in imgname:
            cover_found = True
            print bookname + " cover extracted."
            shutil.copy(imgdir+imgname,cover_out_name)
            break

        # Delete the extracted files
    shutil.rmtree('temp', ignore_errors=True)

    if not cover_found:
        print bookname + " cover NOT found in extracted files"
        return (None, None)
    else:
        return (bookname, bookdownloadtime)
#%%
def extract_book_covers(bookdirs):
    # Add cover images from books in the directory. Don't overwrite or delete existing
    # images.
    booknames = [] 
    bookdownloadtimes = []
    for bookroot in bookdirs:
        for filename in os.listdir(bookroot):
            if not ((filename.endswith('azw3')) or (filename.endswith('azw')) or (filename.endswith('mobi'))):
                continue
            
            (bookname, bookdownloadtime) = extract_cover(filename, bookroot)
            if bookname:
                booknames.append(bookname)
                bookdownloadtimes.append(bookdownloadtime)
               
    pd.DataFrame({'bookname':booknames, 'downloadtime':bookdownloadtimes}).to_csv('downloadtimes.tsv', sep='\t', index=False)
    #%%


if __name__ == "__main__":
    bookdirs = sys.argv[1:]
    
#    bookdirs = ['/Users/dsaunder/Books', 
#    '/Users/dsaunder/Books/Books bought from Amazon, no DRM',
#    '/Users/dsaunder/Books/Books bought from Amazon and De-DRMed']
    extract_book_covers(bookdirs)
    