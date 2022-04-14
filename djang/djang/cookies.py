import datetime

global EXPR
EXPR = datetime.datetime(2025, 5, 17)


def main(request):
    pass

def getcookie(request):
    
    if(request.COOKIES.get('donation', '0') == "None"):
        # print("reached")
        donation_cookie = 0
    else:
        donation_cookie = int( request.COOKIES.get('donation', '0') )

    #print("GET COOKIE: "+ str(donation_cookie))
    return donation_cookie


def setcookie(response, submitteddono):
    return response.set_cookie('donation', submitteddono, expires=EXPR)