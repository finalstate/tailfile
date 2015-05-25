#! /usr/bin/python3
# -*- coding: utf-8 -*-
####################################################################################################

import io

####################################################################################################

def TailFile(p_FileName, p_BufferSize=4096, p_Encoding='utf8', p_Separator = '\n', p_KeepSeparator=True):
    '''
        Iterator used to read a file starting with the last line, and proceeding backwards.
        The lines read do NOT contain the newline.
        
        p_FileName    : the full path to the file to be read backwards
        p_BufferSize  : the size of the file chunk to read into memory for processing
        p_Encoding    : the encoding of the file, default is utf-8
        p_Separator   : the character(s) used to separate the stream. Usually either newline or space.
        p_KeepNewLine : keep the newline character at the end of the line (to be compatible with readline() )
    '''
    
    l_Separator = bytes(p_Separator, p_Encoding)
    l_Joiner    = l_Separator if p_KeepSeparator else b''
    
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
                continue
            
            else:
                l_Right = len(l_BufferContent)
                l_Left  = l_BufferContent.rfind(l_Separator, 0, l_Right)
                while l_Left != -1:
                    l_Fragments.append(l_BufferContent[l_Left+1:l_Right])
                    l_Right = l_Left
                    l_Left  = l_BufferContent.rfind(l_Separator, 0, l_Right)
                    
                    yield str(b''.join(list(reversed(l_Fragments)))+l_Joiner, p_Encoding)
                    
                    l_Fragments = []
                l_Fragments = [l_BufferContent[0:l_Right]]
                
        yield str(b''.join(list(reversed(l_Fragments))), p_Encoding)

####################################################################################################

if __name__ == '__main__':
    import os
    import sys

    C_TestFileName   = 'tmp.txt'
    C_TestBufferSize =  4092
    
    if len(sys.argv) != 2:
        print ('Usage: python3 tailfile.py <testfile>')
        sys.exit(0)
        
    # write reversed content to tmp file
    with open(C_TestFileName, 'w') as l_TempFile:
        for l_Line in TailFile(sys.argv[1], C_TestBufferSize, p_Separator='\n'):
            l_TempFile.write(l_Line)
            
    # read and compare original file to reversed tmp file, should be identical
    for l_Line, l_Copy in zip(open(sys.argv[1], 'r'), TailFile(C_TestFileName, C_TestBufferSize)):
        if l_Line != l_Copy:
            print ('|'+l_Line+'|\n---\n|'+l_Copy+'|')
            break
        
    os.remove(C_TestFileName)    