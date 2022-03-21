import requests
import json


def main( request ):

    # Your API Key
    # You can get your API Key by following these instructions:
    # https://developers.whatismybrowser.com/api/docs/v2/integration-guide/#introduction-api-key

    api_key = "4792c488bd5227618219e639c8324ee5"

    # user agent to parse:
    #user_agent = request.META['HTTP_USER_AGENT']
    user_agent = request.headers['User-Agent']
    

    # Where will the request be sent to
    api_url = "https://api.whatismybrowser.com/api/v2/user_agent_parse"

    # -- Set up HTTP Headers
    headers = {
        'X-API-KEY': api_key,
    }

    # -- prepare data for the API request
    # This shows the `parse_options` key with some options you can choose to enable if you want
    # https://developers.whatismybrowser.com/api/docs/v2/integration-guide/#user-agent-parse-parse-options
    post_data = {
        'user_agent': user_agent,
        "parse_options": {
            "allow_servers_to_impersonate_devices": True,
            "return_metadata_for_useragent": True,
            # "dont_sanitize": True,
        },
    }

    # -- Make the request
    result = requests.post(api_url, data=json.dumps(post_data), headers=headers)

    # -- Try to decode the api response as json
    result_json = {}
    try:
        result_json = result.json()
    except Exception as e:
        print(result.text)
        print("Couldn't decode the response as JSON:", e)
        exit()


    # -- Check that the server responded with a "200/Success" code
    if result.status_code != 200:
        print("ERROR: not a 200 result. instead got: %s." % result.status_code)
        print(json.dumps(result_json, indent=2))
        exit()


    # -- Check the API request was successful
    if result_json.get('result', {}).get('code') != "success":
        print("The API did not return a 'success' response. It said: result code: %s, message_code: %s, message: %s" % (result_json.get('result', {}).get('code'), result_json.get('result', {}).get('message_code'), result_json.get('result', {}).get('message')))
        #print(json.dumps(result_json, indent=2))
        exit()

    # Now you have "result_json" and can store, display or process any part of the response.

    # -- print the entire json dump for reference
    #print(json.dumps(result_json, indent=2))


    # -- Copy the data to some variables for easier use
    parse = result_json.get('parse')
    version_check = result_json.get('version_check')

    #print(parse)

    # Now you can do whatever you need to do with the parse result
    
    return (parse)
