function hideOverlay() {
    // 获取 class 为 fullscreen-overlay 的第一个元素
    const overlay = document.querySelector('.fullscreen-overlay');
    // console.log(overlay)

    // 如果元素存在，则修改其样式
    if (overlay) {
        overlay.style.opacity = '0';
        overlay.style.visibility = 'hidden';
    } else {
        console.warn('未找到 class 为 fullscreen-overlay 的元素');
    }
}

function switchTag(element) {
    // 获取点击对象的 ID
    const id = element.id;

    // 修改 cookie
    $.cookie('tag', id);

    // 隐藏组件
    hideOverlay()

    // 强制从服务器重新加载（跳过缓存）
    location.reload(true);
}


