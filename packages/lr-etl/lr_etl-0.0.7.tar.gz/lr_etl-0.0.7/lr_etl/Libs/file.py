import os
import glob
import shutil
import time
from lr_etl.Libs.log import Log

class FileUteis():

    def createFolder(folder,replace=False):
        if not os.path.isdir(folder):
            os.mkdir(folder)
        if replace:
            os.remove(folder)
            os.mkdir(folder)

    def moveFiles(pattern, place):
        files = glob.glob(pattern)
        for f in files:
            fnm = os.path.basename(f)
            # shutil.copy(f, DIR +  fr'\{place}.xls')
            shutil.copy(f,f"{place}/{fnm}")
            os.remove(f)

    def clearFolder(folder):
        files = glob.glob(folder + "\*.*")
        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                Log.warning(f"erro ao excluir arquivos do storage: {str(e)}")

    def waitFileFromChrome(pattern,dirr=None,timeout=0):
        start = time.time()
        dirr =  dirr if dirr else fr'c:\Users\{os.getlogin()}\downloads'
        
        while not glob.glob(f"{dirr}\{pattern}"):
            if timeout and time.time() - start > timeout: raise("Timeout downloading the file")
        
        time.sleep(0.5)

        while glob.glob(dirr + "\*.crdownload"):
            time.sleep(0.5)
            if timeout and time.time() - start > timeout: raise("Timeout downloading the file")
        
        list_of_files = glob.glob(f"{dirr}\{pattern}") # * means all if need specific format then *.csv
        return max(list_of_files, key=os.path.getctime)

    def renameFile(fl,newName):
        path = os.path.dirname(os.path.abspath(fl))
        os.rename(fl,f"{path}\{newName}")
        return f"{path}\{newName}"

    def getFileName(addrs):
        return os.path.basename(addrs)
        



# d = DateUteis()
# a = d.lastWorkingDate(fmt="%Y-%m-%d")
# a=1
