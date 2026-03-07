// 检查名为 'engine' 的 cookie 是否存在
if ($.cookie("engine") === undefined) {
  // 如果不存在，则创建它，并设置初始值
  $.cookie("engine", "Baidu");
}

// 获取 div 元素
const divBaidu = document.getElementById("Baidu");
const divBing = document.getElementById("Bing");
const divGoogle = document.getElementById("Google");
const divDuckduckgo = document.getElementById("Duckduckgo");

// 所有 div 数组 (便于循环)
const divs = [divBaidu, divBing, divGoogle, divDuckduckgo];
const names = ["Baidu", "Bing", "Google", "Duckduckgo"];

// 根据 cookie 值显示对应 div，隐藏其他
function showDivFromCookie(cookieVal) {
  let currentCookie = cookieVal;
  // console.log(currentCookie)

  // 隐藏所有 div
  divBaidu.style.display = "none";
  divBing.style.display = "none";
  divGoogle.style.display = "none";
  divDuckduckgo.style.display = "none";

  if (currentCookie === "Baidu") {
    divBaidu.style.display = "grid";
  } else if (currentCookie === "Bing") {
    divBing.style.display = "grid";
  } else if (currentCookie === "Google") {
    divGoogle.style.display = "grid";
  } else if (currentCookie === "Duckduckgo") {
    divDuckduckgo.style.display = "grid";
  }
}

// 根据 cookie 展示 div
showDivFromCookie($.cookie("engine"));


// 鼠标滚轮切换引擎 /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


let scrollWheelBusy = false; // 简单节流: 每个滚动间隔至少 200ms
let wheelTimeout = null;

// 根据当前显示的 div 和 滚动方向 计算下一个要显示的字母
// direction:  1  向下滚动 (deltaY > 0)
//            -1  向上滚动 (deltaY < 0)
function getNextTarget(currentCookie, direction) {
  const index = names.indexOf(currentCookie); // names 数组下标
  if (index === -1) return "Baidu"; // 容错

  if (direction > 0) {
    // 向下滚动 (顺序循环 A->B->C->A)
    const nextIndex = (index + 1) % 4;
    return names[nextIndex];
  } else {
    // 向上滚动 (反向循环 C->B->A->C)
    const prevIndex = (index - 1 + 4) % 4;
    return names[prevIndex];
  }
}

// 滚轮事件处理函数
function onWheel(event) {
  // 阻止默认滚动行为 (避免页面滚动导致体验差)
  event.preventDefault();

  // 节流控制: 如果正在处理则忽略本次触发
  if (scrollWheelBusy) {
    return;
  }

  // 获取滚轮方向: deltaY > 0 向下滚动, < 0 向上滚动
  const deltaY = event.deltaY;
  if (Math.abs(deltaY) < 5) return; // 极小移动忽略

  const direction = deltaY > 0 ? 1 : -1; // 1: 向下, -1: 向上

  // 计算下一个目标
  const nextTarget = getNextTarget($.cookie("engine"), direction);
  if (nextTarget === $.cookie("engine")) return; // 无变化（理论上不会）

  // 更新 cookie
  $.cookie("engine", nextTarget);
  // 更新显示
  showDivFromCookie(nextTarget);

  // 开启节流
  scrollWheelBusy = true;

  // 延时 200ms 后允许下一次滚动切换 (防止滚轮一次滚动触发多次)
  if (wheelTimeout) clearTimeout(wheelTimeout);
  wheelTimeout = setTimeout(() => {
    scrollWheelBusy = false;
    wheelTimeout = null;
  }, 220);
}

// 监听 wheel 事件 (整个窗口)
window.addEventListener("wheel", onWheel, { passive: false });

// 可选：清理定时器 (但页面长期运行无妨)
// 若页面卸载，移除监听不是必须，但良好实践
window.addEventListener("beforeunload", function () {
  if (wheelTimeout) clearTimeout(wheelTimeout);
  window.removeEventListener("wheel", onWheel);
});


// 鼠标点击切换引擎 /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function switchEngine() {
  // 计算下一个目标
  const nextTarget = getNextTarget($.cookie("engine"), 1);
  if (nextTarget === $.cookie("engine")) return; // 无变化（理论上不会）

  // 更新 cookie
  $.cookie("engine", nextTarget);
  // 更新显示
  showDivFromCookie(nextTarget);
}