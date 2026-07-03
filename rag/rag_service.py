from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda

from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompt
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model

def print_prompts(prompts):
    print("-"*20)
    print(prompts.to_string())
    print("-"*20)
    return prompts
class RagSummerizeService:
    def __init__(self):
        self.vectorstore= VectorStoreService()
        self.retriever = self.vectorstore.retriever()
        self.prompts_txt = load_rag_prompt()
        self.prompts_template =PromptTemplate.from_template(self.prompts_txt)
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        chain = self.prompts_template | RunnableLambda(print_prompts) | self.model | StrOutputParser()
        return chain

    #用检索器返回查询内容
    def retriever_docs(self, query)->list[Document]:
        return  self.retriever.invoke(query)

    #把查询内容存入链中
    def rag_summerize(self, query) -> str:
        contxt_docs = self.retriever_docs(query)
        context = ""
        counter = 0
        for doc in contxt_docs:
            counter += 1
            context += f"参考资料{counter}:{doc.page_content},参考元数据{doc.metadata}\n"

        return self.chain.invoke({"input": query, "context": context})
if __name__ == "__main__":
    rag =RagSummerizeService()
    print(rag.rag_summerize("小户型适合什么机器人"))