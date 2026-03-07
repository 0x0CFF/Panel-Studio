function showtagSelector() {
    // 获取 class 为 fullscreen-overlay 的第一个元素
    const overlay = document.querySelector('.fullscreen-overlay');
    // console.log(overlay)

    // 如果元素存在，则修改其样式
    if (overlay) {
        overlay.style.opacity = '1';
        overlay.style.visibility = 'visible';
    } else {
        console.warn('未找到 class 为 fullscreen-overlay 的元素');
    }
}