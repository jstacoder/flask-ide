function hidebar(side){
    $("sidebar-"+side).hide();
    var $main = $(".main"),
    mClass = $main.hasClass("col-md-8") ? "col-md-8" : "col-md-10",
    newMClass = mClass == 'col-md-8' ? "col-md-10" : "col-md-12";

    $main.removeClass(mClass).addClass(newMClass);
}


$(function(){
    
});
