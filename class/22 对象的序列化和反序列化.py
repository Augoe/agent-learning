# import json

# text = '''
# {
#     "name": "search",
#     "arguments": {
#         "query": "AI Agent"
#     }
# }
# '''

# object = json.loads(text)
# print(object['name'])
# print(object['arguments']['query'])


# import json

# object={
#     "name":"search",
#     "arguments":{
#         "a":"10",
#         "b":"20",
#     }
# }

# text=json.dumps(object,ensure_ascii=False,indent=2)
# print(text)

# with open("hello.txt", "w", encoding="utf-8") as f:
#     f.write("hello agent")

# with open("hello.txt", "r", encoding="utf-8") as f:
#     text = f.read()

# print(text)

# import json

# # data = {
# #     "name": "search",
# #     "query": "Agent"
# # }

# # with open("tool_call.json", "w", encoding="utf-8") as f:
# #     json.dump(data, f, ensure_ascii=False, indent=2)

# with open("tool_call.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# print(data)


## 配合tool.py使用

# from tool import calculator as cal
# import tool
# print(tool.calculator(10,20))
# print(tool.search("6666"))

from tool import calculator as cal, search as se
print(cal(10, 20))
print(se("6666"))
