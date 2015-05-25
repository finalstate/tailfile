#! /usr/bin/python3
# -*- coding: utf-8 -*-
####################################################################################################

import io

####################################################################################################

def TailFile(p_FileName, p_BufferSize=4096, p_Encoding='utf8', p_Separator = '\n', p_KeepSeparator=True):
    '''
        Iterator used to read a file starting with the end, and proceeding backwards.
        
        p_FileName    : the full path to the file to be read backwards
        p_BufferSize  : the size of the file chunk to read into memory for processing
        p_Encoding    : the encoding of the file, default is utf-8
        p_Separator   : the character(s) used to separate the stream. Usually either newline or space.
        p_KeepNewLine : keep the newline character at the end of the line (to be compatible with readline() )
    '''
    
    l_Separator     = bytes(p_Separator, p_Encoding)
    l_KeepSeparator = l_Separator if p_KeepSeparator else b''
    
    l_Fragments = [] # array of bytes
    with open(p_FileName, 'rb') as l_File:        
        l_File.seek(0, io.SEEK_END)
        l_Blocks = l_File.tell() // p_BufferSize
        
        while l_Blocks >= 0:
            l_File.seek(l_Blocks * p_BufferSize, io.SEEK_SET)
            l_BufferContent = l_File.read(p_BufferSize) # might overshoot at first read
            l_Blocks       -= 1
            
            if not l_Separator in l_BufferContent:
                l_Fragments.append(l_BufferContent)
            
            else:
                l_BufferFragments = l_BufferContent.split(l_Separator)
                yield str(l_BufferFragments[-1] + b''.join(l_Fragments[::-1]) + l_KeepSeparator, p_Encoding)
                    
                for l_BufferFragment in reversed(l_BufferFragments[1:-1]): 
                    yield str(l_BufferFragment + l_KeepSeparator, p_Encoding)
                
                l_Fragments = [l_BufferFragments[0]] 
            
        yield str(b''.join(l_Fragments[::-1]), p_Encoding)

####################################################################################################

if __name__ == '__main__':
    import os
    import sys
    import time

    C_TestFileName   = 'tmp.txt'
    C_TestBufferSize =  4096
    
    if len(sys.argv) != 2:
        print ('Usage: python3 tailfile.py <testfile>')
        sys.exit(0)
    
    if True: # benchmark
        l_Moment1 = time.time()
    
        l_Count1 = 0
        with open(sys.argv[1], 'r') as l_File:
            for l_Line in l_File:
                l_Count1 += 1

        l_Moment2 = time.time()
        
        l_Count2 = 0
        for l_Line in TailFile(sys.argv[1], p_BufferSize=C_TestBufferSize):
            l_Count2 += 1

        l_Moment3 = time.time()
        
        print ('{}: {} {}'.format(l_Count1, (l_Moment2 - l_Moment1), (l_Moment3 - l_Moment2)))
        
    else: # test algorithm
        # write reversed content to tmp file
        with open(C_TestFileName, 'w') as l_TempFile:
            for l_Line in TailFile(sys.argv[1], C_TestBufferSize, p_Separator='\n'):
                l_TempFile.write(l_Line)
#                print (l_Line, end='')
                
        # read and compare original file to reversed tmp file, should be identical
        for l_Line, l_Copy in zip(open(sys.argv[1], 'r'), TailFile(C_TestFileName, C_TestBufferSize)):
            if l_Line != l_Copy:
                print ('|'+l_Line+'|\n---\n|'+l_Copy+'|')
                break
            
#        os.remove(C_TestFileName)    