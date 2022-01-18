# -*-coding:utf-8-*-
# @Time    : 2018/8/2 20:43
# @Author  : x00293437
import yaml
import os
import shutil
import re
import sys
import logging
import collections
import xlwt
if sys.version_info[0] > 2:
    # py3k
    pass
else:
    # py2
    import codecs
    import warnings
    def open(file, mode='r', buffering=-1, encoding=None,
             errors=None, newline=None, closefd=True, opener=None):
        if newline is not None:
            warnings.warn('newline is not supported in py2')
        if not closefd:
            warnings.warn('closefd is not supported in py2')
        if opener is not None:
            warnings.warn('opener is not supported in py2')
        return codecs.open(filename=file, mode=mode)
					
#用字典保存日志级别

format_dict = {
   1 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
}

class Logger():
    def __init__(self, logname, loglevel, logger):

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logname)
        fh.setLevel(logging.DEBUG)

        #再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        # ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger

logger = Logger(logname='log.txt', loglevel=1, logger="Log").getlog()


global config,target
config = {}
target = {}


def create_sidebar_file():
    logger.info("start create_sidebar_file")
    SIDEBAR_FILE = os.path.sep.join(os.path.split(os.path.realpath(__file__))[0].split(os.path.sep)[:-1]) + "\\templates\\common\\sidebar.html"
    menu_esxit = False
    with open(SIDEBAR_FILE,'r',encoding='utf-8') as fin_in:
        with open(target['common']+'\\sidebar.html','w',encoding='utf-8') as fin_out:
            lines = fin_in.readlines()
            for line in lines:
                # line = bytes.decode(line)
                if "/%smanager/" %config['english_name'] in line:
                    logger.info("menu esxited ... ")
                    menu_esxit = True
                if "EasyIT menu position" in line and not menu_esxit:
                    menu_li = [x for x in config['menu'].strip(';').split(";")]
                    if len(menu_li) == 1:
                        fin_out.write('            <li app="%s"><a href="/%smanager/%slist.html"><i class="fa fa-dot-circle-o" style="color:#4CAF50"></i> %s</a></li>'%(config['english_name'],config['english_name'],config['english_name'],menu_li[0]))
                    elif len(menu_li) == 2:
                        tmpl = '''            <li app="%s"><a><i class="fa fa-dot-circle-o" style="color:#03a9f4"></i> %s <span class="fa fa-chevron-down" ></span></a>
                <ul class="nav child_menu">
                    <li><a href="/%smanager/%slist.html">%s</a></li>
                </ul>
                </li>\r\n'''
                        fin_out.write(tmpl%(config['english_name'],menu_li[0],config['english_name'],config['english_name'],menu_li[1]))
                    elif len(menu_li) == 3:
                        tmpl = '''   <li app="%s"><a><i class="fa fa-dot-circle-o" style="color:#03a9f4"></i> %s <span class="fa fa-chevron-down" ></span></a>
                    <ul class="nav child_menu">
                  <li><a>%s<span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li class="sub_menu"><a href="/%smanager/%slist.html">%s</a></li>
                     </ul>
                  </li>
                </ul></li>\r\n'''
                        fin_out.write(tmpl % (config['english_name'],menu_li[0],menu_li[1], config['english_name'],config['english_name'], menu_li[2]))
                fin_out.write(line)

def create_url_file():
    logger.info("start create_url_file")
    URL_FILE = os.path.sep.join(os.path.split(os.path.realpath(__file__))[0].split(os.path.sep)[:-1]) + "\\config\\urls.py"
    with open(URL_FILE,'r',encoding='utf-8') as fin_in:
        with open(target['config']+'\\urls.py','w',encoding='utf-8') as fin_out:
            for line in fin_in.readlines():
                if not "%smanager/"%config['english_name'] in line:
                    fin_out.write(line)
                if "admin.site.urls" in line:
                    fin_out.write("    url(r'^%smanager/', include('apps.%smanager.urls')),\n"%(config['english_name'],config['english_name']))

