from langchain_chroma import Chroma
from utils.config_handler import chroma_config
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.path_tool import get_abs_path
import os
from utils.file_handler import pdf_loader,txt_loader,dirlist,get_file_md5_hex
from utils.LoggerHandler import logger

from langchain_core.documents import Document
class VectorStoreService:
    def __init__(self):
        self.vector_store=Chroma(
            collection_name=chroma_config["collection_name"],
            persist_directory= chroma_config["persist_directory"],
            embedding_function=embed_model

        )

        self.splitter=RecursiveCharacterTextSplitter(
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            separators=chroma_config["separators"],
            length_function=len



        )
    #获取向量检索器
    def retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k":chroma_config["k"]})

    # 检查md5字符串去重
    def load_document(self):

        def check_md5_hex(md5_for_check:str):
            if not os.path.exists(get_abs_path(chroma_config["md5_hex_store"])):
                open(get_abs_path(chroma_config["md5_hex_store"]),"w",encoding="utf-8").close()
                return False
            with open(get_abs_path(chroma_config["md5_hex_store"]),"r",encoding="utf-8") as f:
                for line in f.readlines():
                    line= line.strip()
                    if line==md5_for_check:
                        return True
                return False
        #把md5字符串写入到文件中
        def save_md5_hex(md5_for_add:str):
            with open(get_abs_path(chroma_config["md5_hex_store"]),"a",encoding="utf-8") as f:
                f.write(md5_for_add+"\n")
        #读取文件转换成md5字符串
        def get_file_Documents(file_path:str):
            if file_path.endswith(".txt"):
                return txt_loader(file_path)
            if file_path.endswith(".pdf"):
                return pdf_loader(file_path)

            return []
        #允许的文件列表
        allow_file_path=dirlist(get_abs_path(chroma_config["data_path"]),tuple(chroma_config["allow_knowledge_file_type"]))

        #获取文件的md5
        for path in allow_file_path:
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f"加载路径{path}已经在向量库中")
                continue
            #文本分割
            try:
                documents:list[Document]=get_file_Documents(path)

                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本,跳过")
                    continue
                splits_document:list[Document]=self.splitter.split_documents(documents)

                if not splits_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本,跳过")
                    continue

                self.vector_store.add_documents(splits_document)
                save_md5_hex(md5_hex )#记录这个已经处理好的md5文件避免下次重复加载
                logger.info(f"[加载知识库]{path}内容加载成功")
            except Exception as e:
                logger.error(f"[加载知识库]{path}失败:{str(e)}",exc_info=True)
                continue
if __name__ =="__main__":
    vs = VectorStoreService()
    vs.load_document()
    retriever = vs.retriever()
    res = retriever.invoke("迷路")
    for line in res:
        print(line.page_content)
        print("-"*20)





















