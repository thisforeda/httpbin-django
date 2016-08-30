
from .core import httpbin,JsonResponse

URI_MAP = \
{
    "user-agent" : httpbin.user_agent,
    "ip"         : httpbin.ip,
    "headers"    : httpbin.headers,
    "get"        : httpbin.get,
    "redirect-to" : httpbin.redirect_to,
    "response-headers" : httpbin.response_headers,
    "cookies"    : httpbin.cookies,
    "cookies-del" : httpbin.cookies_del,
    "cookies-set" : httpbin.cookies_set,
    "status"    : httpbin.status,
}

def httpbin_handler (req, uri = None) :
    try :
        return URI_MAP[uri] (req)
    except : 
        return JsonResponse (
            status = 500 ,
            data = {
                "对不起" : "|*_*| 程序好像发生了一个错误."
            }
        )

            
    
