import os
from server import PromptServer
from aiohttp import web
import json

class Cancelled(Exception):
    pass
def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return '{}'
    except Exception as e:
         return '{}'
    return None
def string_to_json(json_string):
    try:
        json_object = json.loads(json_string)
        return json_object
    except json.JSONDecodeError as e:
        return None
    
@PromptServer.instance.routes.get("/fk_server")
async def fksapi(request):
         tget = request.rel_url.query
         gtype =  tget['type']         
         if gtype == "getpz":
                config_path = os.path.join(os.path.dirname(__file__), "ini.json")
                return web.json_response(string_to_json(read_file_content(config_path)), content_type='application/json')
         elif gtype == "getslpz":
                config_path = os.path.join(os.path.dirname(__file__), "server/data.json")
                return web.json_response(string_to_json(read_file_content(config_path)), content_type='application/json')
         elif gtype == "delslpz":
               config_path = os.path.join(os.path.dirname(__file__), "server/data.json")
               try:
                   os.remove(config_path)
                   return web.json_response({"v":gtype}, content_type='application/json')
               except OSError:
                  return web.json_response({"v":gtype}, content_type='application/json')               
         else:
             return web.json_response({"v":gtype}, content_type='application/json')
@PromptServer.instance.routes.get("/fkhome")
async def fkweb(request): 
         return web.Response(
                text="hi",
                content_type="text/html",
            )
@PromptServer.instance.routes.post('/fk_server')
async def fkpostapi(request):
    post = await request.post()
    bdappid = post.get("bdappid")
    bdappkey = post.get("appbdkey") 
    zhitsc = post.get("zhitsc")
    zhipukey = post.get("zhipukey") 
    if bdappid and bdappkey:
        config_path = os.path.join(os.path.dirname(__file__), "ini.json")
        config_data = string_to_json(read_file_content(config_path))
        print(f"Comfyui_fk_server：密钥设置成功")
        config_data["appid"] = bdappid
        config_data["key"] = bdappkey
        config_data["zhitsc"] = zhitsc
        config_data["zhipukey"] = zhipukey
        with open(config_path, 'w', encoding='utf-8') as file:
             json.dump(config_data, file, ensure_ascii=False, indent=4)
    return web.json_response({})



print(f"\33[93m》===>====>========>Fk_Server:OK!<========<====<===《\33[0m")

