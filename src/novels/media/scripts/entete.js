$(document).ready(function(){
	$("#home").click(function() { $(location).attr('href', "/home/"); });
	$("#logout").click(function() { $(location).attr('href', "/home/logout"); });
});
