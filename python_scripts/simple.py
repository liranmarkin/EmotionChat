import base64
import sys

while True:
    input = base64.b64decode(raw_input()).split(' ')
    id = input[0]
    message = ' '.join(input[1:])

    result = 'emotion'

    output = ' '.join([id, result])
    encoded = base64.b64encode(output)
    print encoded
    sys.stdout.flush()