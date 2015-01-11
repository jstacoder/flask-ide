$(function(){
function addToProgressBar(e,num){
       if(undefined === num){            
            num = 1;
       }
       var percent = 100/$(".list-group-item").length*num;
       var current = parseFloat($(".progress-bar").attr("style").split(":")[1]);
       if(current < 100){
           //var current = parseInt($(".progress-bar").attr("width"))/$(".list-group-item.complete").length;
           var ccurent = current + percent;
           console.info(ccurent);
           console.info(percent);
           console.info(current);
           console.info(num);
           $(".progress-bar").attr("style","width:"+ccurent+"%");
           $(".progress-bar-text").text(String(ccurent).substr(0,5)+"% complete");
       }
   }
    function checkOffBox(elem){
        elem.find("input[type=checkbox]")[0].checked = true;
    }
    function unCheckBox(elem){
        elem.find("input[type=checkbox]")[0].checked = false;
    }
    function strikeOutText(elem){
        elem.find("label").css("text-decoration","line-through")
    }
    function checkChecked(elem){
        return elem.children().find("input[type=checkbox]")[0].checked;
    }
    $(document).on("click",".list-group-item",function(){
        if(!checkChecked){
            addToProgressBar($(this));
            checkOffBox($(this));
            strikeOutText($(this));
        }
    });
});
