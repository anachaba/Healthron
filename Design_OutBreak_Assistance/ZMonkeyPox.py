from tensorflow.keras.models import load_model
import numpy as np

import cv2
from imutils.video import VideoStream
vs = VideoStream(src="https://192.168.43.1:8080/video").start()
#vs = VideoStream(src="./Pics/night_drive.mp4").start()
# vs = VideoStream(src=0).start()

class_names = ["MonkeyPox", "NoMonkeyPox"]

model = load_model(r'C:\Program Files\Innovation projects\CovidEnforcement\MaskCheck\Disease_OutBreak_Assistance\Models\monkeyPox_model.h5')
renderSpeed = 20
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

while True:

    frame = vs.read()

    img = cv2.resize(frame, (224, 224))
    img = np.reshape(img, [1, 224, 224, 3])

    k = 1
    confidences = np.squeeze(model.predict(img))
    classs = np.argmax(confidences)
    name = class_names[classs]
    top_conf = confidences[classs]

    inds = np.argsort(-confidences)
    top_k = inds[:k]
    top_confidences = confidences[inds]

    for i, (conf, ind) in enumerate(zip(top_confidences, top_k)):
        new_confi = 100 * conf
        status = str(class_names[ind])

        new_confi=round(new_confi,2)


        cv2.putText(frame, f'Confidence: {new_confi}%', (440, 620), 0, 1, (255, 255, 255), 2)

        # print(f'Class #{i + 1} - {class_names[ind]} - Confidence: {new_confi}%')
        print(f'Detection is Activated as - {class_names[ind]} - With Confi as: {new_confi}%')
    if new_confi >= 85 and status == 'MonkeyPox':
        cv2.rectangle(frame, (40, 820), (150, 640), (255, 0, 0), -5)
        cv2.putText(frame, f'{class_names[ind]}', (440, 570),0, 1, (56, 255, 255), 2)


    cv2.imshow('Light System', frame)
    k = cv2.waitKey(renderSpeed) & 0xff
    if k == 27:
        break

vs.release()
cv2.destroyAllWindows()
