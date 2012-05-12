<div class="row">
	<div class="span1">
		<img src="<?php echo $asset->asset_url('/media/images/chalkboard-64x64.gif') ?>" alt="projects" />
	</div>
	
	<div class="about-info span11">
		<div class="row">
			<div class="span11">
				<h2 class="fancy"><a href="<?php echo URL::site('/extra/sprint', TRUE) ?>">Sprint Name Generator</a></h2>
				
				<p>Select a letter from the list below and suggestions will be shown.</p>
			
				<h3 id="sprint-letters" class="thin">
				<?php foreach ($letters as $l): ?>
					<a href="<?php echo URL::site('/extra/sprint/'.$l, TRUE) ?>"><?php echo strtoupper($l) ?></a>
				<?php endforeach ?>
				</h3>
			
				<?php if (isset($letter)): ?>
				<p><a href="<?php echo URL::site('/extra/sprint', TRUE) ?>">Back to sprint name index</a></p>
				<div class="project-info">
					<h4 class="thin positive">Sprint name suggestions for letter "<?php echo strtoupper($letter) ?>"</h4>
			
					<?php if ($has_list): ?>
						<div id="suggestion-w"></div>
						<p>
							<a href="javascript:void(0);" class="btn btn-primary" id="btn-generate">Generate suggestions</a>
						</p>
					<?php else: ?>
						<div class="alert alert-error">
							Sorry, no list for this sprint.
						</div>
					<?php endif ?>
				</div>
				<?php endif ?>
			</div>
			
			<div class="span11">
				<p class="push-down-3">Enjoy and share.</p>
			</div>
		
			<div class="span11">
				<a class="fblike-single" href="http://www.facebook.com/plugins/like.php?href=<?php echo urlencode(URL::site('/extra/sprint', TRUE)) ?>&amp;layout=standard&amp;show_faces=false&amp;width=450&amp;action=like&amp;font&amp;colorscheme=light&amp;height=35"></a>
			</div>
			
			<div class="span11">
				<g:plusone annotation="inline" href="<?php echo URL::site('/extra/sprint', TRUE) ?>"></g:plusone>
			</div>
		</div>
	</div>
</div>