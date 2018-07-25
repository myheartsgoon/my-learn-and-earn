// delete article function
$(document).ready(function(){
    $("#checkAll").click(function () {
        $('input:checkbox').not(this).prop('checked', this.checked);
    });
    $("#delete").on("click", function() {
        var n = $("input:checked[id!='checkAll']").length;
        if(n === 0){
            alert('请至少选择一篇文章!');
        } else {
            if(confirm('确认删除选中的'+ n +'篇文章?')){
                var ids = $("input:checked[id!='checkAll']").map(function(){
                            return this.id;
                    }).get().join();
                var form = $('#action_form');
                $('#ids').val(ids);
                form.submit();
            }
        }
	});
});


// filter keyword function
$.fn.simpleContentSearch = function ( options ) {

    /**
     * Plugin Top Level Scope Variables
     *
     */

    var settings = {
        'active'    : 'active',
        'normal'    : 'normal',
        'searchList' : 'searchable tr',
        'searchItem' : 'td',
        'effect' : 'none' // fade, none
    };

    var base = this;
    var options = $.extend(settings, options);

    /**
     * The main searching method.
     * Using the input of the user, search for (base.text())
     */

    function startSearching(query)
    {
        $( '.' + settings.searchList ).each(function ()
        {
            $(this).children( settings.searchItem ).each(function ()
            {
                var elem = $(this);

                if (!elem.html().match(new RegExp('.*?' + query + '.*?', 'i'))) {

                    if( settings.effect == 'fade' ){
                        $(this).parent( '.' + settings.searchList ).fadeOut();
                    } else {
                        $(this).parent( '.' + settings.searchList ).hide();
                    }

                } else {

                    if( settings.effect == 'fade' ){
                        $(this).parent( '.' + settings.searchList ).fadeIn();
                    } else {
                        $(this).parent( '.' + settings.searchList ).show();
                    }

                    return false;
                }

                return;
            });
        });
    }

    return this.each(function() {

        //Keyup
        base.keyup(function ()
        {
            startSearching(base.val());
        });

        return this;

    });
}
$(document).ready(function(){
    $('.searchFilter').simpleContentSearch({
        'active' : 'searchBoxActive',
        'normal' : 'searchBoxNormal',
        'searchList' : 'searchable tr',
        'searchItem' : 'td'
    });
});




// show more or less function
$(document).ready(function() {
	var showChar = 30;
	var ellipsestext = "...";
	var moretext = "更多";
	var lesstext = "隐藏";
	$('.more').each(function() {
		var content = $(this).html();

		if(content.length > showChar) {

			var c = content.substr(0, showChar);
			var h = content.substr(showChar, content.length - showChar);

			var html = c + '<span class="moreellipses">' + ellipsestext+ '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';

			$(this).html(html);
		}

	});

	$(".morelink").click(function(){
		if($(this).hasClass("less")) {
			$(this).removeClass("less");
			$(this).html(moretext);
		} else {
			$(this).addClass("less");
			$(this).html(lesstext);
		}
		$(this).parent().prev().toggle();
		$(this).prev().toggle();
		return false;
	});
});