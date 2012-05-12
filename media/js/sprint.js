(function($){
	$(function(){
		SprintNameGenerator.init();

		$("#btn-generate").click(function(){
			SprintNameGenerator.generateList();
		});
	});
})(jQuery);

window.SprintNameGenerator = {
	adjCount: 0,
	animalCount: 0,
	
	init: function() {
		if (typeof sprintAdj !== "undefined" && typeof sprintAnimals !== "undefined") {
			if (sprintAdj.length > 0 && sprintAnimals.length > 0) {
				this.adjCount = sprintAdj.length;
				this.animalCount = sprintAnimals.length;

				this.generateList();
			}
		}
	},

	generateList: function() {
		var html = '<ul>';
		var list = [];

		for (var x = 0; x < 10; x++) {
			var s = this.generate();
			if (s) {
				list.push(s);
			}
		}
		
		if (list.length > 0) {
			for (var i in list) {
				html += '<li>' + list[i] + '</li>';
			}
		}

		html += '<ul>';

		$("#suggestion-w").html(html);
	},

	generate: function() {
		var adj = Math.floor(Math.random() * this.adjCount);
		var animal = Math.floor(Math.random() * this.animalCount);

		var name = "";

		if (adj in sprintAdj) {
			name = sprintAdj[adj];

			if (animal in sprintAnimals) {
				name += (" " + sprintAnimals[animal]);
			}
		}

		return name;
	}
};