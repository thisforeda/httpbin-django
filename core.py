from .http_status import *
from django.http import HttpResponse
from json import dumps as _dump_json

def JsonResponse (data = {}, status = 200, headers = {}):
    response = HttpResponse (
        _dump_json (data, indent = 4, ensure_ascii = False) ,
        status = status ,
        content_type = "text/json; charset=utf-8"
    )
    for k, v in headers.items():
        response[k] = v
    return response

def meta_headers (req):
    """ yield tuple (key, value) """
    for k in req.META :
        if k.startswith ("HTTP_") :
            yield \
            (
                "-".join ([
                    m.capitalize() for m in k [5:].split("_")
                ]) ,
                req.META [k]
            )

def redirect_header (url):
    return \
    {
        "Location" : url
    }

class httpbin :

    def user_agent (req):
        return JsonResponse (
            data = \
            {
                "user-agent" : req.META.get("HTTP_USER_AGENT", "")
            },
        )

    def ip (req):
        return JsonResponse (
            data = \
            {
                "origin" : req.META.get("REMOTE_ADDR")
            }
        )
    
    def headers (req):
        return JsonResponse (
            data = \
            {
                "headers" : dict ([
                    tup for tup in meta_headers (req)
                ]),
            }
        )
    
    def get (req):
        return JsonResponse (
            data = \
            {
                "url" : req.get_raw_uri(),
                "origin" : req.META.get("REMOTE_ADDR"),
                "args" : dict([
                    (k, req.GET[k]) for k in req.GET
                ]),
                "headers" : dict ([
                        tup for tup in meta_headers (req)
                ]),
            }
        )

    def status (req):
        code = req.GET.get("code")
        if not code or (code not in STATUS_CODE):
            return JsonResponse (
                data = {
                    "~ (¯(∞)¯)" : "Fuck U!（*>.<*） You Cheat M ee!!"
            })
        return JsonResponse (
            status = int(code) ,
            data = {code : STATUS_CODE[code]}
        )
            
    def cookies_del (req):
        response = JsonResponse (
            status = 302 ,
            headers = redirect_header ("/cookies")
        )
        c_names = req.GET.get("name")
        if c_names :
            for k in c_names.split(",") :
                if k :
                    response.delete_cookie(k)
        return response
    
    def cookies_set (req):
        response = JsonResponse (
            status = 302 ,
            headers = redirect_header ("/cookies")
        )
        for k in req.GET :
            response.set_cookie(k, req.GET[k])
        return response
    
    def cookies (req):
        return JsonResponse (
            data = \
            {
                "cookies" : dict ([
                    (k, req.COOKIES[k]) for k in req.COOKIES
                ])
            })
    
    def response_headers (req):
        response = JsonResponse (
            data = dict ([
            (k, req.GET[k]) for k in req.GET
        ]))
        for k in req.GET :
            response[k] = req.GET[k]
        return response
            
    def redirect_to (req):
        url = req.GET.get("url", "http://www.example.com").lower()
        if not url.startswith ("http"):
            url = "http://" + url
        return JsonResponse (
            status = 302 ,
            headers = \
            {
                "Location" : url
            })





