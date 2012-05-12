<div class="row">
	<div class="span1">
		<img src="<?php echo $asset->asset_url('/media/images/box-64x64.gif') ?>" alt="tools" />
	</div>
	
	<div class="about-info span11">
		<div class="row">
	
			<div class="span11">
				<h2 class="fancy"><a href="<?php echo URL::site('/extra/tools/urlencode', TRUE) ?>">URL Encoder/Decoder</a></h2>
			</div>
	
			<div class="project-info span11">
				<div class="row">
					<div class="span11">
						<h3 class="thin">Encoding/decoding URL parameter values</h3>
						<p>Good for encoding/decoding query parameter values.</p>
					</div>
					<div class="span11">
						<div class="row">
							<div id="encode-w" class="span5">
								<div class="row">
									<div class="span5">
										<textarea class="span5" name="encode-uricomp" id="encode-uricomp" rows="5" cols="30"></textarea>
									</div>
									<div class="span5">
										<a href="javascript:void(0);" id="encode-uricomp-btn" class="btn btn-primary">Encode</a>
									</div>
								</div>
							</div>
							<div id="decode-w" class="span5">
								<div class="row">
									<div class="span5">
										<textarea class="span5" name="decode-uricomp" id="decode-uricomp" rows="5" cols="30"></textarea>
									</div>
									<div class="span5">
										<a href="javascript:void(0);" id="decode-uricomp-btn" class="btn btn-primary">Decode</a>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			
			<div class="project-info span11">
				<div class="row">
					<div class="span11">
						<h3 class="thin push-down-3">Encoding/decoding URLs</h3>
						<p>Good for encoding/decoding URLs as it preserves the actual URL.</p>
					</div>
					<div class="span11">
						<div class="row">
							<div id="encode-w" class="span5">
								<div class="row">
									<div class="span5">
										<textarea class="span5" name="encode-uri" id="encode-uri" rows="5" cols="30"></textarea>
									</div>
									<div class="span5">
										<a href="javascript:void(0);" id="encode-uri-btn" class="btn btn-primary">Encode</a>
									</div>
								</div>
							</div>
							<div id="decode-w" class="span5">
								<div class="row">
									<div class="span5">
										<textarea class="span5" name="decode-uricomp" id="decode-uri" rows="5" cols="30"></textarea>
									</div>
									<div class="span5">
										<a href="javascript:void(0);" id="decode-uri-btn" class="btn btn-primary">Decode</a>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			
			<div class="span11">
				<p class="push-down-3">For comments and suggestions, <a href="http://blog.lysender.com/2012/03/just-another-url-encoderdecoder/">see the blog post</a>. Enjoy and share.</p>
			</div>
		
			<div class="span11">
				<a class="fblike-single" href="http://www.facebook.com/plugins/like.php?href=<?php echo urlencode(URL::site('/extra/tools/urlencode', TRUE)) ?>&amp;layout=standard&amp;show_faces=false&amp;width=450&amp;action=like&amp;font&amp;colorscheme=light&amp;height=35"></a>
			</div>
			
			<div class="span11">
				<g:plusone annotation="inline" href="<?php echo URL::site('/extra/tools/urlencode', TRUE) ?>"></g:plusone>
			</div>
		</div><!-- row -->
	</div><!-- span11 -->
</div><!-- span12 -->