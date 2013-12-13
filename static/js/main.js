var SHRINK = SHRINK || {};

SHRINK = (function(){

	

	var init = function(){
		console.log("page loaded");

		// parseLyrics();
		evtHandler();
	};


	//Event Handler
	function evtHandler(){

		jQuery('#list-form').on("click", ".btn-addmore", function(){
			event.preventDefault();


			inputFields = '<li class="listitem"><input type="text" id="field-link-long" placeholder="longurl" pattern="^[a-zA-Z0-9_-.]*$" name="l" required><input type="text" id="field-link-short" placeholder="shorturl" pattern="^[a-zA-Z0-9_-.]*$" name="s" required><input type="text" id="field-link-bundle" list="sbundle" name="b" placeholder="bundle" ><datalist id="sbundle"><option value="bundlename1"></option><option value="bundlename2"></option> <option value="bundlename3"></option></datalist><button class="icon-entypo btn-addmore" title="add more links">&plus;</button></li>';

            jQuery('#list-form').append(inputFields);
		});


		jQuery('#form-shrink').submit(function(event){
			event.preventDefault();

			lurl = jQuery('#field-link-long').val();


			// regex reference link:
			// http://blog.mattheworiordan.com/post/13174566389/url-regular-expression-for-links-with-or-without-the

			var re = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[.\!\/\\w]*))?)/;

			console.log(lurl);

			if (re.test(lurl)){
				jQuery(this).unbind('submit').submit();
			}else{
				alert("long url not in correct format");
			}

		});



	}





	return {
		'init' : init
	};
})();


jQuery(document).ready(function(){
	SHRINK.init();
});