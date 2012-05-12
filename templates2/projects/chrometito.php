<div class="row">
	<div class="span1">
		<img src="<?php echo $asset->asset_url('/media/images/portfolio/chrome-tito/64.png') ?>" alt="projects" />
	</div>
	
	<div class="about-info span8">
		<div class="row">
			<div class="span8">
				<h2 class="fancy"><a href="<?php echo URL::site('/projects/chrome-time-in-time-out', TRUE) ?>">Google Chrome Time-in Time-out Extension</a></h2>
			</div>
			
			<div class="project-info span8">
				<div class="row">
					<div class="span8">
						<p>Google Chrome extension that reminds you to time-in and time-out.
						This is especially helpful when your company uses a computerized/networked
						time-in and time-out system.</p>
						
						<h3>Installation</h3>
						
						<p><a href="http://www.lysender.com/chrome-timein-timeout/chrome-timein-timeout.crx">To install the extension, click here.</a></p>
						
						<p>After installing the extension, go to Tools -&gt; Extensions and look for
						the Time-in Time-out extension and click options. Set the Time-in and timeout
						time and leave the Activated checkbox checked. </p>
					</div>
					
					<div class="project-images span8" id="chrome-tito-project-images">
						<ul class="thumbnails">
						<?php foreach ($project_images['chrome-tito'] as $image): ?>
							<li class="span3">
								<a class="thumbnail" href="<?php echo $asset->asset_url('/media/images/portfolio/chrome-tito/'.$image) ?>">
									<img src="<?php echo $asset->asset_url('/media/images/portfolio/chrome-tito/'.$image) ?>" alt="Techtuit project image" />
								</a>
							</li>
						<?php endforeach ?>
						</ul>
					</div>
					
					<div class="span8">
						<h4>Contact</h4>
						
						<p>Source code extension is available in Github. View the source at:<br />
						<a href="https://github.com/lysender/chrome-time-in-time-out">https://github.com/lysender/chrome-time-in-time-out</a>.</p>
						
						<p>For feedbacks, suggestions and bug reports, please send an email to <?php echo HTML::mailto('leonel@lysender.com') ?></p>
						
						<h4>Credits</h4>
						
						<p>Original code based on Google Chrome Notification samples.</p>
						
						<p>Icons by KDE Artwork team.</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
