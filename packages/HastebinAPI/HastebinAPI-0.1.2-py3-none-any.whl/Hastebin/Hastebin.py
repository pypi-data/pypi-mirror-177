import sys
import json
import requests

def CreatePaste(content="", **kwargs):
    pt = kwargs.get("print", False)
    fullurl = kwargs.get("fullurl", True)
    if content == "":
        print("Hastebin API Error: CreatePaste was called but text was not provided.")
        sys.exit()
    try:
        request = requests.post("https://hastebin.com/documents", content)
        request = json.loads(str(request.text))
    except:
        print("Hastebin API Error: Could not establish a connection to Hastebin.")
        sys.exit()
    result = ""
    if fullurl == False:
        result = request["key"]
    else:
        result = "https://hastebin.com/raw/" + request["key"]
    if pt == True:
        print(result)
    return result

def GetPaste(paste, **kwargs):
    pt = kwargs.get("print", False)
    result = ""
    if paste == "":
        print("Hastebin API Error: CreatePaste was called but text was not provided.")
        sys.exit()
    if "hastebin.com" in paste:
        if "hastebin.com/raw" in paste:
            try:
                request = requests.get(paste)
                if request.text == '{"message":"Document not found."}':
                    print("Hastebin API Error: The requested document was not found.")
                else:
                    result = request.text
            except:
                print("Hastebin API Error: Could not establish a connection to Hastebin.")
        else:
            paste = paste.replace("https", "").replace("://", "").replace("hastebin", "").replace(".com", "")
            paste = paste[1:]
            if paste.find(".") != -1:
                paste = paste[:paste.find(".")]
            paste = "https://hastebin.com/raw/" + paste
            try:
                request = requests.get(paste)
                if request.text == '{"message":"Document not found."}':
                    print("Hastebin API Error: The requested document was not found.")
                else:
                    result = request.text
            except:
                print("Hastebin API Error: Could not establish a connection to Hastebin.")
    else:
        try:
            request = requests.get("https://hastebin.com/raw/" + paste)
            if request.text == '{"message":"Document not found."}':
                print("Hastebin API Error: The requested document was not found.")
            else:
                result = request.text
        except:
            print("Hastebin API Error: A valid Hastebin URl was not provided.")
    if pt == True:
        print(result)
    return result