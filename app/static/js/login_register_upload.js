$(document).ready(function(){

	$('#links_left a').click(function(){
		$('.login-form').hide();
		$('.getpassword-form').show("slow");
	});
	$('.message a').click(function(){
		$('.register-form').hide();
		$('.getpassword-form').hide();
		window.location.assign("/register?#");
		//$('.login-form').show("slow");
	});
	$('#links_right a').click(function(){ 
		$('.login-form').hide();
		window.location.assign("/login?#");
	});

	$("#create").click(function(){
		var name = document.getElementById("name").value;
		var password = document.getElementById("password").value;
		var email = $('#email').val();
		var obj = {'name':name, 'password':password, 'email':email};

		if (email.slice(-12) == ".cuhk.edu.hk" && password != "" && name != ""){
			$.ajax('/register',{
				type: 'POST',
				data: obj,
				dataType: 'html'
			}).done(function(output){
				console.log(output);
				if (output == "ok"){
					window.location.assign("/login?#");

					alert("You have registered successfully, you can login in now!");

				}
				if (output == "email exist"){
					alert("This email exist!!");
				}
				console.log("Post success!");
			}).fail(function(){
				console.log("Post fail!");
			});
		}
	
	});

	$("#login").click(function(){
		var email = document.getElementById("loginEmail").value;
		var password = document.getElementById("loginPassword").value;
		var obj = {'email':email, 'password':password};

		if (email.slice(-12) == ".cuhk.edu.hk" && password != ""){
			$.ajax('/login',{
				type: 'POST',
				data: obj,
				dataType: 'html'
			}).done(function(output){
				console.log(output);
				if (output == "correctPassword"){
					window.location.assign("/");
				}
				if (output == "wrongPassword"){
					alert("Wrong password!");
				}
				if (output == "noSuchEmail"){
					alert("No such email!")
				}
				console.log("Post success!");
			}).fail(function(){
				console.log("Post fail!");
			});
		}
		
	});

	$("#confirm").click(function(){
		var email = document.getElementById("getEmail").value;
		var password = document.getElementById("getPassword").value;
		var obj = {'email':email, 'password':password};

		if (email.slice(-12) == ".cuhk.edu.hk" && password != ""){
			$.ajax('/find_password',{
				type: 'POST',
				data: obj,
				dataType: 'html'
			}).done(function(output){
				console.log(output);
				if (output == "success"){
					alert("Successfully changed the password!");
					window.location.assign("/login?#");
				}
				console.log("Post success!");
			}).fail(function(){
				console.log("Post fail!");
			});
		}
		
	});

	$("#update").click(function () {
		var name = $("#name").val();
		var location = $("#location").val();
		var aboutMe = $("#about_me").val();
		var obj = {'name':name, 'location':location, 'aboutMe':aboutMe };

		if (name || location || aboutMe){
			$.ajax('/editProfile', {
				type: 'POST',
				data: obj,
				dataType: 'html'
			}).done(function (output) {
				console.log("Update post successfully!");
			}).fail(function () {
				console.log("Update post fail!");
			});
		}

	});
	
	$("#submit").click(function () {
		var body = $("#body").val();
		var obj = {'body': body};

		if (body != ""){
			$.ajax('/upload',{
				type: 'POST',
				data: obj,
				dataType: 'html'
			}).done(function (output) {
				console.log("Submit post successfully!");
			}).fail(function () {
				console.log("Submit post fail!");
			});
		}
	});
	
	// $("#submit_avator").click(function () {
	// 	var image = $("#avator").val();
	// 	var obj = {'image': image};
    //
	// 	if (image != undefined) {
	// 		$.ajax('/upload/avator',{
	// 			type: 'POST',
	// 			data: obj
	// 		}).done(function (output) {
	// 			console.log("Image post successfully!");
	// 		}).fail(function () {
	// 			console.log("Image post fail!");
	// 		});
	// 	}
	// });
	
	// $("#post").click(function () {
	// 	var itemName = $("#itmeName").val();
	// 	var estimateValue = $("#estimateValue").val();
	// 	var description = $("#description").val();
	// 	var obj = {'itemName':itemName, 'estimateValue':estimateValue, 'description':description};
    //
	// 	$.ajax('',{
	// 		type: 'POST',
	// 		data: obj,
	// 		dateType: 'html'
	// 	}).done(function () {
	// 		console.log("Post successfully!");
	// 	}).fail(function () {
	// 		console.log("Post failed!")
	// 	});
	// });

	function haveExchange(id, para) {
		var haveExchange = true;
		var obj = {'haveExchange': haveExchange};

		$.ajax('/changeItemStatus/' + id,{
			type: 'POST',
			data: obj,
			dateType: 'html'
		}).done(function (output) {
			$(para).attr("disabled", "disabled");
			console.log(output);
			console.log("Post exchange successfully!");
		}).fail(function () {
			console.log("Post exchange fail!");
		});
	}
	window.haveExchange = haveExchange;

	function postToItem(id) {
		var textBody = $("#textBody").val();
		var obj = {'textBody': textBody};

		$.ajax('/product/' + id,{
			type: 'POST',
			data: obj,
			dateType: 'html'
		}).done(function () {
			console.log("Post text successfully!");
		}).fail(function () {
			console.log("Post text fail!");
		});
	}
	window.postToItem = postToItem;
	
	function addToInteres(id) {
		var obj = {'id': id};

		$.ajax('/interestInfoHandler',{
			type: 'POST',
			data: obj,
			dateType: 'html'
		}).done(function (output) {
			alert(output);
			console.log(output);
			console.log("Post interest successfully!");
		}).fail(function () {
			console.log("Post interest fail!");
		});
	}
	window.addToInteres = addToInteres;

	function setBuyer(thispara, id) {
		var buyeremail = $(thispara).text();
		var obj = {'buyeremail': buyeremail, "id": id};

		$.ajax('/setBuyerHandler',{
			type: 'POST',
			data: obj,
			dateType: 'html'
		}).done(function (output) {
			alert(output);
			console.log(output);
			console.log("Post interest successfully!");
		}).fail(function () {
			console.log("Post interest fail!");
		});
	}
	window.setBuyer = setBuyer;

});

