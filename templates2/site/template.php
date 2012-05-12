<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title><?php echo ( ! empty($title)) ? $title.' :: ' : '' ?>Lysender</title>
	
<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="robots" content="all" />
	
<?php if (isset($description) && $description): ?>
<meta name="description" content="<?php echo $description ?>" />
<?php endif ?>
	
<?php if (isset($keywords) && $keywords): ?>
<meta name="keywords" content="<?php echo $keywords ?>" />
<?php endif ?>

<link rel="shortcut icon" href="<?php echo URL::site('/favicon.ico?v='.APP_VERSION, true) ?>" />

<!-- basic styles -->
<?php foreach ($styles as $style => $media)
	echo HTML::style($style.'?v='.APP_VERSION, array('media' => $media)), "\n" ?>

<script type="text/javascript">
	var base_url = '<?php echo URL::site('/', true) ?>';
</script>
	
<?php if (Kohana::$environment == Kohana::DEVELOPMENT && Kohana::$profiling): ?>
<!-- Profiler Styles -->
<style type="text/css">
	<?php include Kohana::find_file('views', 'profiler/style', 'css') ?>
</style>
<?php endif ?>
</head>

<body>
<div class="container">
	<div class="row">
		<div id="header" class="span12">
			<?php echo $header ?>
		</div><!-- #header -->
		
		<div id="content" class="span12">
			<?php echo $content ?>
		</div><!-- #content -->
		
		<div id="footer" class="span12">
			<?php echo $footer ?>
		</div><!-- #footer -->
	</div><!-- .row -->
</div><!-- .container -->

<!-- basic scripts -->
<?php foreach ($scripts as $script)
	echo HTML::script($script.'?v='.APP_VERSION), "\n" ?>

<script type="text/javascript">
	<?php
		if (isset($head_scripts) && $head_scripts) {
			echo $head_scripts."\n";
		}
	?>
	$(function(){
		<?php
			if (isset($head_readyscripts) && $head_readyscripts) {
				echo $head_readyscripts."\n";
			}
		?>
	});
</script>

<?php if (isset($show_google_plusone) && $show_google_plusone): ?>
<script type="text/javascript">
	$(window).load(function(){
		var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
		po.src = 'https://apis.google.com/js/plusone.js';
		var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
	});
</script>
<?php endif ?>

<?php if (isset($show_facebook_like) && $show_facebook_like): ?>
<script type="text/javascript">
	$(window).load(function(){
		$(".fblike-single").each(function(){
			var t = $(this);
			var info = t.attr("href");
			t.replaceWith("<iframe src='" + info + "' scrolling=\"no\" frameborder=\"0\" style=\"border:none; overflow:hidden; width:450px; height:35px;\" allowTransparency=\"true\"></iframe>");
		});
	});
</script>
<?php endif ?>

<?php if (Kohana::$environment == Kohana::PRODUCTION): ?>
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-7713082-2']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
<?php endif ?>
</body>
</html>