def create_apps_files():
    logger.info("start create_apps_files")
    tmpl_path = "demoapp\\apps\\demoapp"
    f_li = os.listdir(tmpl_path)
    for fname in f_li:
        fpath = os.path.join(tmpl_path,fname)
        with open(fpath,'r',encoding='utf-8') as fin_in:
            with open(os.path.join(target['apps'],fname),'w',encoding='utf-8') as fin_out:
                for line in fin_in.readlines():
                    reg = "{\$(.*?)\$}"
                    ma = re.findall(reg,line)
                    if len(ma) >0:
                        for item in ma:
                            line = line.replace('{$%s$}'%item,config[item])
                    fin_out.write(line)

def create_templates_form_file():
    logger.info("start create_templates_form_file")
    tmpl_path = "demoapp\\templates\\demoapp\\demoform.html"
    param_li = config['params']
    form_content = ""
    select_init = ""
    date_num = 0
    #富文本相关配置
    config['richtextjs'] = ""
    config['richtextdata'] = ""
    config['autocomplete_content'] = ""

    for pitem in param_li:
        for k in pitem:
            required_str = ""
            if 'required' in pitem[k] and pitem[k]['required']:
                required_str = 'required="required"'
            ele_type = pitem[k].get("type")
            if  ele_type == 'input':
                rule_str = ""
                if 'rule' in pitem[k] and pitem[k]['rule']:
                    rule_str = 'data-parsley-pattern="/%s/"' % pitem[k]['rule']
                ph_str = ""
                if 'info' in pitem[k] and pitem[k]['info']:
                    ph_str = 'placeholder="%s"' % pitem[k]['info']
                if pitem[k].get('autocomplete'):
                    config['autocomplete_content'] += '''$.ajax( {
         async: false,
         url: "/%smanager/reportdata?type=bar&param=%s",
         success: function( resp ) {
          data_li = resp.item ;
            $("[name='%s']").autocomplete({
                 source: Array.from(new Set(data_li.join(";").replace(/\s*;\s*/g,";").split(";"))),
               });
        }
    });\n''' % (config['english_name'], k, k)
                tmpl = '''                         <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12">%s</label>
                                <div class="col-md-6 col-sm-9 col-xs-12">
                                    <input name="%s" type="text" class="form-control" %s %s %s
                                           value="{{ old%s.%s }}">
                                </div>
                            </div>\n'''

                form_content += tmpl%( pitem[k]['desc'],k,required_str,rule_str,ph_str,config['english_name'],k)

            elif ele_type == 'textarea':
                tmpl = '''                         <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12">%s </label>
                                <div class="col-md-6 col-sm-9 col-xs-12">
                                    <textarea class="form-control" name="%s" rows="3" %s>{{ old%s.%s }}</textarea>
                                </div>
                            </div>\n'''
                form_content += tmpl % (pitem[k]['desc'], k, required_str, config['english_name'], k)
            elif ele_type == 'select':
                option_str = ""
                select_init += '''$("[name='%s']").val("{{ old%s.%s}}");\n''' % (k,config['english_name'],k)
                for op in pitem[k]['data']:
                    option_str += '                 <option >%s</option>\n' % op

                tmpl = '''                          <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12">%s</label>
                                <div class="col-md-6 col-sm-9 col-xs-12">
                                    <select name="%s" class="form-control" %s>
                                    %s
                                    </select>
                                </div>
                            </div>\n'''
                form_content += tmpl % (pitem[k]['desc'], k, required_str, option_str)
            elif ele_type == 'date':
                tmpl = '''                         <div class="form-group">
                             <div class="controls">
                                 <label class="control-label col-md-3 col-sm-3 col-xs-12">%s</label>
                                 <div class="col-md-6 xdisplay_inputx form-group has-feedback">
                                     <input name="%s" type="text" class="form-control has-feedback-left" id="single_cal%d" aria-describedby="inputSuccess2Status" value="{{ old%s.%s }}">
                                     <span class="fa fa-calendar-o form-control-feedback left" aria-hidden="true"></span>
                                     <span id="inputSuccess2Status" class="sr-only">(success)</span>
                                 </div>
                             </div>
                         </div>\n'''
                date_num += 1
                form_content += tmpl % (pitem[k]['desc'],k,date_num,config['english_name'],k)

            elif ele_type == 'richtext':
                config['richtextjs'] = '''
                <script id="contInsert">
                   {{ old%s.%s | safe }}
                </script>>
                <script >
                    $("#editor-one").append($("#contInsert").html());
                    $('#editor-one').on('paste', function (e) {
                        var items = e.originalEvent.clipboardData.items;
                        for (var i = 0; i < items.length; ++i) {
                            ele = this;
                            if (items[i].kind == 'file' &&
                                items[i].type.indexOf('image/') !== -1) {
                
                                var file = items[i].getAsFile();
                                if(file)    {
                                            var reader = new FileReader();
                                            reader.onload = function(evt)
                                            {
                                                var result = evt.target.result;
                                                var img = document.createElement('img');
                                                img.src = result;
                                                ele.appendChild(img);
                                             }
                                            reader.readAsDataURL(file);
                                         }
                            }
                
                        }
                    });
                </script>
                ''' %(config['english_name'],k)

                config['richtextdata'] = "postJson['%s'] = $('#editor-one').html();" % k

                richtextele =  '''
                             <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12">%s</label>
                                <div class="col-md-6 col-sm-8 col-xs-12">
                                <div class="x_panel">
                                  <div class="x_content">
                                    <div id="alerts"></div>
                                    <div class="btn-toolbar editor" data-role="editor-toolbar" data-target="#editor-one">
                                      <div class="btn-group">
                                        <a class="btn dropdown-toggle" data-toggle="dropdown" title="Font"><i class="fa fa-font"></i><b class="caret"></b></a>
                                        <ul class="dropdown-menu">
                                        </ul>
                                      </div>
                                      <div class="btn-group">
                                        <a class="btn dropdown-toggle" data-toggle="dropdown" title="Font Size"><i class="fa fa-text-height"></i>&nbsp;<b class="caret"></b></a>
                                        <ul class="dropdown-menu">
                                          <li>
                                            <a data-edit="fontSize 5">
                                              <p style="font-size:17px">Huge</p>
                                            </a>
                                          </li>
                                          <li>
                                            <a data-edit="fontSize 3">
                                              <p style="font-size:14px">Normal</p>
                                            </a>
                                          </li>
                                          <li>
                                            <a data-edit="fontSize 1">
                                              <p style="font-size:11px">Small</p>
                                            </a>
                                          </li>
                                        </ul>
                                      </div>

                                      <div class="btn-group">
                                        <a class="btn" data-edit="bold" title="Bold (Ctrl/Cmd+B)"><i class="fa fa-bold"></i></a>
                                        <a class="btn" data-edit="italic" title="Italic (Ctrl/Cmd+I)"><i class="fa fa-italic"></i></a>
                                        <a class="btn" data-edit="strikethrough" title="Strikethrough"><i class="fa fa-strikethrough"></i></a>
                                        <a class="btn" data-edit="underline" title="Underline (Ctrl/Cmd+U)"><i class="fa fa-underline"></i></a>
                                      </div>

                                      <div class="btn-group">
                                        <a class="btn" data-edit="insertunorderedlist" title="Bullet list"><i class="fa fa-list-ul"></i></a>
                                        <a class="btn" data-edit="insertorderedlist" title="Number list"><i class="fa fa-list-ol"></i></a>
                                        <a class="btn" data-edit="outdent" title="Reduce indent (Shift+Tab)"><i class="fa fa-dedent"></i></a>
                                        <a class="btn" data-edit="indent" title="Indent (Tab)"><i class="fa fa-indent"></i></a>
                                      </div>

                                      <div class="btn-group">
                                        <a class="btn" data-edit="justifyleft" title="Align Left (Ctrl/Cmd+L)"><i class="fa fa-align-left"></i></a>
                                        <a class="btn" data-edit="justifycenter" title="Center (Ctrl/Cmd+E)"><i class="fa fa-align-center"></i></a>
                                        <a class="btn" data-edit="justifyright" title="Align Right (Ctrl/Cmd+R)"><i class="fa fa-align-right"></i></a>
                                        <a class="btn" data-edit="justifyfull" title="Justify (Ctrl/Cmd+J)"><i class="fa fa-align-justify"></i></a>
                                      </div>

                                      <div class="btn-group">
                                        <a class="btn dropdown-toggle" data-toggle="dropdown" title="Hyperlink"><i class="fa fa-link"></i></a>
                                        <div class="dropdown-menu input-append">
                                          <input class="span2" placeholder="URL" type="text" data-edit="createLink" />
                                          <button class="btn" type="button">Add</button>
                                        </div>
                                        <a class="btn" data-edit="unlink" title="Remove Hyperlink"><i class="fa fa-cut"></i></a>
                                      </div>

                                      <div class="btn-group">
                                        <a class="btn" title="Insert picture (or just drag & drop)" id="pictureBtn"><i class="fa fa-picture-o"></i></a>
                                        <input type="file" data-role="magic-overlay" data-target="#pictureBtn" data-edit="insertImage" />
                                      </div>

                                      <div class="btn-group">
                                        <a class="btn" data-edit="undo" title="Undo (Ctrl/Cmd+Z)"><i class="fa fa-undo"></i></a>
                                        <a class="btn" data-edit="redo" title="Redo (Ctrl/Cmd+Y)"><i class="fa fa-repeat"></i></a>
                                      </div>
                                    </div>

                                    <div id="editor-one" class="editor-wrapper"></div>
                                  </div>
                                </div>
                              </div>
                            </div>
                ''' % pitem[k]['desc']

                form_content += richtextele

    with open(tmpl_path,'r',encoding='utf-8') as fin_in:
        with open(os.path.join(target['templates'],config['english_name']+"form.html"),'w',encoding='utf-8') as fin_out:
            for line in fin_in.readlines():
                reg = "{\$(.*?)\$}"
                # line = bytes.decode(line)
                ma = re.findall(reg, line)
                if len(ma) > 0:
                    for item in ma:
                        if item == "form_content":
                            line = form_content
                        elif item == "select_init":
                            line = select_init
                        else:
                            line = line.replace('{$%s$}' % item, config[item])
                fin_out.write(line)

