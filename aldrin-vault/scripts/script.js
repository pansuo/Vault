(function() {
function $id(id) {
    return document.getElementById(id);
}

function Output(msg) {
    var m = $id("messages");
    m.innerHTML = msg + m.innerHTML;
}

if (window.File && window.FileList && window.FileReader) {
    Init();
}

function Init() {
    var fileselect = $id("fileselect"),  
        filedrag = $id("filedrag"), 
        submitbutton = $id("submit_button");

    fileselect.addEventListener("change", FileSelectHandler, false);
    var xhr = new XMLHttpRequest()
    if(xhr.upload) {

        filedrag.addEventListener("dragover", FileDragHover, false);
        filedrag.addEventListener("dragleave", FileDragHover, false);
        filedrag.addEventListener("drop", FileSelectHandler, false);
        filedrag.style.display = "block";
        fileselect.style.display = "none";
        //submitbutton.style.display = "";
    }
}

function FileDragHover(e) {
    e.stopPropagation();
    e.preventDefault();
    e.target.className = (e.type == "dragover" ? "hover" : "")
}

function FileSelectHandler(e) {
    FileDragHover(e);
    var files = e.target.files || e.dataTransfer.files;
    for (var i = 0, f; f = files[i]; i++) {
        ParseFile(f);
        UploadFile(f);
    }
}

function ParseFile(file) {
    Output(
           "<p>File info: " + file.name + 
               "type: " + file.type +
               "size: " + file.size +
           "</p>");
}

function UploadFile(file) {
    var xhr = new XMLHttpRequest();
    if(xhr.upload) {
        xhr.open("POST", $id("upload").action, true);
        xhr.setRequestHeader("Content-Type", file.type);
        xhr.send(file);
    }
}

})();
