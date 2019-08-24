from .json_encoder import JSONEncoder
import json

responseFormater = {
    'success': True,
    'status_code': 200,
    'message': '',
    'data': []
}


def resultToResponse(result):
    res = responseFormater.copy()
    try:
        res['success'] = result[0]
        res['status_code'] = result[1]
        res['message'] = result[2]['message']
        if result[0]:
            res['data'] = json.loads(json.dumps(result[2]['data'], cls=JSONEncoder))
    except:
        print('Can not conver result to response')
    return res