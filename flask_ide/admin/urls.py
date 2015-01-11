#added line
from admin import admin
from .views import (
        AdminDashboardView,AdminPageView,
        AdminCMSListView,AdminListPageView,
        AdminDetailView,AdminEditView,
        AdminCodeView,AdminTemplateAjaxView,
        AdminListedView,AdminModalView,TestView,
        AdminFilesystemView,
)
from .save_views import (
        SaveStaticBlockView,SaveSuccessStaticBlockView,
        SaveErrorStaticBlockView,SaveSuccessAdminTabView,
        SaveErrorAdminTabView,
)

from .delete_views import (
        DeleteStaticBlockView
)

from .views2 import AdminTemplateView as AddAdminTemplateView
'''from .views import (AdminDashboardView,AdminPageView,AdminTemplateView,AdminBlockView,
                    AdminCMSListView,AdminListPageView,AdminDetailView,AdminEditView,
                    PageListView,AdminBlogView,AdminAddCategoryView,AdminAddBlogView)'''


routes = [
        ((admin),
            ('',AdminDashboardView.as_view('index')),
            ('/files',AdminFilesystemView.as_view('files')),
            ('/test',TestView.as_view('test')),
            ('/list/blocks',AdminCMSListView.as_view('blocks')),
            ('/list/blogs',AdminCMSListView.as_view('blogs')),
            ('/list/pages',AdminCMSListView.as_view('pages')),
            ('/list/users',AdminCMSListView.as_view('users')),
            ('/list/templates',AdminCMSListView.as_view('templates')),
            ('/list/buttons',AdminCMSListView.as_view('buttons')),
            ('/paged/template/<page_num>',AdminListPageView.as_view('page_template')),
            ('/paged/block/<page_num>',AdminListPageView.as_view('page_block')),
            ('/view/block/<name>',AdminDetailView.as_view('block_view')),
            ('/view/page/<slug>',AdminDetailView.as_view('page_view')),
            ('/view/template/<name>',AdminDetailView.as_view('template_view')),
            ('/edit/block/<item_id>',AdminEditView.as_view('edit_block')),
            ('/edit/page/<item_id>',AdminEditView.as_view('edit_page')),
            ('/edit/template/<item_id>',AdminEditView.as_view('edit_template')),
            ('/edit/page/content/<item_id>',AdminEditView.as_view('edit_page_content')),
            ('/edit/block/content/<item_id>',AdminEditView.as_view('edit_block_content')),
            #('/blogs',AdminBlogView.as_view('blog')),
            #('/blogs',AdminBlogListView.as_view('blog')),
            ('/blogs',AdminListedView.as_view('blog')),
            ('/list/code',AdminCodeView.as_view('list_code')),
            ('/edit/file/<path:file_path>',AdminCodeView.as_view('edit_file')),
            ('/get/template',AdminTemplateAjaxView.as_view('get_base')),
            ('/modal',AdminModalView.as_view('modal')),
            ('/save/success/static_block',SaveSuccessStaticBlockView.as_view('save_static_block_success')),
            ('/save/error/static_block',SaveErrorStaticBlockView.as_view('save_static_block_error')),
            ('/save/static_block',SaveStaticBlockView.as_view('save_static_block')),
            ('/delete/static_block',DeleteStaticBlockView.as_view('delete_static_block')),
            ('/save/success/admin_tab',SaveSuccessAdminTabView.as_view('save_admin_tab_success')),
            ('/save/error/admin_tab',SaveErrorAdminTabView.as_view('save_admin_tab_error')),
        )
    ]
