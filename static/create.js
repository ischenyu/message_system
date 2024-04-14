layui.use(['form'], function(){
    var form = layui.form;

    form.on('select(grade)', function(data){
        var grade = data.value;
        var classSelect = $('#classSelect');

        classSelect.empty();
        classSelect.append('<option value="">请选择班级</option>');

        if (grade === '8') {
            for (var i = 1; i <= 16; i++) {
                classSelect.append('<option value="' + i + '">' + i + '班</option>');
            }
        } else if (grade === '9') {
            for (var i = 1; i <= 16; i++) {
                classSelect.append('<option value="' + i + '">' + i + '班</option>');
            }
        }

        form.render('select');
    });
});
layui.use(['form', 'jquery'], function(){
    var form = layui.form;
    var $ = layui.jquery;
    var layer = layui.layer;

    form.on('submit(demo-login)', function(data){
        var formData = {
            username: $('input[name="username"]').val(),
            grade: $('#gradeSelect').val(),
            class: $('#classSelect').val(),
            message: $('textarea').val()
        };

        $.ajax({
            type: 'POST',
            url: '/api/create', // 替换为你的后端 API 地址
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                // 处理成功响应
                if(response.code === 200){
                    layer.msg('提交成功', {icon: 6});
                }if(response.code === 500){
                    layer.msg('服务器内部错误', {icon: 5});
                }if(response.code === 429){
                    layer.msg('请求过快，服务器拒绝了你的请求(你想把我的数据库存炸是不可能的￣へ￣)', {icon: 5});
                }
            },
            error: function(xhr, status, error) {
                // 处理错误响应
                layer.msg('提交失败，请联系paimon@alistnas.top', {icon: 5});
            }
        });

        return false; // 阻止表单默认提交行为
    });
});