def create_templates_list_file():
    logger.info("start create_templates_list_file")
    tmpl_path = "demoapp\\templates\\demoapp\\demolist.html"
    param_li = config['params']
    cloumns_content = "{checkbox: true},"
    select = ""
    for pitem in param_li:
        for k in pitem:
            tmplselect = '''
                                <option value="%s">%s</option>
                                 \n'''
            select += tmplselect % (k, pitem[k]['desc'])
            tmpl = '''
                    {
                        title: '%s',
                        field: '%s',
                        align: 'center',
                        sortable: true,
                        visible:true,
                        %s
                        %s
                    },\n'''
            ele_type = pitem[k].get("type")
            if ele_type == 'select':
                filter_str = '''filter: {
                          type: "select",
                          data: [%s]
                        }''' %  ",".join(['"'+x+'"' for x in pitem[k]['data']])
            else:
                filter_str = '''filter: {
                                  type: "input",
                                }'''
            option_str = ""
            if 'width' in pitem[k] and pitem[k]['width']:
                option_str = 'width : "%s" ,' % pitem[k]['width']

            if ele_type == 'richtext':
                option_str += 'formatter : richtextFormatter ,\n                        events:richcontentEvents,'

            cloumns_content += tmpl % (pitem[k]['desc'], k, option_str,filter_str)

    with open(tmpl_path,'r',encoding='utf-8') as fin_in:
        with open(os.path.join(target['templates'],config['english_name']+"list.html"),'w',encoding='utf-8') as fin_out:
            for line in fin_in.readlines():
                reg = "{\$(.*?)\$}"
                # line = bytes.decode(line)
                ma = re.findall(reg, line)
                if len(ma) > 0:
                    for item in ma:
                        if item == "cloumns_content":
                            line = cloumns_content
                        elif item == "select":
                            line = select
                        else:
                            line = line.replace('{$%s$}' % item, config[item])
                fin_out.write(line)

