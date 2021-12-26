var download_path = "";
var n = 0;
var btn_x = 1;

function upload() {
    if(n==0) {
        var style_image = document.getElementById("style_image");
        style_image.click();
        style_image.onchange = function () {
            var check = fileChange(this);
            if(check) {
                n = 1;
                var btn = document.getElementById("upload_btn");
                btn.style.backgroundColor = "transparent";
                btn.innerText = "upload content image";
            }
        }
    }
    else if(n==1) {
        var content_image = document.getElementById("content_image");
        content_image.click();
        content_image.onchange = function () {
            var check = fileChange(this);
            if (check) {
                var form = new FormData();
                form.append("style_image", $("#style_image")[0].files[0]);
                form.append("content_image", $("#content_image")[0].files[0]);
                form.append("num_step", btn_x);
                console.log("send");
                n = 2;
                var btn = document.getElementById("upload_btn");
                btn.style.backgroundColor = "#c6524e";
                btn.innerHTML = "loading...";
                $.ajax({
                    url: "/media_separator/neural_trans/",
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
                            n = 3;
                        }
                        else {
                            alert(resepnse["message"]);
                            btn.style.backgroundColor = "transparent";
                            btn.innerText = "upload style image";
                            n = 0;
                        }
                    }
                })
            }
        }
    }
	else if(n==2) {
	    alert("loading...");
    }
	else {
        // window.location.href = "/media_separator/download/" + download_path;
        window.open("/media_separator/download/" + download_path);
    }
}

function fileChange(target, id) {
        var fileSize = 0;
        var filetypes = [".jpg"];
        var filepath = target.value;
        var filemaxsize = 1024*2;//50M
        if(filepath){
            var isnext = false;
            var fileend = filepath.substring(filepath.lastIndexOf("."));
            if(filetypes && filetypes.length>0){
                for(var i =0; i<filetypes.length;i++){
                    if(filetypes[i]==fileend){
                        isnext = true;
                        break;
                    }
                }
            }
            if(!isnext){
                alert("图片格式限制为.jpg");
                target.value ="";
                return false;
            }
        }else{
            return false;
        }
        if (!target.files) {
            var filePath = target.value;
            var fileSystem = new ActiveXObject("Scripting.FileSystemObject");
            if(!fileSystem.FileExists(filePath)){
                alert("图片不存在");
                return false;
            }
            var file = fileSystem.GetFile (filePath);
            fileSize = file.Size;
        } else {
            fileSize = target.files[0].size;
        }

        var size = fileSize / 1024;
        if(size>filemaxsize){
            alert("图片大小限制为"+filemaxsize/1024+"M！");
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

function btn_click1() {
    btn_x = 0;
    var btn1 = document.getElementById("btn_low");
    var btn2 = document.getElementById("btn_middle");
    var btn3 = document.getElementById("btn_high");
    btn1.style.backgroundColor = "#57cbcc";
    btn2.style.backgroundColor = "transparent";
    btn3.style.backgroundColor = "transparent";
}

function btn_click2() {
    btn_x = 1;
    var btn1 = document.getElementById("btn_low");
    var btn2 = document.getElementById("btn_middle");
    var btn3 = document.getElementById("btn_high");
    btn1.style.backgroundColor = "transparent";
    btn2.style.backgroundColor = "#57cbcc";
    btn3.style.backgroundColor = "transparent";
}

function btn_click3() {
    btn_x = 2;
    var btn1 = document.getElementById("btn_low");
    var btn2 = document.getElementById("btn_middle");
    var btn3 = document.getElementById("btn_high");
    btn1.style.backgroundColor = "transparent";
    btn2.style.backgroundColor = "transparent";
    btn3.style.backgroundColor = "#57cbcc";
}