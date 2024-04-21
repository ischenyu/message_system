var layer = layui.layer;
layui.use('table', function(){
            var table = layui.table;

            // 加载数据到表格中
            table.render({
                elem: '#messageTable',
                url: '/messages', // 数据接口
                page: false, // 关闭分页
                cols: [[
                    {field: 'id', title: 'ID', width: 80},
                    {field: 'username', title: '用户名'},
                    {field: 'ip', title: 'IP地址'},
                    {field: 'message', title: '消息内容'},
                    {field: 'grade', title: '等级', width: 80},
                    {field: 'class', title: '班级', width: 80},
                    {fixed: 'right', toolbar: '#operate', title: '操作'}
                ]]
            });

            // 监听表格操作栏的按钮点击事件
            table.on('tool(messageTable)', function(obj){
                var data = obj.data; // 获取当前行数据
                var id = data.id; // 获取当前行ID
                if(obj.event === 'like'){ // 点赞按钮点击事件
                    // 发送点赞请求到后端，这里以控制台输出为例
                    layer.msg('点赞id' + id, {icon: 5});
                } else if(obj.event === 'report'){ // 举报按钮点击事件
                    // 发送举报请求到后端，这里以控制台输出为例
                    layer.msg('举报id' + id, {icon: 5});
                }
            });
        });