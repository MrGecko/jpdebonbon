$(document).ready(function(){
	
	//pour autoriser les POST en ajax et ne pas se taper de 403 forbidden
	$.ajaxSetup({ 
	     beforeSend: function(xhr, settings) {
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
	         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
	             // Only send the token to relative URLs i.e. locally.
	             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	         }
	     } 
	});
	
	
	$("#colonne-milieu").hide();
	
	function binder_fleche_derouler() {
		var recit = $(this).parent();
		var ul = $(recit).find("ul")[0];
		var fleche = this;
		$(ul).slideDown('slow', function() {
			//$(recit).css("padding-bottom", "0px");
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
				var ma_couleur = ($(this).hasClass("piste_vert") ? "vert" : "orange"); 
				continuerHistoire($(this).find(":input[type='hidden']").val(), ma_couleur, null);//$(this).index());
			}	
		}
	}
	
	
	function binder_demander_bouton(){
		$(this).unbind();
		var ma_couleur = ($(this).closest("li").hasClass("piste_vert") ? "vert" : "orange"); 
		var ma_reponse = $(this).closest("li").find("textarea").val();
		continuerHistoire($(this).closest("li").find(":input[type='hidden']").val(), ma_couleur, ma_reponse);
	}
	
	
	function continuerHistoire(index, ma_couleur, ma_reponse) {
		$.ajax({
			  url: './'+index+"/",
			  type: "POST",
			  data : {"couleur" : ma_couleur, "reponse" :  ma_reponse},
			  success: function(data) {		
				  var recit = $("#en-tete-milieu-bas").prev();
				  //recit.animate({"padding-bottom" : 0}, 500);
				  //recit.find("ul").animate({"padding-bottom" : 0}, 300);
				  
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

				  $(new_recit).hide().delay(800).fadeIn();
			  }
		});
	}
	
	$("li").click(binder_li);
	$(".fleche_derouler").click(binder_fleche_derouler);
	$(".demander-bouton").click(binder_demander_bouton);
	
	$("#colonne-milieu").delay(300).fadeIn();
	
});