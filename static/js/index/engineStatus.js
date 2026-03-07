if ($.cookie("engine") == "Baidu") {
    var element = document.getElementById("Baidu");
    element.style.display = "grid";
} else if ($.cookie("engine") == "Bing") {
    var element = document.getElementById("Bing");
    element.style.display = "grid";
} else if ($.cookie("engine") == "Google") {
    var element = document.getElementById("Google");
    element.style.display = "grid";
} else if ($.cookie("engine") == "Duckduckgo") {
    var element = document.getElementById("Duckduckgo");
    element.style.display = "grid";
}