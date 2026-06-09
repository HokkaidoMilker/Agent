import  os

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from utils.LoggerHandler import  get_logger
import hashlib
logger = get_logger()
#文件转化为md5
def get_file_md5_hex(file_path):

    if not os.path.exists(file_path):
        logger.warning("文件路径不存在")
    if not os.path.isfile(file_path):
        logger.warning("请传入md5文件")
    md5_obj = hashlib.md5()

    chunk_size=4096 #避免文件过大爆内存

    #读取文件转化为md5
    try:
        with open(file_path,"rb") as f:
            chunk = f.read(chunk_size)
            while chunk:
                md5_obj.update(chunk)
                chunk = f.read(chunk_size)
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"获取文件md5失败,文件名{file_path}")

#处理文件列表
def dirlist(file_path,type:tuple[str]):
    files=[]
    if not os.path.isdir(file_path):
        return logger.warning("请传入一个文件夹")
    for f in os.listdir(file_path):
        if f.endswith(type):
            files.append(os.path.join(file_path,f))
    return tuple(files)

#pdf加载器
def pdf_loader(file_path,password=None)->list[Document]:
    return  PyPDFLoader(file_path,password).load()

#txt加载器
def txt_loader(file_path,password=None)->list[Document]:
    return  TextLoader(file_path,encoding="utf-8").load()






