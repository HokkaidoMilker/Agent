from abc import ABC, abstractmethod
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel,ChatTongyi
from utils.config_handler import rag_config
from langchain_community.embeddings import DashScopeEmbeddings

class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self)->[Embeddings|BaseChatModel]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self) ->[Embeddings|BaseChatModel]:
        return ChatTongyi(model=rag_config["chat_model_name"])

class EmbeddingsFactory(BaseModelFactory):
    def generator(self) ->[Embeddings|BaseChatModel]:
        return DashScopeEmbeddings(model=rag_config["embedding_model_name"])

chat_model_factory = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()