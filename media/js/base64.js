$(function(){
	$("#base64-encode-btn").click(function(){
		var str = $("#base64-encode").val();
		str = $.trim(str);

		$("#base64-decode").val(base64_encode(str));
	});

	$("#base64-decode-btn").click(function(){
		var str = $("#base64-decode").val();
		str = $.trim(str);

		$("#base64-encode").val(base64_decode(str));
	});
});