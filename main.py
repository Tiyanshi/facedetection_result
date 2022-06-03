import numpy as np
import cv2
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

with_mask = np.load('with_mask.npy')
without_mask = np.load('without_mask.npy')
with_mask = with_mask.reshape(300, 50*50*3)
without_mask = without_mask.reshape(300, 50*50*3)
X = np.r_[with_mask, without_mask]
labels = np.zeros(X.shape[0])
labels[200:] = 1.0
names = {0: 'Mask', 1: 'No Mask'}
x_train, x_test, y_train, y_test = train_test_split(X, labels, test_size=0.25)
pca = PCA(n_components=3)
x_train = pca.fit_transform(x_train)
x_train, x_test, y_train, y_test = train_test_split(X, labels, test_size=0.20)
svm = SVC()
svm.fit(x_train, y_train)
x_test = pca.transform(x_test)
y_pred = svm.predict(x_test)
accuracy_score(y_test, y_pred)

video = cv2.VideoCapture(0)
haar_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
data = []
font = cv2.FONT_HERSHEY_PLAIN

while True:
    flag, img = video.read()
    if flag:
        faces = haar_data.detectMultiScale(img)
        for x, y, w, h in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 4)
            face = img[y:y+w, x:x+w, :]
            face = cv2.resize(face, (50, 50))
            face = face.reshape(1, -1)
            #face = pca.transform(face)
            pred = svm.predict(face)
            n = names[int(pred)]
            cv2.putText(img, n, (x, y), font, 1, (244, 250, 250), 2)
            print(n)
        cv2.imshow("result", img)
        if cv2.waitKey(2) == 27:
            break
video.release()
cv2.destroyAllWindows()
np.save('with_mask.npy', data)
