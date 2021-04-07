$(document).ready(function(){
    $("#sendToProf").click(function(){
        $.ajax({
            url: "askAlumni",
            type: "get",
            data: {
                userPost:$("#myText").val()
            },
            success: function(response){
                console.log( $("#myText").val() );
            }

        });
    });
});