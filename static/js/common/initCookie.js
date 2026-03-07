// 检查名为 'tag' 的 cookie 是否存在
if ($.cookie('tag') === undefined) {
    // 如果不存在，则创建它，并设置初始值
    $.cookie('tag', 'DEVELOPMENT');
}