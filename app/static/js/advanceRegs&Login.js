/**
 * Created by shinn on 2016/4/26.
 */
$(document).ready(function(){
    $("#submit").click(function () {
        var username = $("#username").val();
        var pass1 = $("#pass1").val();
        var email = $("#email").val();
        var phone = $("#phone").val();

        var obj = {"name": username, "password":pass1, "email":email, "phone":phone};
        $.ajax("/register", {
            type: 'POST',
            data: obj,
            dataType: 'html'
        }).done(function () {
            console.log("Post advanced register successfully!");
        }).fail(function () {
            console.log("Post advanced register failed!");
        });
    });
});