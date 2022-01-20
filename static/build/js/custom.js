function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg);  //匹配目标参数
    if (r != null) return unescape(r[2]); return null; //返回参数值
}
//modify by xubin 00293437,add filter cookies
function SetListUrlParamToCookie() {
      var vars = [], hash;
      var totalurl =  window.location.href.slice(window.location.href.indexOf('?') + 1)
      var hashes =totalurl.split('&');
      var path =GetUrlRelativePath();
      var d = new Date();
      d.setTime(d.getTime() + (30*24*60*60*1000));
      var expires = "expires="+ d.toUTCString();
      for (var i = 0; i < hashes.length; i++) {
            hash = hashes[i].split('=');
            document.cookie = hash[0] + "=" + hash[1] + ";" + expires + ";path="+path;
        }
}

function GetUrlRelativePath()
　　{
　　　　var url = document.location.toString();
　　　　var arrUrl = url.split("//");

　　　　var start = arrUrl[1].indexOf("/");
　　　　var relUrl = arrUrl[1].substring(start);//stop省略，截取从start开始到结尾的所有字符

　　　　if(relUrl.indexOf("?") != -1){
　　　　　　relUrl = relUrl.split("?")[0];
　　　　}
　　　　return relUrl;
　　}
//===========

//modify by xubin 00293437,easyit import data
function initTemplateImport(apps){
    e = $('#excelFile');
    var files = e.prop('files');
    var fileReader = new FileReader();
    fileReader.onload = function(ev) {
        try {
            var data = ev.target.result,
                workbook = XLSX.read(data, {
                    type: 'binary'
                }), // 以二进制流方式读取得到整份excel表格对象
                xlsdata = []; // 存储获取到的数据
        } catch (e) {
            console.log('文件类型不正确');
            return;
        }

        // 表格的表格范围，可用于判断表头是否数量是否正确
        var fromTo = '';
        // 遍历每张表读取
        for (var sheet in workbook.Sheets) {
            if (workbook.Sheets.hasOwnProperty(sheet)) {
                fromTo = workbook.Sheets[sheet]['!ref'];
                console.log(fromTo);
                xlsdata = xlsdata.concat(XLSX.utils.sheet_to_json(workbook.Sheets[sheet]));
                break; // 如果只取第一张表，就取消注释这行
            }
        }
        fin_data = []
        for ( index in xlsdata){
            item = {}
            for (key in xlsdata[index]){
                if (xlsdata[index][key]!='-')
                    item[key.split("--")[1]] =  xlsdata[index][key]
            }
            fin_data.push(item)
        }
        if (fin_data.length > 0){
            console.log(fin_data);
            $.ajax({
              type: "POST",
              url: '/'+apps+"manager/create",
              data: JSON.stringify(fin_data),
               success: function(msg){
                  window.location.href='/'+apps+'manager/'+apps+'list.html';
               },
               error: function(msg){
                    alert('添加失败！')
                 }
             });
        }
    };
    // 以二进制方式打开文件
    fileReader.readAsBinaryString(files[0]);
}


$(document).ready(function() {

    init_sparklines();
    init_flot_chart();
    init_sidebar();
    init_wysiwyg();
    init_InputMask();
    init_JQVmap();
    init_cropper();
    init_knob();
    init_IonRangeSlider();
    init_ColorPicker();
    init_TagsInput();
    init_parsley();
    init_daterangepicker();
    init_daterangepicker_right();
    init_daterangepicker_single_call();
    init_daterangepicker_reservation();
    init_SmartWizard();
    init_EasyPieChart();
    init_charts();
    init_echarts();
    init_morris_charts();
    init_skycons();
//    init_select2();
    init_validator();
    init_DataTables();
    init_chart_doughnut();
    init_gauge();
    init_PNotify();
    init_starrr();
    init_calendar();
    init_compose();
    init_CustomNotification();
    init_autosize();
    init_autocomplete();

});
