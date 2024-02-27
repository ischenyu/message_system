layui.use(function(){
    var $ = layui.$;
    var form = layui.form;
    var layer = layui.layer;
    var util = layui.util;
    
    // 自定义验证规则
    form.verify({
      // 确认密码
      confirmPassword: function(value, item){
        var passwordValue = $('#reg-password').val();
        if(value !== passwordValue){
          return '两次密码输入不一致';
        }
      }
    });
    
    // 提交事件
    form.on('submit(demo-reg)', function(data){
      var field = data.field; // 获取表单字段值
      
      // 是否勾选同意
      if(!field.agreement){
        layer.msg('您必须勾选同意用户协议才能注册');
        return false;
      }
      
      // 显示填写结果，仅作演示用
      layer.alert(JSON.stringify(field), {
        title: '当前填写的字段值'
      });

      $.ajax({
        url: '/api/user/register',
        type: 'POST',
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(field),
        success: function(res){
            if(res.code === 200){
              layer.msg('注册成功', {icon: 6});
              window.location.replace("/home");
          } else if(res.code === 402) {
              layer.msg('用户已存在', {icon: 6});
          } else {
              layer.msg('注册失败', {icon: 5});
          }
        },
        error: function(xhr, status, error) {
            console.log("Error:", error);
            layer.msg('请求失败，请重试', {icon: 5});
        }
    });
  
      return false; // 阻止默认 form 跳转
    });
    
    // 普通事件
    util.on('lay-on', {
      // 获取验证码
      'reg-get-vercode': function(othis){
        var isvalid = form.validate('#reg-email'); // 主动触发验证，v2.7.0 新增 
        var inputElement = document.getElementById("reg-email");
        var email = inputElement.value;
        // 验证通过
        if(isvalid){
          // layer.msg('邮箱规则验证通过');
          // 此处可继续书写「发送验证码」等后续逻辑
          $.ajax({
            url: '/api/user/register/captcha',
            type: 'POST',
            dataType:"json",
            contentType:"application/json",
            data: JSON.stringify({"email": email}),
            success: function(res){
              if(res.code === 200){
                layer.msg('验证码发送成功，请及时查收', {icon: 6});
              }else{
                layer.msg(res.msg, {icon: 7});
              }
            }
          });
        }
      }
    });
  });