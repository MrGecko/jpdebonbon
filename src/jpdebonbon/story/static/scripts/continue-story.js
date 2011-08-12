$(document).ready(function(){
	
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
				continuerHistoire($(this).find(":input[type='hidden']").val(), ma_couleur);//$(this).index());
			}	
		}
	}
	
	function binder_demander_bouton(){
		$(this).unbind();
		var ma_couleur = ($(this).closest("li").hasClass("piste_vert") ? "vert" : "orange"); 
		continuerHistoire($(this).closest("li").find(":input[type='hidden']").val(), ma_couleur);
	}
	
	
	function continuerHistoire(index, ma_couleur) {
		$.ajax({
			  url: './'+index+"/"+ma_couleur,
			  success: function(data) {		
				  var recit = $("#en-tete-milieu-bas").prev();
				  recit.animate({"padding-bottom" : 0}, 500);
				  //recit.find("ul").animate({"padding-bottom" : 0}, 300);
				  
				  //fermer les pistes du recit
				  recit.find("li").each(function(){
					  if ($(this).find(":input[type='hidden']").val() == index)	{					  
						  $(this).unbind('click').removeClass();
						  
						  //faire disparaitre le textarea et insérer son texte dans le <li>
						  var demander_bouton = $(this).find(".demander-bouton");
						  if (demander_bouton.length > 0) {
							  $(this).find("textarea").fadeOut()
							  demander_bouton.delay(300).slideUp();
							  var text = $(this).find("textarea").val();
							  $(this).find("span > div").first().delay(200).append("<br>"+text);
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