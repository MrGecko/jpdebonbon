	
//pour autoriser les POST en ajax et ne pas se taper de 403 forbidden
$(document).ajaxSend(function(event, xhr, settings) {
	    function getCookie(name) {
	        var cookieValue = null;
	        if (document.cookie && document.cookie != '') {
	            var cookies = document.cookie.split(';');
	            for (var i = 0; i < cookies.length; i++) {
	                var cookie = jQuery.trim(cookies[i]);
	                // Does this cookie string begin with the name we want?
	                if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                    break;
	                }
	            }
	        }
	        return cookieValue;
	    }
	    function sameOrigin(url) {
	        // url could be relative or scheme relative or absolute
	        var host = document.location.host; // host + port
	        var protocol = document.location.protocol;
	        var sr_origin = '//' + host;
	        var origin = protocol + sr_origin;
	        // Allow absolute or scheme relative URLs to same origin
	        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
	            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
	            // or any other URL that isn't scheme relative or absolute i.e relative.
	            !(/^(\/\/|http:|https:).*/.test(url));
	    }
	    function safeMethod(method) {
	        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	    }

	    if (!safeMethod(settings.type)) {
	    	var cookie = getCookie('csrftoken');
	        xhr.setRequestHeader("X-CSRFToken", cookie);
	    }
	});
	

function getRecitDescription(titre_url) {
	$.ajax({
		  url: '/story/'+titre_url+'/description/',
		  type: "POST",
		  crossDomain: true,
		  data : {"titre_url" : titre_url},
		  success: function(data) {		
			  $("#recit").html(data);
		  },
	});
};

$(document).ready(function(){
	$("#pages-container").hide();
	
	$("#pages-container").hover(
			function(){
				//$("#notice").fadeOut(300);
			},
			function(){
				//$("#notice").fadeIn(300);//.css("display", "visible");
			}
	);
	
	$("#pages li").hover(
			function(){
				$(this).children("a").css("color", "#FFF");
				$("#notice").hide();
				getRecitDescription($(this).children("a").attr("name"));
				$("#recit").show();//fadeIn(160);
			},
			function(){
				$(this).children("a").css("color", "#555");
				$("#recit").hide();//fadeOut(160).html("");
				$("#notice").show();

			}
	);
	
	$("#pages li").click( function(){
		$(location).attr("href", $(this).children("a").attr("href"));
	});
	
	$("#pages-container").delay(60).fadeIn();

});


