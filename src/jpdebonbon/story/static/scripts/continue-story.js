	
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
	

$(document).ready(function(){

	
	$("#colonne-milieu").hide();
	
	function binder_fleche_derouler() {
		var recit = $(this).parent();
		var ul = $(recit).find("ul")[0];
		var fleche = this;
		$(ul).slideDown('slow', function() {
			$(fleche).delay(200).slideUp("slow");
		});
	}
	

	function binder_li(){
		if ($(this).hasClass("piste_ouverte")) {
			var demander = $(this).find(".demander");
			if (demander.length > 0) {
				$(demander[0]).slideDown('slow', function() {});
			}
			else {
				var mon_theme = ($(this).hasClass("theme_1") ? "theme_1" : "theme_2"); 
				continuerHistoire($(this).find(":input[type='hidden']").val(), mon_theme, null);//$(this).index());
			}	
		}
	}
	
	
	function binder_demander_bouton(){
		$(this).unbind();
		var mon_theme = ($(this).closest("li").hasClass("theme_1") ? "theme_1" : "theme_2"); 
		var ma_reponse = $(this).closest("li").find("textarea").val();
		continuerHistoire($(this).closest("li").find(":input[type='hidden']").val(), mon_theme, ma_reponse);
	}
	
	
	function continuerHistoire(index, mon_theme, ma_reponse) {
		$.ajax({
			  url: './'+index+"/",
			  type: "POST",
			  crossDomain: true,
			  data : {"theme" : mon_theme, "reponse" :  ma_reponse},
			  success: function(data) {		
				  var recit = $("#en-tete-milieu-bas").prev();

				  //fermer les pistes du recit
				  recit.find("li").each(function(){
					  if ($(this).find(":input[type='hidden']").val() == index)	{					  
						  $(this).unbind('click').removeClass();
						  
						  //faire disparaitre le textarea et insérer son texte dans le <li>
						  var demander = $(this).find(".demander");
						  if (demander.length > 0) {
							  $(demander).find("textarea").fadeOut();
							  demander.delay(300).slideUp();
							  var text = $(demander).find("textarea").val();
							  if (text.length > 0)
								  $(demander).prev().delay(300).append("<br>"+text);
						  }
					  }
					  else
						  $(this).delay(200).slideUp();
				  });
				  
				  //ajouter le recit suivant le fait apparaitre et rétablit les bindings
				  $("#en-tete-milieu-bas").before(data);
				  var new_recit = $("#en-tete-milieu-bas").prev();
				  $(new_recit).find("li").click(binder_li);
				  $(new_recit).find(".fleche_derouler").click(binder_fleche_derouler);	
				  $(new_recit).find(".demander-bouton").click(binder_demander_bouton);	

				  $(new_recit).hide().delay(520).fadeIn().queue(function(){
						$('html,body').delay(50).animate({scrollTop: $(new_recit).position().top, },'slow');
				  });
					
			  }
		});
	}
	
	$("li").click(binder_li);
	$(".fleche_derouler").click(binder_fleche_derouler);
	$(".demander-bouton").click(binder_demander_bouton);
	
	$("#colonne-milieu").delay(100).fadeIn().queue(function(){

		$("#scroll_down").click(function(){
			var new_recit = $("#en-tete-milieu-bas").prev();
			$('html,body').delay(120).animate({scrollTop: $(new_recit).position().top, },'slow');
		})
		
		$("#scroll_up").click(function(){
			$('html,body').delay(120).animate({scrollTop: $("h1").position().top, },'slow');
		})
	});
	

});