def create_templates_report_file():
    logger.info("start create_templates_report_file")
    tmpl_path = "demoapp\\templates\\demoapp\\demoreport.html"
    param_li = config.get('charts',[])
    config['summary_content'] = ""
    config['report_content'] = ""
    config['request_content'] = ""
    summary_tmpl = '''    <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count">
             <span class="count_top"><i class="fa fa-calculator"></i> %s </span>
             <div id="%s"  class="count purple"></div>
           </div>'''
    report_tmpl = '''
          <div class="col-md-6 col-sm-6 col-xs-12">
        <div class="x_panel">
          <div class="x_title">
            <h2>%s统计</h2>
            <div class="clearfix"></div>
          </div>
          <div class="x_content">
          <div id="%s" style="height:350px;"></div>
          </div>
        </div>
      </div>
    '''

    count_request_tmpl = '''
      $.ajax(
        {
                url: '/%smanager/reportdata?type=count&param=%s&rule=%s',
                success: function(resp){
                    $('#%s').text(resp.data);
                }
        });
    '''

    chart_request_tmpl = '''
          $.ajax(
        {
                url: '/%smanager/reportdata?type=%s&param=%s%s',
                success: function(resp){
                  %s("%s",resp.item,resp.value)
                }
        });
    '''
    for pitem in param_li:
        for k in pitem:
            ele_type = pitem[k].get("type")
            if ele_type == 'count':
                config['summary_content'] += summary_tmpl %(pitem[k].get('desc'),k)
                config['request_content'] += count_request_tmpl %(config['english_name'],pitem[k].get("param"),pitem[k].get("rule",".*"),k)
            else:
                rulestr = ""
                chart_rule = pitem[k].get("rule")
                if chart_rule:
                    rulestr = "&rule="+chart_rule
                config['report_content'] += report_tmpl %(pitem[k].get('desc'),k)
                if pitem[k].get("type") == 'bar':
                    func_name = "easyit_init_barchart"
                elif  pitem[k].get("type") == 'pie':
                    func_name = "easyit_init_piechart"
                config['request_content'] += chart_request_tmpl %(config['english_name'],pitem[k].get("type"),pitem[k].get("param"),rulestr,func_name,k)

    with open(tmpl_path, 'r',encoding='utf-8') as fin_in:
        with open(os.path.join(target['templates'], config['english_name'] + "report.html"), 'w',encoding='utf-8') as fin_out:
            for line in fin_in.readlines():
                reg = "{\$(.*?)\$}"
                # line = bytes.decode(line)
                ma = re.findall(reg, line)
                if len(ma) > 0:
                    for item in ma:
                        line = line.replace('{$%s$}' % item, config[item])
                fin_out.write(line)

