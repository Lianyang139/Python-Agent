#langchain_ollama包，ollama需要启动
# Ollama官网：https://ollama.com/search

from langchain_ollama import OllamaLLM
from sqlalchemy.testing.suite.test_reflection import users

ollama_model = OllamaLLM(model="qwen3:4b")

print("输入：quit 退出")

while True:
    # 获取用户输入
    users_input = input("\n你：").strip()

    if users_input.lower() in ["exit","quit","q"]:
        print("bye")
        break
    if not users_input:
        continue # 忽略输入

    try:
        res = ollama_model.invoke(input=users_input)
        print(f"🤖: {res}")
    except Exception as e:
        print(f"❌ 出错了: {e}")