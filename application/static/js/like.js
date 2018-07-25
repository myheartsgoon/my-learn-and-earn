$(function(){
	$(document).one('click', '.like-review', function(e) {
		$(this).text('您已赞');
		var keyword = $(".like-content").attr('id');
		$.ajax({
            type:'GET',
            url:'/like_article',
            data:{'id': keyword},
            dataType:'json'
        });
	});
});