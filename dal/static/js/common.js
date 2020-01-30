window.onload = function(){
    alert("script");
    document.getElementById('compareSearchBtn').onclick = function(){
        var form = document.getElementById('compareSearchForm');
        var checkList = document.querySelectorAll("input[type='checkbox']:checked");
        var checkListStr = "";

        if( checkList.length > 0 ){                
            checkList.forEach(function(ele){
                checkListStr += ele.value + ",";
            });
            checkListStr = checkListStr.substring(0, checkListStr.length - 1);
        }

        form.compareConditionList.value = checkListStr;            
    }
}