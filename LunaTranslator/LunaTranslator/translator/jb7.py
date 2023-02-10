
from utils.subproc import subproc    
from translator.basetranslator import basetrans 
import ctypes 
import os 
import subprocess
from utils.subproc import subproc
class TS(basetrans): 
    # def inittranslator(self ) : 
        
    #     if platform.architecture()[0]=='32bit':
    #         self._x64=False
    #         try:
    #             self.dll=  ctypes.CDLL(self.path)
    #         except:
    #             pass
    #     else:
    #         self._x64=True
    #         self.x64('おはおよう')
    def inittranslator(self ) : 
        self.path=None
        self.userdict=None
    def end(self):
        try:
            self.engine.kill()
        except:
            pass
    def checkpath(self):
        if self.config['args']['路径']=="":
            return False
        if os.path.exists(self.config['args']['路径'])==False:
            return False
        if   self.config['args']['路径']!=self.path or self.userdict!=(self.config['args']['用户词典1(可选)'],self.config['args']['用户词典2(可选)'],self.config['args']['用户词典3(可选)']):
            self.path=self.config['args']['路径']
            self.userdict=(self.config['args']['用户词典1(可选)'],self.config['args']['用户词典2(可选)'],self.config['args']['用户词典3(可选)'])
            self.dllpath=os.path.join(self.path,'JBJCT.dll')
            dictpath=''
            for d in self.userdict:
                if os.path.exists(d):
                    d=os.path.join(d,'Jcuser')
                    dictpath+=f' "{d}" '
            try:
                self.engine.kill()
            except:
                pass
            #self.engine=subproc(f'./files/x64_x86_dll/jbj7.exe "{self.dllpath}"'+dictpath,stdin=subprocess.PIPE,name='jbj', stdout=subprocess.PIPE ,encoding='utf-16-le')
            self.engine=subproc(f'./files/x64_x86_dll/jbj7.exe "{self.dllpath}"'+dictpath,stdin=subprocess.PIPE , stdout=subprocess.PIPE ,encoding='utf-16-le',name='jbj7')
             
    def x64(self,content:str):   
            if self.tgtlang not in ['936','950']:
                return ''  
            self.checkpath()
            content=content.replace('\r','\n')
            lines=content.split('\n')
            ress=[]
            for line in lines:
                self.engine.stdin.write(self.tgtlang+'\r\n'+line+'\r\n') 
                self.engine.stdin.flush() 
                res=self.engine.stdout.readline() 
                ress.append(res[:-2])  
            return '\n'.join(ress)
    def x86(self,content):
        CODEPAGE_JA = 932
        CODEPAGE_GB = 936
        CODEPAGE_BIG5 = 950
        BUFFER_SIZE = 3000
        # if globalconfig['fanjian'] in [0,1,4]:
        #     code=CODEPAGE_GB
        # else:
        #     code=CODEPAGE_BIG5
        code=CODEPAGE_GB
            
        size = BUFFER_SIZE 
        out = ctypes.create_unicode_buffer(size) 
        buf = ctypes.create_unicode_buffer(size) 
        outsz = ctypes.c_int(size) 
        bufsz = ctypes.c_int(size) 
        try:
            self.dll.JC_Transfer_Unicode( 0, # int, unknown 
                CODEPAGE_JA    , # uint     from, supposed to be 0x3a4 (cp932) 
                code, # uint to, eighter cp950 or cp932 
                1, # int, unknown 
                1, # int, unknown 
                content, #python 默认unicode 所有不用u'
                out, # wchar_t* 
                ctypes.byref(outsz), # ∫ 
                buf, # wchar_t* 
                ctypes.byref(bufsz)) # ∫ 
        except:
            pass
        return out.value
    def translate(self,content): 
         
            return self.x64(content)
        
        
          