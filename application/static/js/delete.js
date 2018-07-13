$(document).ready(function(){
    $("#checkAll").click(function () {
        $('input:checkbox').not(this).prop('checked', this.checked);
    });
    $("#delete").on("click", function() {
        var n = $("input:checked").length;
        if(n === 0){
            alert('请至少选择一篇文章!');
        } else {
            if(confirm('确认删除选中的文章?')){
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