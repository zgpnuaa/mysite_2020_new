let currentRecipient = '';
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');


function updateUserList() {
    $.getJSON('api/v1/user/', function (data) {
        userList.children('.user').remove();
        for (let i = 0; i < data.length; i++) {


            if(`${data[i]['username']}`==recipient_now)
                {
                const userItem = `<a class="list-group-item user active" id=${data[i]['username']}>${data[i]['username']}</a>`;
                 userList.children('.active').removeClass('active');
                 console.log('666');
                 console.log( $(userItem));
                  $(userItem).addClass('active');
                  $(userItem).appendTo('#user-list');
                  console.log($(userItem).attr('class'));
                  $('.panel-title').html($(userItem).text());
                  setCurrentRecipient($(userItem).text);
                  console.log($(userItem).text);
                 }
                 else
                 {const userItem = `<a class="list-group-item user" id=${data[i]['username']}>${data[i]['username']}</a>`;
                 $(userItem).appendTo('#user-list');}

        }

        userList.children('.active').removeClass('active');
        $(`a#${recipient_now}`).addClass('active');
        console.log('888');
        console.log( $(`a#${recipient_now}`));
        $('.panel-title').html( $(`a#${recipient_now}`).text());
        setCurrentRecipient( $(`a#${recipient_now}`).text());

        $('.user').click(function () {
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');

            $('.panel-title').html($(selected).text());
            setCurrentRecipient(selected.text);
        });
    });

    $.getJSON('api/v1/userinfo/', function (data) {
        // console.log(data);
        for (let i = 0; i < data.length; i++) {
//            const userItem = `<img src=${data[i]['photo']} class="userinfo"></img>`;
//            $(userItem).appendTo('#user');
            const  userItem = '<img src=# class="userinfo"></img>'
            console.log('lllll');
            console.log(data[i]);
            console.log( $(`a#${data[i]['username']}`));
            $(`a#${data[i]['username']}`).before(userItem);
        }

    });
}

//function updateUserInfoList() {
//    $.getJSON('api/v1/userinfo/', function (data) {
//         console.log(data);
//        for (let i = 0; i < data.length; i++) {
////            const userItem = `<img src=${data[i]['photo']} class="userinfo"></img>`;
////            $(userItem).appendTo('#user');
//            const  userItem = '<img src=# class="userinfo"></img>'
//            $(`a#${data[i]['username']}`).before(userItem);
//        }
//
//    });
//}

function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.timestamp);

    if (message.user === currentUser) position = 'right';
    const messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.user}</div>
                    <div class="text_wrapper">
                        <div class="text">${message.body}<br>
                            <span class="small">${formatMsgTime(date.getTime())}</span>
                    </div>
                </div>
            </li>`;
    $(messageItem).appendTo('#messages');
}

function getConversation(recipient) {
    $.getJSON(`api/v1/message/?target=${recipient}`, function (data) {
        messageList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});

    });

}

function getMessageById(message) {
    id = JSON.parse(message).message
    $.getJSON(`api/v1/message/${id}/`, function (data) {
        if (data.user === currentRecipient ||
            (data.recipient === currentRecipient && data.user == currentUser)) {
            drawMessage(data);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});

    });
}

function sendMessage(recipient, body) {
    $.post('api/v1/message/', {
        recipient: recipient,
        body: body
    }).fail(function () {
        alert('Error! Check console!');
    });
}

function setCurrentRecipient(username) {
    currentRecipient = username;
    getConversation(currentRecipient);
    enableInput();
}


function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

function disableInput() {
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
}




function formatMsgTime(timespan) {

  var dateTime = new Date(timespan);

  var year = dateTime.getFullYear();
  var month = dateTime.getMonth() + 1;
  var day = dateTime.getDate();
  var hour = dateTime.getHours();
  var minute = dateTime.getMinutes();
  var second = dateTime.getSeconds();

  var now = new Date();
  var now_new = now.getTime();  //typescript转换写法

  var milliseconds = 0;
  var timeSpanStr;

  milliseconds = now_new - timespan;


 if (milliseconds <= 1000 * 60 * 1) {
    timeSpanStr = '刚刚';
  }
  else if (1000 * 60 * 1 < milliseconds && milliseconds <= 1000 * 60 * 60) {
    timeSpanStr = Math.round((milliseconds / (1000 * 60))) + '分钟前';
  }
  else if (1000 * 60 * 60 * 1 < milliseconds && milliseconds <= 1000 * 60 * 60 * 24) {
    timeSpanStr = Math.round(milliseconds / (1000 * 60 * 60)) + '小时前';
  }
  else if (1000 * 60 * 60 * 24 < milliseconds && milliseconds <= 1000 * 60 * 60 * 24 * 15) {
    timeSpanStr = Math.round(milliseconds / (1000 * 60 * 60 * 24)) + '天前';
  }
  else if (milliseconds > 1000 * 60 * 60 * 24 * 15 && year == now.getFullYear()) {
    timeSpanStr = month + '-' + day + ' ' + hour + ':' + minute;
  } else {
    timeSpanStr = year + '-' + month + '-' + day + ' ' + hour + ':' + minute;
  }
  return timeSpanStr;
}

$(document).ready(function () {
    updateUserList();
//    updateUserInfoList();
    disableInput();

//    let socket = new WebSocket(`ws://127.0.0.1:8000/?session_key=${sessionKey}`);
    var socket = new WebSocket(
        'ws://' + window.location.host +
        '/ws?session_key=${sessionKey}')

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0) {
            sendMessage(currentRecipient, chatInput.val());
            chatInput.val('');
        }
    });

    socket.onmessage = function (e) {
        getMessageById(e.data);
    };
});



