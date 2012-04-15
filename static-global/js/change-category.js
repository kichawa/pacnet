var packages = new Array();

// AJAX with CSRF
jQuery(document).ajaxSend(function(event, xhr, settings) {
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	function sameOrigin(url) {
		// url could be relative or scheme relative or absolute
		var host = document.location.host; // host + port
		var protocol = document.location.protocol;
		var sr_origin = '//' + host;
		var origin = protocol + sr_origin;
		// Allow absolute or scheme relative URLs to same origin
		return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
			(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
			// or any other URL that isn't scheme relative or absolute i.e relative.
			!(/^(\/\/|http:|https:).*/.test(url));
	}
	function safeMethod(method) {
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	}
});

(function($) {
	$.fn.shiftClick = function() {
		var lastSelected;
		var checkBoxes = $(this);

		this.each(function() {
			$(this).click(function(ev) {
				if (ev.shiftKey) {
					var last = checkBoxes.index(lastSelected);
					var first = checkBoxes.index(this);

					var start = Math.min(first, last);
					var end = Math.max(first, last);

					var chk = lastSelected.checked;
					var first_element = true;
					for (var i = start; i < end; i++) {
						if(first_element) {
							first_element = false;
						} else {
							$(checkBoxes[i]).click();
						}
					}
				} else {
					lastSelected = this;
				}
			})
		});
	};
})(jQuery);

$(document).ready(function() {
	
	// switch to edit mode
	$("#change_category a").click(function(){
		if ( $(".hide").css('display') == "none" ) {
			$('#packages input').shiftClick();
			$(".hide").show();
		} else {
			$(".hide").hide();
		}
	});
	
	// category filter
	$("#category-filter").keyup(function(){
		var term = $(this).val().toLowerCase();
		if(term != '') {
			$('.modal-body table td').each(function(){
				category = $(this).text().toLowerCase();
				if(category.search(term) == -1) {
					$(this).parent().fadeOut('slow');
				} else {
					if($(this).parent().css('display') == "none") {
						$(this).parent().fadeIn('slow');
					}
				}
			});
		} else {
			$('.modal-body table tbody tr').fadeIn('slow');
		}
	});
	
	// modal window trigger
	$('.change-window-trigger').click(function(){
		if(!$(this).hasClass('disabled')) {
			$('#select-category').modal();
			$('#category-filter').focus();
		}
		return false;
	});
	
	// activing modal trigger button
	$("#packages input").change(function(){
		
		id = $(this).data('id');
		
		if($(this).is(':checked')) {
			$(this).parents('tr').addClass('selected');
			packages.push(id);
		} else {
			$(this).parents('tr').removeClass('selected');
			packages.splice( $.inArray(id, packages), 1 );
		}
		
		if($("#packages input:checked").size() > 0) {
			if($('.form-actions input').hasClass('disabled')) {
				$('.form-actions input').removeClass('disabled');
			}
		} else {
			if(!$('.form-actions input').hasClass('disabled')) {
				$('.form-actions input').addClass('disabled');
			}
		}
		
		return false;
	});
	
	// changing category
	$('.modal-body table a').click(function(){
		$("#select-category .modal-body table").hide().siblings('.alert').show();
		category = $(this).data('id');
		$.post(change_category_url, { category: category, packages: packages }, function(data) {
			var response = jQuery.parseJSON(data);
			if (response['0'].status == "ok") {
				$("#packages input:checked").each(function(){
					$(this).parents('tr').fadeOut('slow', function() { 
						$(this).remove(); 
					});
				});
				packages = [];
				$("#select-category .modal-body .alert").hide().siblings('table').show();
				$('#select-category').modal('hide');
				$('.change-window-trigger').addClass('disabled');
			} else {
				alert('error');
			}
		});
		return false;
	});
});
