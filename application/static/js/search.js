$(document).ready(function(){
    var keyword = $("#keyword").text();
    var search_text = '<h3>搜索完成, 以下是所有包含 "<a id="keyword" class="uk-link-reset uk-text-bold">' + keyword + '</a>" 的文章</h3>'
    $.ajax({
        type:'GET',
        url:'/search',
        data:{'keyword': keyword},
        dataType:'html',
        success:function(html){
        var text = search_text
            $("h3").html(text);
            $("#container").html(html);
        }
    });
});