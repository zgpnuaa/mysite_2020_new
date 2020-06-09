//****************针对第一种方式的具体js实现部分******************//
//****************所使用的数据是city.js******************//



/*根据id获取对象*/
function $(str) {
    return document.getElementById(str);
}

//var addrShow = $('addr-show');
var btn = document.getElementsByClassName('met1')[0];
var prov = $('prov');
var city = $('city');
var country = $('country');



/*用于保存当前所选的省市区*/
var current = {
    prov: '',
    city: '',
    country: '',
};

/*自动加载省份列表*/
(function showProv() {
    btn.disabled = true;
    var len = provice.length;
    for (var i = 0; i < len; i++) {
        var provOpt = document.createElement('option');
        provOpt.innerText = provice[i]['name'];
        provOpt.value = i;
        prov.appendChild(provOpt);
    }
})();

/*根据所选的省份来显示城市列表*/
function showCity(obj) {
    var val = obj.options[obj.selectedIndex].value;
    if (val != current.prov) {
        current.prov = val;
       // addrShow.value = '';
        btn.disabled = true;
    }
    //console.log(val);
    if (val != null) {
        city.length = 1;
        var cityLen = provice[val]["districts"].length;
        for (var j = 0; j < cityLen; j++) {
            var cityOpt = document.createElement('option');
            cityOpt.innerText = provice[val]["districts"][j].name;
            cityOpt.value = j;
            city.appendChild(cityOpt);
        }
    }
}

/*根据所选的城市来显示县区列表*/
function showCountry(obj) {
    var val = obj.options[obj.selectedIndex].value;
    current.city = val;
    if (val != null) {
        country.length = 1; //清空之前的内容只留第一个默认选项

        var countryLen = provice[current.prov]["districts"][val].districts.length;

        if(countryLen == 0){
           // addrShow.value = provice[current.prov].name + '-' + provice[current.prov]["districts"][current.city].name;
            return;
        }
        for (var n = 0; n < countryLen; n++) {
            var countryOpt = document.createElement('option');
            countryOpt.innerText = provice[current.prov]["districts"][val].districts[n].name;
            countryOpt.value = n;
            country.appendChild(countryOpt);
        }
    }
}

/*选择县区之后的处理函数*/
function selecCountry(obj) {
    current.country = obj.options[obj.selectedIndex].value;
    var year = $('#year');
var month = $('#month');
var day=$('#day');
var hour =$('#hour');
var minute = $('#minute');

    if ((current.city != null) && (current.country != null) && (year.val() != -1) && (month.val() != -1) && (day.val() != -1) && (hour.val() != -1) && (minute.val() != -1)) {
        btn.disabled = false;
    }
}

/*选择县区之后的处理函数*/
function selectime() {

    var year = $('#year');
var month = $('#month');
var day=$('#day');
var hour =$('#hour');
var minute = $('#minute');

    if ((current.city != null) && (current.country != null) && (year.val() != -1) && (month.val() != -1) && (day.val() != -1) && (hour.val() != -1) && (minute.val() != -1)) {
        btn.disabled = false;
    }
}

///*点击确定按钮显示用户所选的地址*/
//function showAddr() {
////    addrShow.value = provice[current.prov].name + '-' + provice[current.prov]["districts"][current.city].name + '-' + provice[current.prov]["districts"][current.city].districts[current.country].name +" "+ provice[current.prov]["districts"][current.city].districts[current.country].center["longitude"]+" "+provice[current.prov]["districts"][current.city].districts[current.country].center["latitude"] ;
////
//    addrShow.value = provice[current.prov]["districts"][current.city].districts[current.country].center["longitude"]+" "+provice[current.prov]["districts"][current.city].districts[current.country].center["latitude"] ;
//
//}