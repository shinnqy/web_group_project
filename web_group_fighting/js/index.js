$(document).ready(function(){
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
	$('#account_desc_1').click(function(){
		$('.login-form').hide();
		$('.register-form').show("slow");
		$('.login-form').show("slow");
	});
	$('#account_desc_2').click(function(){
		$('.register-form').hide();
	    $('.getpassword-form').hide();
		$('.login-page').show();
		$('.login-form').show("slow");
	});

});
