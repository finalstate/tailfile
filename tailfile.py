#! /usr/bin/python3
# -*- coding: utf-8 -*-
####################################################################################################

import io
import os
import pprint
import subprocess
import sys
import time

####################################################################################################

def TailFile(p_FileName, p_BufferSize=4096, p_Encoding='UTF8'):
    l_Remaining = bytes()
    
    with open(p_FileName, 'rb') as l_File:        
        l_File.seek(0, io.SEEK_END)
        l_Done = False
        while not l_Done:
            if l_File.tell() >= p_BufferSize:
                l_File.seek(-p_BufferSize, io.SEEK_CUR)
                l_BufferContent = l_File.read(p_BufferSize)
                l_File.seek(-p_BufferSize, io.SEEK_CUR)
            else:
                l_RemainingSize = l_File.tell()
                l_File.seek(0, io.SEEK_SET)
                l_BufferContent = l_File.read(l_RemainingSize)
                l_Done = True
                
            l_BufferLines = l_BufferContent.splitlines()
            
            yield str(l_BufferLines[-1] + l_Remaining, p_Encoding)
            for l_Line in reversed(l_BufferLines[1:-1]):
                yield str(l_Line, p_Encoding)
                
            l_Remaining = l_BufferLines[0]
        
        yield str(l_Remaining, p_Encoding)
    
####################################################################################################

if __name__ == '__main__':
    import io
    import os
    import sys
    import time

    if len(sys.argv) != 2:
        print ('Usage: python tailfile.py <testfile>')
        sys.exit(0)
   
    for l_Lines in TailFile(sys.argv[1]):
        print (l_Lines)
