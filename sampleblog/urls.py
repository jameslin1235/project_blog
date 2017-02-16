from django.conf.urls import url
from . import views
from django.conf import settings



app_name = 'sampleblog'
urlpatterns = [
    # url(r'^blog/test/$',views.test,name='test'),
    url(r'^blog/$',views.post_list,name='post_list'),

    url(r'^blog/post/like/$',views.post_like,name='post_like'),
    url(r'^blog/post/dislike/$',views.post_dislike,name='post_dislike'),
    url(r'^blog/post/(?P<post_slug>.*)/$',views.post_details,name='post_details'),
    url(r'^blog/comment/like/$',views.comment_like,name='comment_like'),
    url(r'^blog/comment/dislike/$',views.comment_dislike,name='comment_dislike'),
    url(r'^blog/category/(?P<category_slug>.*)/$',views.posts_by_category,name='posts_by_category'),
    url(r'^blog/category/$',views.category,name='category'),
    url(r'^blog/user/(?P<user>.*)/$',views.posts_by_user,name='posts_by_user'),


    url(r'^blog/register/$',views.register,name='register'),
    url(r'^blog/register/success/$',views.register_success,name='register_success'),


    url(r'^blog/dashboard/$',views.dashboard,name='dashboard'),
    url(r'^blog/dashboard/posts/$',views.dashboard_posts,name='dashboard_posts'),
    # url(r'^blog/dashboard/posts/add$',views.dashboard_posts_add,name='dashboard_posts_add'),
    url(r'^blog/dashboard/posts/(?P<post_slug>.*)/edit/$',views.dashboard_posts_edit,name='dashboard_posts_edit'),
    url(r'^blog/dashboard/posts/(?P<post_slug>.*)/delete/$',views.dashboard_posts_delete,name='dashboard_posts_delete'),


    url(r'^blog/dashboard/drafts/$',views.dashboard_drafts,name='dashboard_drafts'),
    url(r'^blog/dashboard/draft/(?P<draft_slug>.*)/$',views.dashboard_draft_details,name='dashboard_draft_details'),
    url(r'^blog/dashboard/drafts/add$',views.dashboard_drafts_add,name='dashboard_drafts_add'),
    url(r'^blog/dashboard/drafts/(?P<draft_slug>.*)/edit/$',views.dashboard_drafts_edit,name='dashboard_drafts_edit'),
    url(r'^blog/dashboard/drafts/(?P<draft_slug>.*)/delete/$',views.dashboard_drafts_delete,name='dashboard_drafts_delete'),
    url(r'^blog/dashboard/drafts/(?P<draft_slug>.*)/publish/$',views.dashboard_drafts_publish,name='dashboard_drafts_publish'),
    url(r'^blog/dashboard/drafts/category/(?P<category_slug>.*)/$',views.dashboard_drafts_by_category,name='dashboard_drafts_by_category'),
    url(r'^blog/dashboard/drafts/user/(?P<user>.*)/$',views.dashboard_drafts_by_user,name='dashboard_drafts_by_user'),




    url(r'^blog/dashboard/comments/$',views.dashboard_comments,name='dashboard_comments'),
    url(r'^blog/dashboard/comments/(?P<comment_slug>.*)/edit/$',views.dashboard_comments_edit,name='dashboard_comments_edit'),
    url(r'^blog/dashboard/comments/(?P<comment_slug>.*)/delete/$',views.dashboard_comments_delete,name='dashboard_comments_delete'),


    url(r'^blog/dashboard/profile/$',views.dashboard_profile,name='dashboard_profile'),
    url(r'^blog/dashboard/profile/add/$',views.dashboard_profile_add,name='dashboard_profile_add'),
    url(r'^blog/dashboard/profile/edit/$',views.dashboard_profile_edit,name='dashboard_profile_edit'),
    url(r'^blog/dashboard/profile/delete/$',views.dashboard_profile_delete,name='dashboard_profile_delete'),






]
