from django.shortcuts import render
import datetime
import os
from models.video_tools import get_face_video, del_dir, get_zip
import zipfile
from django.http import FileResponse, JsonResponse
import time
import threading
from models.siamese_net import openImg, get_diff
from models.neural_trans_tools import image_loader, img_unloader, style_transfer, cnn_normalization_mean, cnn_normalization_std
import torch
from software_project import settings
from django.core.mail import send_mail
from models.models_loader import classify_model, neural_trans_model

# net = SiameseNetwork()
# net.load_state_dict(torch.load('models/net_params1.pkl'))
#
# neural_trans_cnn.load_state_dict(torch.load('models/vgg19_pretrainedmodel.pth'))
# print("1111111111")

def thread_del_file(path, delay=0):
    if os.path.exists(path):
        time.sleep(delay)
        os.remove(path)

def thread_del_dir(path, delay=0):
    if os.path.exists(path):
        time.sleep(delay)
        del_dir(path)

def thread_send_email(subject, message):
    send_mail(subject=subject,
              message=message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=['1456320989@qq.com'])

def mainPage_page(request):
    if request.method == "GET":
        return render(request, 'mainPage.html')
    else:
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        content = 'name: ' + name + '\n' + 'email: ' + email + '\n' + 'subject: ' + subject + '\n' + message
        t = threading.Thread(target=thread_send_email, args=(subject, content, ))
        t.run()
        return render(request, 'mainPage.html')


def get_face_page(request):
    if request.method == "POST":
        video = request.FILES.get('video')
        frequency_choice = request.POST.get('frequency_choice')
        frequency_choice = int(frequency_choice)
        video_name = video.name
        video_name_list = video_name.split('.')
        if len(video_name_list)!= 2 or video_name_list[1] != 'mp4':
            data = {'check': 1, 'message': 'file is not mp4'}
            return JsonResponse(data)
        video_name = video_name_list[0]
        prefix = str(datetime.datetime.now())
        prefix = prefix[:4] + prefix[5:7] + prefix[8:10] + prefix[11:13] + prefix[14:16] + prefix[17:19]
        video_name = prefix + '_' + video_name

        path_in = os.getcwd() + '/static/media_in/' + video_name
        path_out = os.getcwd() + '/static/media_out/' + video_name
        zip_path = os.getcwd() + '/static/media_out/' + video_name + '.zip'
        classifier_dir = os.getcwd() + '/models/'

        with open(path_in, 'wb') as f:
            for _ in video.chunks():
                f.write(_)
        if not os.path.exists(path_out):
            os.makedirs(path_out)
        get_face_video(path_in, path_out, classifier_dir, frequency_choice=frequency_choice)
        get_zip(path_out, zip_path)
        if os.path.exists(path_in):
            os.remove(path_in)
        if os.path.exists(path_out):
            del_dir(path_out)
        data = {'check': 0, 'message': video_name+'.zip'}
        t1 = threading.Thread(target=thread_del_file, args=(path_in, ))
        t2 = threading.Thread(target=thread_del_dir, args=(path_out, ))
        t1.start()
        t2.start()
        return JsonResponse(data)
    else:
        return render(request, 'get_face.html')

def classify_face_page(request):
    if request.method == "GET":
        return render(request, 'classify_face.html')
    else:
        file_list = request.FILES.getlist('img_dir')
        threshold = request.POST.get('threshold')
        threshold = int(threshold)
        prefix = str(datetime.datetime.now())
        prefix = prefix[:4] + prefix[5:7] + prefix[8:10] + prefix[11:13] + prefix[14:16] + prefix[17:19]
        path_in = os.getcwd() + '/static/media_in/' + prefix
        classify_model.load_model()
        if not os.path.exists(path_in):
            os.makedirs(path_in)
        for img in file_list:
            with open(path_in+'/'+img.name, 'wb') as f:
                for _ in img.chunks():
                    f.write(_)

        img_list = []
        for img in file_list:
            img_name = img.name
            img_path = path_in + '/' + img.name
            img = openImg(img_path)
            img_list.append((img_name, img))

        class_list = []
        max_diff = 0.5 + threshold * 0.1
        # for img1 in img_list:
        #     min_diff = 100
        #     x = 0
        #     l = len(class_list)
        #     for i in range(l):
        #         for img2 in class_list[i]:
        #             diff = get_diff(net, img1[1], img2[1])
        #             if diff < min_diff:
        #                 min_diff = diff
        #                 x = i
        #     if min_diff < max_diff:
        #         class_list[x].append(img1)
        #     else:
        #         tmp_list = []
        #         tmp_list.append(img1)
        #         class_list.append(tmp_list)

        for img in img_list:
            min_diff = 100
            x = 0
            for i in range(len(class_list)):
                diff = get_diff(classify_model.model, img[1], class_list[i][0][1])
                if diff < min_diff:
                    min_diff = diff
                    x = i
            if min_diff < max_diff:
                class_list[x].append(img)
            else:
                tmp_list = []
                tmp_list.append(img)
                class_list.append(tmp_list)

        zip_path = os.getcwd() + '/static/media_out/' + prefix + '.zip'
        zip_file = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        for i in range(len(class_list)):
            dir_path = '/' + str(i) + '/'
            for img in class_list[i]:
                path = path_in + '/' + img[0]
                zip_file.write(path, dir_path+img[0])
        zip_file.close()
        t = threading.Thread(target=thread_del_dir, args=(path_in,))
        t.start()
        data = {'check': 0, 'message': prefix + '.zip'}
        return JsonResponse(data)

def neural_trans_page(request):
    if request.method == 'GET':
        return render(request, 'neural_trans.html')
    else:
        style_img = request.FILES.get('style_image')
        content_img = request.FILES.get('content_image')
        num_step = request.POST.get('num_step')
        print(num_step)
        num_step = int(num_step)
        print(num_step)
        prefix = str(datetime.datetime.now())
        prefix = prefix[:4] + prefix[5:7] + prefix[8:10] + prefix[11:13] + prefix[14:16] + prefix[17:19]
        style_img_name = prefix + '_' + style_img.name
        content_img_name = prefix + '_' + content_img.name
        path_in = os.getcwd() + '/static/media_in/'
        path_out = os.getcwd() + '/static/media_out/'
        neural_trans_model.load_model()
        with open(path_in+style_img_name, 'wb') as f:
            for _ in style_img.chunks():
                f.write(_)
        with open(path_in+content_img_name, 'wb') as f:
            for _ in content_img.chunks():
                f.write(_)
        style_img = image_loader(path_in+style_img_name)
        content_img = image_loader(path_in+content_img_name)
        num_step_list = [50, 150, 300]
        num_step = num_step_list[num_step]
        img = style_transfer(neural_trans_model.model, cnn_normalization_mean, cnn_normalization_std, content_img, style_img, num_steps=num_step)
        img = img_unloader(img)
        img.save(path_out+prefix+'.jpg')
        data = {'check': 0, 'message': prefix+'.jpg'}
        return JsonResponse(data)



def download(request, filename):
    file_path = os.getcwd() + '/static/media_out/' + filename
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return response

def delete(request, filename):
    file_path = os.getcwd() + '/static/media_out/' + filename
    if os.path.exists(file_path):
        os.remove(file_path)
    return render(request, 'mainPage.html')
