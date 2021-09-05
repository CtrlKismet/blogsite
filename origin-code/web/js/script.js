var fade = ['scale(0,0)', 'scale(1,1)'];
//var fade = ['Rotate3d(1,0,0,90deg)', 'Rotate3d(1,0,0,0deg)'];

var cnt = [0, 0, 0, 0, 0, 0],
    number = [-1, -1, -1, -1, -1, -1];

function refreshTime() {
    var timeNow = new Date().toTimeString().substring(0, 8).replace(':', '').replace(':', '');
    var els = document.getElementsByClassName('timeNum');
    for (var i = 0; i < els.length; i++) {
        if (timeNow[i] === number[i]) continue;
        var el = els[i];
        cnt[i] = (cnt[i] + 1) % 2;
        if (cnt[i] !== 0) {
            el.innerText = timeNow[i];
            number[i] = timeNow[i];
            el.style.transitionDelay = '0s';
        } else el.style.transitionDelay = '0.2s';
        el.style.transform = fade[cnt[i]];
    }
};


let chznday = ['日', '一', '二', '三', '四', '五', '六'];
var refresh_time_interval;

function get_time() {
    refresh_time_interval = setInterval(refreshTime, 500);
    var temp_time_for_date = new Date();
    $('#YYMMDD')[0].innerHTML = temp_time_for_date.getFullYear() + '/' +
        (temp_time_for_date.getMonth() + 1) + '/' +
        temp_time_for_date.getDate() + '     ' +
        '星期' + chznday[temp_time_for_date.getDay()];
}

var preTitle;

document.addEventListener('visibilitychange', function () {
    var isHidden = document.hidden;
    if (isHidden) {
        preTitle = document.title;
        document.title = "这里是CtrlKismet的博客";
        clearInterval(refresh_time_interval);
        document.getElementById('web_icon').href = "/images/faviconOUT.ico";
    } else {
        document.title = preTitle;
        refresh_time_interval = setInterval(refreshTime, 500);
        document.getElementById('web_icon').href = "/images/faviconIN.ico";
    }
});

var topValue = 80,
    scrollValue = 260;

document.addEventListener('scroll', function () {
    if (window.scrollY > topValue) {
        $('.head-bar').css('top', '-2.5em');
    } else {
        $('.head-bar').css('top', '0');
    }
    if (window.innerWidth <= 900) return;
    if (window.scrollY > scrollValue) {
        $('div[id^=list_of_]').css('margin-top', window.scrollY - scrollValue + 60 + 'px');
        $('aside .topRocket').css('opacity', '1');
    } else {
        $('div[id^=list_of_]').css('margin-top', '40px');
        $('aside .topRocket').css('opacity', '0');
    }
});

function UpToTop() {
    $('body,html').scrollTop(0);
}

function loadEl() {
    $('.loading-page').css('opacity', '0');
    $('.loading-page').css('z-index', '-1');
    $('.head-bar').css('top', '0');
    $('.head-bar div').css('opacity', '1');
    $('.content').css('opacity', '1');
    $('.content').css('margin-top', '4.2em');
    $('.footer').css('opacity', '1');
    get_time();
}

$(document).ready(function () {});

let rootsrc = "https://ctrlkismet.top/";
// let rootsrc = "http://localhost:50542/";

function listen_login(authent) {
    if (authent === 'True') return;
    var keyCode = event.keyCode;
    var altKey = event.altKey;
    if (altKey && keyCode === 76) {
        window.location.href = rootsrc + "authorization/login";
    }
}


// docker run -v /home/web/imgblogres:/home/img  --name blog -p 5000:80 -d blog