layui.use(function(){
    var $ = layui.$;
    var form = layui.form;
    var layer = layui.layer;
    var util = layui.util;
    
    form.on('submit(demo-login)', function(data){
        var field = data.field; // 获取表单字段值
    
        // 使用jQuery的Ajax方式提交表单数据
        $.ajax({
            url: '/login',
            type: 'POST',
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(field),
            success: function(res){
                if(res.code === 200){
                    layer.msg('登录成功', {icon: 6});
                    // 设置要重定向的 URL
                    var newLocation = '/';
                    // 执行页面重定向
                    window.location.href = newLocation;
                }else if(res.code === 401){
                    layer.msg('用户名或密码错误', {icon: 5});
                }else if(res.code === 429){
                    layer.msg('请求过快，服务器拒绝了你的请求', {icon: 5});
                }
            },
            error: function(xhr, status, error) {
                layer.msg('请求失败，请重试', {icon: 5});
            }
        });
    
        return false; // 阻止默认 form 跳转
    });

  });