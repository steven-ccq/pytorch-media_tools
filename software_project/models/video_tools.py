import cv2
import os
import zipfile

def get_face_video(path_in, path_out, classifier_dir, frequency_choice=1):
    cap = cv2.VideoCapture(path_in)
    classifier = cv2.CascadeClassifier(classifier_dir + 'haarcascade_frontalface_alt.xml')
    suc = cap.isOpened()
    frame_count = 0
    out_count = 0
    frequency_list = [1, 5, 10]
    frequency = frequency_list[frequency_choice]
    while suc:
        suc, frame = cap.read()
        if frame_count % frequency == 0:
            faceRects = classifier.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
            for faceRect in faceRects:
                x, y, w, h = faceRect
                img = frame[y-10:y+h+10, x-10:x+w+10]
                cv2.imwrite(path_out+'/'+str(out_count)+'.jpg', img)
                out_count += 1
        frame_count += 1
    cap.release()
    cv2.destroyAllWindows()

def del_dir(path):
    for root, dirs, files in os.walk(path, False):
        for file in files:
            os.remove(os.path.join(root, file))
        for  dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(path)

def get_zip(path_in, path_out):
    zip_file = zipfile.ZipFile(path_out, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path_in):
        file_path = root.replace(path_in, '')
        for file in files:
            zip_file.write(os.path.join(root, file), os.path.join(file_path, file))
    zip_file.close()
    return zip_file