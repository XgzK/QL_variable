var socket = io("ws://" + document.domain + ":" + location.port);
console.log('ws连接状态：' + socket.readyState);
socket.on("my_response", function (msg) {
    console.log(msg)
    // $("#log").append("<p>" + msg.data + "</p>");  // 收消息
    var aa = ""
    if(msg.data.indexOf("[info]") !== -1){
        aa =  "<p><span style=\"color: rgba(138,43,226,0.68); \">"+ msg.data +"</span></p>"
    }else if (msg.data.indexOf("[warning]") !== -1){
        aa =  "<p><span style=\"color: rgba(255,204,0,0.89); \">"+ msg.data +"</span></p>"
    }else if (msg.data.indexOf("[debug]") !== -1){
        aa =  "<p><span style=\"color: rgba(0,255,255,0.73); \">"+ msg.data +"</span></p>"
    }else if (msg.data.indexOf("[error]") !== -1){
        aa =  "<p><span style=\"color: rgba(255,0,0,0.75); \">"+ msg.data +"</span></p>"
    }
    $("#log").append(aa)
});