def parse_yaml(f):
    global config
    config = {}
    logger.info("start parse yaml config file : "+f)
    with open(f, 'r',encoding='utf-8') as f_in:
        config = yaml.load(f_in)
        if config['english_name'][0].isupper:
            config['english_name'] = config['english_name'][0].lower()+config['english_name'][1:]
        config['upper_english_name'] = config['english_name'][0].upper() + config['english_name'][1:]
        if sys.version_info[0] == 2:
            config = convert(config)
        logger.info("config result : " + str(config))

def convert(data):
    if isinstance(data, basestring):
        return str(data.encode('utf-8'))
    elif isinstance(data, collections.Mapping):
        return dict(list(map(convert, iter(data.items()))))
    elif isinstance(data, collections.Iterable):
        return type(data)(list(map(convert, data)))
    else:
        return data

def create_app_folders():
    logger.info("start create_app_folders")
    global target
    app_name = config['english_name']+'manager'
    target['app_name'] = app_name
    if os.path.exists(app_name):
        shutil.rmtree(os.path.split(os.path.realpath(__file__))[0]+os.path.sep+app_name)
    os.mkdir(app_name)
    os.mkdir(app_name+"\\apps")
    os.mkdir(app_name+ "\\templates")
    target['apps'] = app_name + "\\apps\\"+app_name
    os.mkdir(target['apps'])
    target['templates'] = app_name + "\\templates\\" + app_name
    os.mkdir(target['templates'])
    target['config'] =app_name + "\\config"
    os.mkdir(target['config'] )
    target['common'] =app_name + "\\templates\\common"
    os.mkdir(target['common'])


