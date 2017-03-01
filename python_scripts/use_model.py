import base64
import sys
import os
from sklearn.externals import joblib
from BagOfWords import BagOfWords

save_name_model = 'model_v1'
save_name_bag = 'bag_v1'
dir_name = 'model'
save_path_model = os.path.join(os.path.join(os.path.dirname(__file__), '/'.join((dir_name, save_name_model))))
save_path_bag = os.path.join(os.path.join(os.path.dirname(__file__), '/'.join((dir_name, save_name_bag))))

model = joblib.load(save_path_model)
bag = joblib.load(save_path_bag)


def predict(sentence):
    X = bag.transform([sentence])
    y_hat = model.predict(X)

    return y_hat[0]

while True:
    input_msg = base64.b64decode(raw_input()).split(' ')
    msg_id = input_msg[0]
    message = ' '.join(input_msg[1:])

    result = predict(message)

    output = ' '.join([msg_id, result])
    encoded = base64.b64encode(output)
    print encoded
    sys.stdout.flush()