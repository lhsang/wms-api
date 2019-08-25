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
    except Exception as e:
        print(str(e))
    return res


def setAssociationToResponse(res, data, att):
    try:
        index = 0
        while index < len(res['data']):
            res['data'][index][att] = json.loads(json.dumps(getattr(data[index], att), cls=JSONEncoder))
            index += 1
    except Exception as e:
        print(str(e))
    finally:
        return res