def create_import_template():
    logger.info("start create_import_template")
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Worksheet')
    param_li = config['params']
    index = 0
    for pitem in param_li:
        for k in pitem:
            worksheet.write(0, index, label=(pitem[k]['desc']+"--"+k))
            index += 1
    # 保存
    fd_path = os.path.join(target['apps'],'file')
    os.mkdir(fd_path)
    workbook.save(os.path.join(fd_path,'template.xls'))


def create(is_batch_mode=False,deploy_flag=False):
    logger.info("==================== start create new app  ====================")
    if is_batch_mode:
        files =[f for f in os.listdir("./") if f.endswith('.yaml')]
    else:
        files = ['config.yaml']
    for f in files:
        parse_yaml(f)
        create_app_folders()
        create_url_file()
        create_sidebar_file()
        create_apps_files()
        create_templates_form_file()
        create_templates_list_file()
        create_templates_report_file()
        create_import_template()
        if deploy_flag:
            deploy()


def deploy():
    logger.info("start deploy new app %s to project" % config['english_name'])
    src_dir = os.path.split(os.path.realpath(__file__))[0]+os.path.sep+config['english_name']+'manager'
    dst_dir =  os.path.sep.join(os.path.split(os.path.realpath(__file__))[0].split(os.path.sep)[:-1])
    # shutil.copytree(src_dir, dst_dir,False)
    cmd = "xcopy %s %s  /E/I/D/Y" % (src_dir,dst_dir)
    logger.info("copy cmd : " + cmd)
    fp = os.popen(cmd)
    logger.info(fp.read())#.decode('gbk').encode("utf-8"))
    logger.info("deploy app successfully !")


def uninstall(is_batch_mode = False):
    logger.info("start uninstall app from project")
    if is_batch_mode:
        files =[f for f in os.listdir("./") if f.endswith('.yaml')]
    else:
        files = ['config.yaml']
    for f in files:
        parse_yaml(f)
        delete_url()
        delete_menu()
        delete_source_and_templates()

def delete_url():
    logger.info("delete %s url..." % config['english_name'])
    URL_FILE = os.path.sep.join(os.path.split(os.path.realpath(__file__))[0].split(os.path.sep)[:-1]) + "\\config\\urls.py"
    data =[]
    with open(URL_FILE, 'r+',encoding='utf-8') as f:
        for line in f.readlines():
            if not "%smanager/" % config['english_name'] in line:
                data.append(line)
    with open(URL_FILE, 'w',encoding='utf-8') as f:
        f.writelines(data)

def delete_menu():
    logger.info("delete %s menu..." % config['english_name'])
    SIDEBAR_FILE = os.path.sep.join(
        os.path.split(os.path.realpath(__file__))[0].split(os.path.sep)[:-1]) + "\\templates\\common\\sidebar.html"
    with open(SIDEBAR_FILE, 'r+',encoding='utf-8') as f:
        source = f.read()
    menu_li = config['menu'].strip(';').split(";")
    reg = r'<li\s+app="%s"((?!</li>)[\s\S]+?</li>){%s}' %(config['english_name'],str(len(menu_li)))
    source = re.sub(reg,"",source)
    with open(SIDEBAR_FILE, 'w',encoding='utf-8') as f:
        f.write(source)

def delete_source_and_templates():
    logger.info("delete %s source_and_templates..." % config['english_name'])
    dst_dir = os.path.sep.join(os.path.split(os.path.realpath(__file__))[0].split(os.path.sep)[:-1])
    shutil.rmtree(os.path.join(dst_dir,'templates',config['english_name']+'manager'))
    shutil.rmtree(os.path.join(dst_dir,'apps',config['english_name']+'manager'))

if __name__ == "__main__":
    args = sys.argv
    deploy_flag = False
    batch_flag = False
    if "-d" in args:
        deploy_flag = True
    if '-b' in args:
        batch_flag = True
    if  "-u" in args:
        uninstall(batch_flag)
    else:
        create(batch_flag,deploy_flag)
