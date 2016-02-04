<!--
<div>
<div style="width:40%;display:block"><ul id="tree" class="ztree"></ul></div>
<div id="readme" style="width:70%;margin-left:25%;"><article class='markdown-body'>
<!-- 顶部的html部分和结尾处的html内容， 用于生成网页左侧的菜单TOC. 第二行中div属性display改为block后，显示TOC -->
-->

# 服务相关API

## 修订历史

| 日期      |  服务版本 |  修改人  | 对应项目版本 | 说明 |
| ----      |---------| --------|  -------  | -------------- |
| 2016.1.14 |   1.0   | 董伟    |  fund    |   汇总整理  |



#接口详情

## 公共类接口

### 1、手机号登陆
    URI: /api/v1/login
    参数:
        phone[必选]: 手机号
    返回:
    {
        "code":状态码
               0:"成功",
        "msg": "错误信息",
        "body":{
        }
    }


## 附一 状态码
### 1、系统状态码
    0: "成功",
    1: "参数错误",
    2: "程序内部错误",
    3: "外部接口错误",
    4: "第三方接口超时",
    5: "接口不存在",
    6: "鉴权失败",
    7: "访问被禁止"

### 2、业务状态码  10000 -> 20000  
    10001: 111
    10002: 222


</article>
</div></div>
<script type="text/javascript" src="http://10.0.1.232:8080/js/jquery-1.10.2.min.js">
</script><script type="text/javascript" src="http://10.0.1.232:8080/js/jquery.ztree.all-3.5.min.js"></script>
<script type="text/javascript" src="http://10.0.1.232:8080/js/jquery.ztree_toc.js"></script>
<link type="text/css" href="http://10.0.1.232:8080/js/css/zTreeStyle.css" rel="stylesheet">

<SCRIPT type="text/javascript" >
$(document).ready(function(){
    $('#tree').ztree_toc({
        is_auto_number: false,
        // documment_selector: '.first_part'
    });
});
</SCRIPT>
