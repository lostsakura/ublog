"use strict";


// 窗口大小变化时，被动调节窗口大小
$(window).resize(function() {
    changeFrameHeight($('#admin_main_content'));
});

// iframe窗口大小调节
function changeFrameHeight(that){
    $(that).height(document.documentElement.clientHeight - 120);
}