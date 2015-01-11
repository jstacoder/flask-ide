save_static_block = function(data) {
    var name, content, block_id;
    name = data.name;
    content = data.content;
    block_id = data.block_id;
    if (name && content && block_id) {
        var tmp = $.getJSON(
            SCRIPT_ROOT + 'admin/save/static_block',data,function(data){
                if (data.success) {
            window.location = SCRIPT_ROOT + 'admin/save/success/static_block';
        } else {
            window.location = SCRIPT_ROOT + 'admin/save/error/static_block';
            };
        });
    }
}

save_admin_tab = function(data) {
    var name,content,tab_id,tab_title;
    name = data.name;
    content = data.content;
    tab_id = data.tab_id;
    tab_title = data.tab_title;
    if (name && tab_id && tab_title && content) {
        $.getJSON(
            SCRIPT_ROOT + 'admin/admin_tab',data).success(function(){
                    window.location = SCRIPT_ROOT + 'admin/save/success/admin_tab';
            }).error(function(){
                    window.location = SCRIPT_ROOT + 'admin/save/error/admin_tab';
        });
    }
}


$("body#admin_add_static_block button[type='submit']").click(function(e){
    e.preventDefault();
    //var t = editable_cke_1.valueOf()['$'];
    //var t = '';

    var data = {
        'content':t, //$("textarea").ckeditor().val(),
        'name':$("input#name").val(),
        'block_id':$("input#block_id").val(),
    };
    save_static_block(data);
});
    
$("body#admin_add_tab button[type='submit']").click(function(e){
    e.preventDefault();
    var t = editor.getSession().getValue();
    //var t = CKEDITOR.instances.content.getData();
    var data = {
        'content':t,
        'name':$("input#name").val(),
        'tab_id':$("input#tab_id").val(),
        'tab_title':$("input#tab_title").val(),
    };
    save_admin_tab(data);
});
