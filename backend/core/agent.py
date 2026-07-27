import json

from fastapi import HTTPException
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from backend.schemas.agent import NameResultSchema
from backend.schemas.name import NameIn
from backend.settings import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL


SYSTEM_PROMPT = """
你是一位精通汉语言文学、音韵学与传统文化的命名专家。
请结合用户提供的姓氏、性别、名字长度与偏好，给出 6 个候选姓名。
名字应发音自然、寓意积极、适合现代语境，并优先从《诗经》《楚辞》、
唐诗宋词、成语典故等经典文化中寻找有依据的灵感。
每个结果必须包含完整姓名、准确简洁的出处，以及名字的字义与整体寓意。
""".strip()


async def generate_names(name_info: NameIn) -> NameResultSchema:
    if not DEEPSEEK_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="AI 服务尚未配置，请设置 DEEPSEEK_API_KEY",
        )

    llm = ChatOpenAI(
        model=DEEPSEEK_MODEL,
        temperature=0.8,
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,
    )
#    structured_llm = llm.with_structured_output(NameResultSchema)
    excluded = "、".join(name_info.exclude) if name_info.exclude else "无"
    prompt = (
        f"姓氏：{name_info.surname}\n"
        f"性别：{name_info.gender}\n"
        f"名字字数：{name_info.length}\n"
        f"其他要求：{name_info.other or '无'}\n"
        f"避用字或姓名：{excluded}"
    )
    response = await llm.ainvoke(
        [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)]
    )
    
        # 手动解析 JSON
    try:
        content = response.content
        # 尝试提取 markdown 代码块中的 JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        data = json.loads(content.strip())
        return NameResultSchema(**data)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI 返回格式异常: {str(e)}\n原始响应: {response.content[:500]}"
        )
