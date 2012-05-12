<div class="row">
	<div class="span1">
		<img src="<?php echo $asset->asset_url('/media/images/box-64x64.gif') ?>" alt="tools" />
	</div>
	
	<div class="about-info span11">
		<div class="row">
	
			<div class="span11">
				<h2 class="fancy"><a href="<?php echo URL::site('/extra/tools/worldclock', TRUE) ?>">World Clock</a></h2>
				
				<p>This tool allows you to define your word clock widget as many as you like and display them for quick reference.<br />
				The widgets created are saved so that they will be displayed on your next visit.</p>
			</div>

			<?php if (isset($selected_timezone) && isset($formatted_timezone)): ?>
				<div class="span11" id="worldclock-widget-current-w">
					<h2 class="thin">Current time for <?php echo HTML::chars($formatted_timezone) ?></h2>
				</div>
			<?php endif ?>

			<div class="span11" id="workdclock-widget-w">
				<h2 class="thin">Your World Clock widgets</h2>
			</div>
			
			<div class="span11">
				<form class="form-horizontal">
					<fieldset>
						<legend>Add a new world clock widget</legend>
						<div class="control-group">
							<label class="control-label">Select region</label>
							<div class="controls" id="region-select-w">
								<select id="regions" name="regions"></select>
							</div>
						</div>
						<div class="control-group">
							<label class="control-label">Select timezone</label>
							<div class="controls">
								<select id="timezone" name="timezone" disabled="disabled"></select>
							</div>
						</div>
						<div class="form-actions">
							<input type="button" name="add-tz" id="add-tz" class="btn btn-primary icon-plus" value="Add new clock" disabled="disabled" />
						</div>
					</fieldset>
				</form>
			</div>
			
			<div class="span11">
				<p>Timezones around the world.</p>
				<ul id="timezone-list">
					<?php foreach ($timezones as $tz => $offset): ?>
						<li><a href="<?php echo URL::site('/extra/tools/worldclock/'.HTML::chars($tz), TRUE) ?>"><?php echo HTML::chars($tz) ?></a></li>
					<?php endforeach ?>
				</ul>
			</div>

			<div class="span11">
				<p class="push-down-3">For comments and suggestions, <a href="http://blog.lysender.com/2012/03/yet-another-world-clock/">see the blog post</a>. Enjoy and share.</p>
			</div>
		
			<div class="span11">
				<a class="fblike-single" href="http://www.facebook.com/plugins/like.php?href=<?php echo urlencode(URL::site('/extra/tools/worldclock', TRUE)) ?>&amp;layout=standard&amp;show_faces=false&amp;width=450&amp;action=like&amp;font&amp;colorscheme=light&amp;height=35"></a>
			</div>
			
			<div class="span11">
				<g:plusone annotation="inline" href="<?php echo URL::site('/extra/tools/worldclock', TRUE) ?>"></g:plusone>
			</div>
		</div><!-- row -->
	</div><!-- span11 -->
</div><!-- span12 -->