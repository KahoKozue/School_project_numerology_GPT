$(document).ready(function(){
    $('#menu').click(function(){
        $(this).toggleClass('fa-times');
        $('header').toggleClass('toggle');
        
    });
    $(window).on('scroll load',function(){
        $('#menu').removeClass('fa-times');
        $('header').removeClass('toggle');
    });
});

function toggleTest(content) {
    var testContent = document.getElementById("testContent");
    if (testContent.classList.contains("hidden")) {
        showContent(content);
    } else {
        hideContent();
    }
}

function showContent(content) {
    var testContent = document.getElementById("testContent");
    testContent.innerHTML = content;
    testContent.classList.remove("hidden");
}

function hideContent() {
    var testContent = document.getElementById("testContent");
    testContent.classList.add("hidden");
}



