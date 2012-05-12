$(function(){
	$("#encode-uricomp-btn").click(function(){
		var s = $("#encode-uricomp").val();
		s = $.trim(s);
		
		$("#decode-uricomp").val(encodeURIComponent(s));
	});
	
	$("#decode-uricomp-btn").click(function(){
		var s = $("#decode-uricomp").val();
		s = $.trim(s);
		
		$("#encode-uricomp").val(decodeURIComponent(s));
	});
	
	$("#encode-uri-btn").click(function(){
		var s = $("#encode-uri").val();
		s = $.trim(s);
		
		$("#decode-uri").val(encodeURI(s));
	});
	
	$("#decode-uri-btn").click(function(){
		var s = $("#decode-uri").val();
		s = $.trim(s);
		
		$("#encode-uri").val(decodeURI(s));
	});
});