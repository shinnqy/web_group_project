$('#links_left a').click(function(){
   $('.login-form').hide();
   $('.getpassword-form').show("slow");
});
$('.message a').click(function(){
   $('.register-form').hide();
   $('.getpassword-form').hide();
   $('.login-form').show("slow");
});
$('#links_right a').click(function(){
   
   $('.login-form').hide();
   $('.register-form').show("slow");
});