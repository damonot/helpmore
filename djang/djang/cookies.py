import datetime

global EXPR
EXPR = datetime.datetime(2025, 5, 17)


def main(request):
    pass

def getcookie(request):
    donation_cookie = int( request.COOKIES.get('donation', '0') )
    print(donation_cookie)
    return donation_cookie


def setcookie(response, submitteddono):
    return response.set_cookie('donation', submitteddono, expires=EXPR)