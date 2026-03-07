// 键盘搜索触发器
document.getElementById('search').addEventListener('keydown', function(event) {
    // 获取搜索引擎
    engine = $.cookie("engine_cookie")
    // console.log(engine)
    // 检查回车键是否按下
    if (event.key === 'Enter') {
        const inputValue = document.getElementById('search').value;
        if (engine == "Baidu") {
            window.location.href = `https://www.baidu.com/s?wd=${inputValue}`;
        } else if (engine == "Bing") {
            window.location.href = `https://www.bing.com/search?q=${inputValue}`;
        } else if (engine == "Google") {
            window.location.href = `https://www.google.com/search?q=${inputValue}`;
        } else if (engine == "Duckduckgo") {
            window.location.href = `https://duckduckgo.com/?q=${inputValue}`;
        }
    }
});

// 鼠标搜索触发器
document.getElementById('mcp').addEventListener('click', function(event) {
    // 获取搜索引擎
    engine = $.cookie("engine_cookie")
    // console.log(engine)
    const inputValue = document.getElementById('search').value;
    if (engine == "Baidu") {
        window.location.href = `https://www.baidu.com/s?wd=${inputValue}`;
    } else if (engine == "Bing") {
        window.location.href = `https://www.bing.com/search?q=${inputValue}`;
    } else if (engine == "Google") {
        window.location.href = `https://www.google.com/search?q=${inputValue}`;
    } else if (engine == "Duckduckgo") {
        window.location.href = `https://duckduckgo.com/?q=${inputValue}`;
    }
});