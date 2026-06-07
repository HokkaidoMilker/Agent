from utils.config_handler import promts_config
from utils.path_tool import get_abs_path
from utils.LoggerHandler import logger
#导入系统提示词
def load_system_prompt():
    try:
        system_prompts_path=get_abs_path(promts_config["main_prompt_path"])
    except KeyError as e:
        logger.error(f"{e},没有找到main_prompt_path")
    try:
        return open(system_prompts_path,"r",encoding="utf-8").read()
    except FileNotFoundError as e:
        logger.error(f"{e},系统提示词解析错误")
#导入rag提示词
def load_rag_prompt():
    try:
        rag_prompts_path=get_abs_path(promts_config["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"{e},没有找到rag_summarize_prompt_path")
    try:
        return open(rag_prompts_path,"r",encoding="utf-8").read()
    except FileNotFoundError as e:
        logger.error(f"{e},系统提示词解析错误")
#导入report提示词
def load_report_prompt():
    try:
        report_prompts_path=get_abs_path(promts_config["report_prompt_path"])
    except KeyError as e:
        logger.error(f"{e},没有找到report_prompt_path")
    try:
        return open( report_prompts_path,"r",encoding="utf-8").read()
    except FileNotFoundError as e:
        logger.error(f"{e},系统提示词解析错误")

if __name__=="__main__":
    load_system_prompt()
    load_rag_prompt()
    load_report_prompt()