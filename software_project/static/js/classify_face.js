var download_path = "";
var n = 0;

function upload() {
    if(n==0) {
	    var form = document.getElementById("upload_form");
        var video = document.getElementById("img_dir");
        video.click();
        video.onchange = function () {
            var check = fileChange(this);
            if(check) {
                var form = new FormData();
                for(var i=0;i<$("#img_dir")[0].files.length;i++) {
                    form.append("img_dir", $("#img_dir")[0].files[i]);
                }
                form.append("threshold", $("#classify_face_range")[0].value);
                console.log("send");
                console.log($("#classify_face_range")[0].value);
                n = 1;
                var btn = document.getElementById("upload_btn");
                btn.style.backgroundColor = "#c6524e";
                btn.innerHTML = "loading...";
                $.ajax({
                    url: "/media_separator/classify_face/",
                    type: "POST",
                    headers: {"X-CSRFToken": $.cookie('csrftoken')},
                    data: form,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        console.log(response);
                        if(response["check"]==0) {
                            download_path = response["message"];
                            btn.style.backgroundColor = "#6bc642";
                            btn.innerHTML = "download";
                            n = 2;
                        }
                        else {
                            alert(resepnse["message"]);
                            btn.style.backgroundColor = "transparent";
                            btn.innerText = "upload";
                            n = 0;
                        }
                    }
                })
            }
        }
    }
	else if(n==1) {
	    alert("loading...");
    }
	else {
        // window.location.href = "/media_separator/download/" + download_path;
        window.open("/media_separator/download/" + download_path);
    }
}

function fileChange(target, id) {
        var fileSize = 0;
        var filepath = target.value;
        var filemaxsize = 1024*50;//50M
        if(!filepath) {
            return false;
        }
        if (!target.files) {
            var filePath = target.value;
            var fileSystem = new ActiveXObject("Scripting.FileSystemObject");
            if(!fileSystem.FileExists(filePath)){
                alert("文件夹不存在");
                return false;
            }
            var file = fileSystem.GetFile (filePath);
            fileSize = file.Size;
        } else {
            for(var i=0;i<target.files.length;i++) {
                fileSize += target.files[i].size;
            }
        }
        var size = fileSize / 1024;
        if(size>filemaxsize){
            alert("文件夹大小限制为"+filemaxsize/1024+"M！");
            target.value ="";
            return false;
        }
        if(size<=0){
            alert("附件大小不能为0M！");
            target.value ="";
            return false;
        }
        return true;
}

window.onbeforeunload = function () {
    $.ajax({
        url: "/media_separator/delete/" + download_path,
        type: "GET"
    })
};

function range_change() {
    var x = document.getElementById("classify_face_range").value;
    var value = document.getElementById("range_value");
    value.innerText = "threshold: " + x;
}