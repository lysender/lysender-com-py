<div class="row">
	<div class="span1">
		<img src="<?php echo $asset->asset_url('/media/images/box-64x64.gif') ?>" alt="tools" />
	</div>
	
	<div class="about-info span8">
		<h2 class="fancy"><a href="<?php echo URL::site('/extra/tools', TRUE) ?>">Tools</a></h2>
		
		<p>This is the home for various online tools for developer that may come in handy for developers
		or QAs in their day to day activities.</p>
	
		<h3 class="thin">Online tools</h3>
		
		<div class="project-info">
			<h4>1. URL Encoder/Decoder</h4>
			
			<p>Copy and paste URLs and strings, convert from raw URL to human readable format and vice versa.</p>
			
			<p><a href="<?php echo URL::site('/extra/tools/urlencode', TRUE) ?>">URL Encoder/Decoder</a>.</p>
		</div>
		
		<div class="project-info">
			<h4>2. World Clock</h4>
			
			<p>Create world clock widgets for different timezones. This is needed when working with other people on different timezones.</p>
			
			<p><a href="<?php echo URL::site('/extra/tools/worldclock', TRUE) ?>">World Clock</a>.</p>
		</div>

		<div class="project-info">
			<h4>3. Base64 Encoder/Decoder</h4>
			
			<p>Base64 encode a string or base64 decode it back. Usefull when working with base64 encoded data.</p>
			
			<p><a href="<?php echo URL::site('/extra/tools/base64', TRUE) ?>">Base64 Encoder/Decoder</a>.</p>
		</div>
	</div>
</div>
