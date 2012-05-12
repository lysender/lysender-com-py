$(function() {
	$(".project-images").each(function(){
		$("#" + this.id + " a").lightBox({
			imageLoading: "/media/images/lightbox/lightbox-ico-loading.gif",
			imageBtnClose: "/media/images/lightbox/lightbox-btn-close.gif",
			imageBtnPrev: "/media/images/lightbox/lightbox-btn-prev.gif",
			imageBtnNext: "/media/images/lightbox/lightbox-btn-next.gif",
			imageBlank: "/media/images/lightbox/lightbox-blank.gif"
		});
	});
});
