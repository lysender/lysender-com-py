$(function(){
	$("#sumitup").click(function(){
		var text = $.trim($("#texttosum").val());
		text = text.replace("\n\r", "\n");

		var totalLines = 0;
		var grandSum = 0;

		if (text) {
			var lines = text.split("\n");
			totalLines = lines.length;

			for (var i in lines) {
				if (lines.hasOwnProperty(i)) {
					var chunks = lines[i].split(" ", 2);
					if (chunks && typeof chunks[0] !== "undefined") {
						var n = parseInt(chunks[0]);

						if (n && !isNaN(n)) {
							grandSum += n;
						}
					}
				}
			}
		}

		var result = "Total lines: " + totalLines + "\n";
		result += "First col cum: " + grandSum + "\n";

		$("#sumresult").val(result);
	});

	$("#clearitup").click(function(){
		var text = $("#texttosum").val("");
		$("#sumresult").val("");
	});
});