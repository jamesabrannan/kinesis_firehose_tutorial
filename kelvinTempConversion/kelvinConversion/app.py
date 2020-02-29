import base64
import json
from decimal import Decimal


def lambda_handler(event, context):
    output = []

    for record in event['records']:
        print(record['recordId'])
        payload = base64.b64decode(record['data']).decode('utf-8')
        print(payload)
        reading = json.loads(payload)
        print(reading)
        temp = reading['temp']
        print(temp)
        isfarenheit = bool(temp.upper().find('F') > 0)
        kelvin = 0

        if isfarenheit :
            print(float(temp.upper().strip('F')))
            kelvin = (float(temp.upper().strip('F')) + 459.67) * 5.0 / 9.0
        else:
            kelvin = float(temp.upper().strip('C')) + 273.15

        print("{:.2f}".format(kelvin))

        reading['temp'] = str("{:.2f}".format(kelvin))

        print(reading)

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(json.dumps(reading).encode('UTF-8'))
        }
        output.append(output_record)

    print('Successfully processed {} records.'.format(len(event['records'])))

    return {'records': output}
