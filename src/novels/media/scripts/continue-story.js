	
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
	
	function binder_tooltips() {
		$(".karma_face").qtip({
			content: {
				text: 'Avoir bonne ou mauvaise réputation peut influer sur le déroulement de l\'histoire.',
			},
			position: {
				my: "bottom center",
				at: "top center"
			},
			style: {
				classes: 'ui-tooltip-blue ui-tooltip-shadow',
				width: "200",
				'font-size': 20
			}
		});
		
		$(".karma_points").qtip({
			content: {
				text: 'Le score lié à la réputation',
			},
			position: {
				my: "right center",
				at: "left center"
			},
			style: {
				classes: 'ui-tooltip-blue ui-tooltip-shadow',
				'font-size': 20
			}
		});
	}

	
	function binder_fleche_derouler() {
		var ul = $("ul").last();
		var fleche = this;
		$(ul).slideDown('slow', function() {
			$(fleche).delay(200).slideUp("slow").queue(function(){
				$('html,body').animate({scrollTop: $("#footer").position().top, },'slow');
			});
		});
	}
	

	function binder_li(){
		if ($(this).hasClass("piste_ouverte")) {
			var demander = $(this).find(".demander");
			if (demander.length > 0) {
				$(demander[0]).slideDown('slow', function() {
					$('html,body').animate({scrollTop: $(demander).position().top, },'slow');
				});
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
	
	
	
	//=============================================================================================
	//=============================================================================================
	recuperer_recit_en_cours = false;

	function continuerHistoire(index, mon_theme, ma_reponse) {
		if (!recuperer_recit_en_cours) {
			$.ajax({
				  url: './'+index+"/",
				  type: "POST",
				  crossDomain: true,
				  data : {"theme" : mon_theme, "reponse" :  ma_reponse},
				  beforeSend: function(jqXHR, settings) {
					  recuperer_recit_en_cours = true; 
				  },
				  complete: function(jqXHR, textstatus) {
					  recuperer_recit_en_cours = false;
				  },
				  success: function(data) {		
					  var last_ul = $("ul").last();

					  //fermer les pistes du recit
					  $(last_ul).find("li").each(function(){
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
					  $(last_ul).after(data);
					  $("p").last().hide();
					  if (!$("p").last().hasClass("attente")) {
						  $(".publication_date").last().hide();
					  }
					  
					  $("ul").last().find("li").click(binder_li);
					  $(".fleche_derouler").last().click(binder_fleche_derouler);	
					  $(".demander-bouton").last().click(binder_demander_bouton);	
					  
					  var txtarea = $("textarea").last();//find("textarea");
					  $(txtarea).closest("li").hover(
					      function(){ //handlerIn
					    	  $(txtarea).css("color", "#EEE"); 
						  }, 
						  function(){ //handlerOut
						      $(txtarea).css("color", "black"); 
						  } 
					  );
						
					  binder_tooltips();
					  
					  $(".publication_date").last().delay(300).fadeIn();
					  $("p").last().delay(520).slideDown().queue(function(){
						  	$(".publication_date").last().fadeIn();
							$('html,body').delay(50).animate({scrollTop: $(this).position().top, },'slow');
					  });
					  
				  }
			});
		}

	}
	
	$("li").click(binder_li);
	$(".fleche_derouler").click(binder_fleche_derouler);
	$(".demander-bouton").click(binder_demander_bouton);
	
	$("#colonne-milieu").delay(160).fadeIn().queue(function(){
		$('html,body').animate({scrollTop: $("#footer").position().top, },'slow');
	});

	
	$("textarea").each( function(){
		var txtarea = this;
	    $(this).closest('li').hover(
	        function(){ //handlerIn
	        	$(txtarea).css({"color": "#EEE", "border-color" : "#EEE"}); 
	        }, 
	        function(){ //handlerOut
	        	$(txtarea).css({"color": "black", "border-color" : "#555"}); 
	        } 
		);
	});
	/*
	$("#colonne-milieu").hover(
			function(){
				$(".karma").fadeIn();
			},
			function(){
				$(".karma").fadeOut();
			}
	);
	*/
	binder_tooltips();    
});
