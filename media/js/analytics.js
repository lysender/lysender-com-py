$(function(){
    $(".ga-track").click(function(){
        var category = $(this).attr("data-category");
        var action = $(this).attr("data-action");
        var label = $(this).attr("data-label");

        fire_ga_event(category, action, label);
    });
});

function fire_ga_event(category, action, label) {
    if (typeof _gaq !== "undefined") {
        _gaq.push(['_trackEvent', category, action, label]);
    }
}