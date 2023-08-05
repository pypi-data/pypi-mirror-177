import aligo
import os
ali = aligo.Aligo()

def clean_cloud_folder(folder_id):
    exist_info = ali.get_file_list(folder_id)
    print('已存在文件:',[i.name for i in exist_info])
    for fobj in exist_info:
        ali.move_file_to_trash(fobj.file_id)

def clean_local_folder(downloadfiles,targetfolder):
    filelist = os.listdir(targetfolder)
    for f in downloadfiles:
        if f in filelist:
            os.remove(targetfolder+f)

def size_checker(cloudfileobj,f,localfolder):
    localsize = os.path.getsize(localfolder+f)
    cloudsize = cloudfileobj.size
    if localsize < cloudsize:
        print('下载文件size:{};小于云盘文件size:{};差额:{}'.format(localsize,cloudsize,cloudsize-localsize))
        print('重新下载')
        return False
    else:
        print('文件大小校验通过')
        return True

def uploader(foldid,filelist):
    clean_cloud_folder(foldid)
    for f in filelist:
        ali.upload_file(f,foldid)

def downloader(sourcefolderid,downloadfiles,targetfolder):
    clean_local_folder(downloadfiles,targetfolder)
    exist_info = ali.get_file_list(sourcefolderid)
    for f in exist_info:
        if f.name in downloadfiles:
            ali.download_file(file = f,local_folder = targetfolder)   
            checker_pass = size_checker(f,f.name,targetfolder)             
            while not checker_pass:
                os.remove(targetfolder+f)
                ali.download_file(file = f,local_folder = targetfolder)
                checker_pass = size_checker(f,f.name,targetfolder)    