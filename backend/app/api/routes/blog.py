import uuid
from typing import Any, List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Query
from sqlmodel import func, select, Session
from pydantic import parse_obj_as

from app.api.deps import CurrentUser, SessionDep
from app.models.blog_model import (
    BlogPost, BlogPostCreate, BlogPostPublic, BlogPostsPublic,
    Comment, CommentPublic, CommentsPublic,
    BlogCategory, BlogStatus, PostLike, CommentLike,
    Message, BlogImage
)
from app.models.user_model import User
from app.utils import upload_file_to_storage

router = APIRouter(prefix="/blog-posts", tags=["blog_posts"])


@router.get("/", response_model=BlogPostsPublic)
def read_blog_posts(
        session: SessionDep,
        current_user: CurrentUser,
        skip: int = 0,
        limit: int = 20,
        category: BlogCategory = None,
        featured: bool = None,
        tag: str = None,
        q: str = None,
) -> Any:
    """
    检索博客文章列表。
    支持筛选、分页和搜索。
    """
    # 构建基本查询
    query = select(BlogPost)
    count_query = select(func.count()).select_from(BlogPost)

    # 非管理员只能看到已发布的文章或自己的草稿
    if not current_user.is_superuser:
        query = query.where(
            (BlogPost.status == BlogStatus.PUBLISHED) |
            (BlogPost.author_id == current_user.id)
        )
        count_query = count_query.where(
            (BlogPost.status == BlogStatus.PUBLISHED) |
            (BlogPost.author_id == current_user.id)
        )

    # 应用筛选条件
    if category:
        query = query.where(BlogPost.category == category)
        count_query = count_query.where(BlogPost.category == category)

    if featured is not None:
        query = query.where(BlogPost.featured == featured)
        count_query = count_query.where(BlogPost.featured == featured)

    # 标签筛选
    if tag:
        # 使用JSON包含查询
        query = query.where(BlogPost.tags.contains([tag]))
        count_query = count_query.where(BlogPost.tags.contains([tag]))

    # 搜索功能
    if q:
        search_filter = (
                (BlogPost.title.contains(q)) |
                (BlogPost.summary.contains(q)) |
                (BlogPost.content.contains(q))
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    # 执行查询
    total_count = session.exec(count_query).one()
    posts = session.exec(
        query.order_by(BlogPost.published_at.desc(), BlogPost.created_at.desc())
        .offset(skip).limit(limit)
    ).all()

    # 计算总页数
    total_pages = (total_count + limit - 1) // limit if total_count > 0 else 1

    # 构建响应数据
    result_posts = []
    for post in posts:
        # 获取作者信息
        author_query = select(User).where(User.id == post.author_id)
        author = session.exec(author_query).first()

        # 检查当前用户是否点赞
        liked = False
        if current_user:
            like_query = select(PostLike).where(
                (PostLike.post_id == post.id) &
                (PostLike.user_id == current_user.id)
            )
            liked = session.exec(like_query).first() is not None
        # 获取物品的图片
        images_query = select(BlogImage.image_url).where(BlogImage.blog_id == post.id)
        image_urls = session.exec(images_query).all()
        print(image_urls)

        # 转换为公开模型
        post_dict = post.model_dump()
        post_dict["author_name"] = author.username if author else "Unknown"
        post_dict["author_avatar"] = author.avatar if author else None
        post_dict["images"] = image_urls
        post_dict["liked"] = liked
        result_posts.append(parse_obj_as(BlogPostPublic, post_dict))

    return BlogPostsPublic(data=result_posts, count=total_count, total_pages=total_pages)


@router.get("/my", response_model=BlogPostsPublic)
def read_my_blog_posts(
        session: SessionDep,
        current_user: CurrentUser,
        skip: int = 0,
        limit: int = 20,
        status: BlogStatus = None,
) -> Any:
    """
    获取当前用户发布的博客文章。
    """
    # 构建基本查询
    query = select(BlogPost).where(BlogPost.author_id == current_user.id)
    count_query = select(func.count()).select_from(BlogPost).where(BlogPost.author_id == current_user.id)

    # 应用状态筛选
    if status:
        query = query.where(BlogPost.status == status)
        count_query = count_query.where(BlogPost.status == status)

    # 执行查询
    total_count = session.exec(count_query).one()
    posts = session.exec(
        query.order_by(BlogPost.created_at.desc())
        .offset(skip).limit(limit)
    ).all()

    # 计算总页数
    total_pages = (total_count + limit - 1) // limit if total_count > 0 else 1

    # 构建响应数据
    result_posts = []
    for post in posts:
        # 获取作者信息
        author_query = select(User).where(User.id == post.author_id)
        author = session.exec(author_query).first()

        # 检查当前用户是否点赞
        liked = False
        if current_user:
            like_query = select(PostLike).where(
                (PostLike.post_id == post.id) &
                (PostLike.user_id == current_user.id)
            )
            liked = session.exec(like_query).first() is not None
        images_query = select(BlogImage.image_url).where(BlogImage.blog_id == post.id)
        image_urls = session.exec(images_query).all()

        comments_query = select(Comment.content).where(Comment.post_id == post.id)
        comments_content = session.exec(comments_query).all()

        # 转换为公开模型
        post_dict = post.model_dump()
        post_dict["author_name"] = author.username if author else "Unknown"
        post_dict["author_avatar"] = author.avatar if author else None
        post_dict["images"] = image_urls
        post_dict["comments"] = comments_content
        post_dict["liked"] = liked
        result_posts.append(parse_obj_as(BlogPostPublic, post_dict))

    return BlogPostsPublic(data=result_posts, count=total_count, total_pages=total_pages)


@router.get("/{id}", response_model=BlogPostPublic)
def read_blog_post(
        session: SessionDep,
        id: uuid.UUID,
        current_user: CurrentUser,
) -> Any:
    """
    通过ID获取博客文章详情。
    """
    post = session.get(BlogPost, id)
    if not post:
        raise HTTPException(status_code=404, detail="博客文章未找到")

    # 检查权限 - 草稿只有作者和管理员可以查看
    if post.status == BlogStatus.DRAFT and not current_user.is_superuser and post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权查看此文章")

    # 增加浏览次数（如果查看者不是文章作者）
    if post.author_id != current_user.id:
        post.views_count += 1
        session.add(post)
        session.commit()
        session.refresh(post)

    # 获取作者信息
    author_query = select(User).where(User.id == post.author_id)
    author = session.exec(author_query).first()

    # 检查当前用户是否点赞
    liked = False
    if current_user:
        like_query = select(PostLike).where(
            (PostLike.post_id == post.id) &
            (PostLike.user_id == current_user.id)
        )
        liked = session.exec(like_query).first() is not None

    # 转换为公开模型
    post_dict = post.model_dump()
    post_dict["author_name"] = author.username if author else "Unknown"
    post_dict["author_avatar"] = author.avatar if author else None
    post_dict["liked"] = liked

    return parse_obj_as(BlogPostPublic, post_dict)


@router.post("/", response_model=BlogPostPublic)
async def create_blog_post(
        session: SessionDep,
        current_user: CurrentUser,
        title: str = Form(...),
        category: BlogCategory = Form(...),
        summary: str = Form(...),
        content: str = Form(...),
        tags: List[str] = Form([]),
        allow_comments: bool = Form(True),
        featured: bool = Form(False),
        status: BlogStatus = Form(BlogStatus.DRAFT),
        images: List[UploadFile] = File(None),
) -> Any:
    """
    创建新的博客文章。
    支持封面图片上传。
    """
    # 处理封面图片上传

    # 创建博客文章记录
    post_data = {
        "title": title,
        "category": category,
        "summary": summary,
        "content": content,
        "tags": tags,
        "allow_comments": allow_comments,
        "featured": featured,
        "status": status,
        "author_id": current_user.id,
        "author_name": current_user.username,
    }

    # 如果状态为已发布，设置发布时间
    if status == BlogStatus.PUBLISHED:
        post_data["published_at"] = datetime.now()

    post = BlogPost(**post_data)
    session.add(post)
    session.commit()
    session.refresh(post)
    # 处理图片上传
    image_urls = []
    if images:
        for image in images:
            if image.content_type.startswith('image/'):
                contents = await image.read()
                if len(contents) > 3 * 1024 * 1024:  # 限制为3MB
                    continue
                await image.seek(0)
                image_url = await upload_file_to_storage(
                    file=image,
                    folder=f"blog/{post.id}",
                    filename=f"{uuid.uuid4()}.{image.filename.split('.')[-1]}"
                )
                blog_image = BlogImage(blog_id=post.id, image_url=image_url, created_at=datetime.now())
                session.add(blog_image)
                image_urls.append(image_url)

    session.commit()

    post.__dict__["images"] = image_urls
    post.__dict__["author_name"] = current_user.username
    post.__dict__["author_avatar"] = current_user.avatar

    return post  # 返回修改后的对象


@router.put("/{id}", response_model=BlogPostPublic)
async def update_blog_post(
        session: SessionDep,
        current_user: CurrentUser,
        id: uuid.UUID,
        title: str = Form(...),
        category: BlogCategory = Form(...),
        summary: str = Form(...),
        content: str = Form(...),
        tags: List[str] = Form([]),
        allow_comments: bool = Form(True),
        featured: bool = Form(False),
        status: BlogStatus = Form(...),
        images: Optional[UploadFile] = File(None),
        remove_cover: bool = Form(False),
) -> Any:
    """
    更新博客文章。
    支持更新封面图片。
    """
    # 获取文章
    post = session.get(BlogPost, id)
    if not post:
        raise HTTPException(status_code=404, detail="博客文章未找到")

    # 检查权限
    if not current_user.is_superuser and post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此文章")

    # 处理封面图片
    images_url = post.images
    if remove_cover:
        images_url = None
    elif images and images.content_type.startswith('image/'):
        contents = await images.read()
        if len(contents) <= 2 * 1024 * 1024:  # 限制为2MB
            await images.seek(0)
            images_url = await upload_file_to_storage(
                file=images,
                folder=f"blog-covers/{id}",
                filename=f"{uuid.uuid4()}.{images.filename.split('.')[-1]}"
            )

    # 检查发布状态变化
    was_draft = post.status == BlogStatus.DRAFT
    is_published = status == BlogStatus.PUBLISHED

    # 如果从草稿变为已发布，设置发布时间
    if was_draft and is_published:
        post.published_at = datetime.now()

    # 更新文章信息
    post.title = title
    post.category = category
    post.summary = summary
    post.content = content
    post.tags = tags
    post.allow_comments = allow_comments
    post.featured = featured
    post.status = status
    post.images = images_url
    post.updated_at = datetime.now()

    session.add(post)
    session.commit()
    session.refresh(post)

    # 获取作者信息
    author_query = select(User).where(User.id == post.author_id)
    author = session.exec(author_query).first()

    # 检查当前用户是否点赞
    liked = False
    if current_user:
        like_query = select(PostLike).where(
            (PostLike.post_id == post.id) &
            (PostLike.user_id == current_user.id)
        )
        liked = session.exec(like_query).first() is not None

    # 构造响应数据
    response_data = post.model_dump()
    response_data["author_name"] = author.username if author else "Unknown"
    response_data["author_avatar"] = author.avatar if author else None
    response_data["liked"] = liked

    return parse_obj_as(BlogPostPublic, response_data)


@router.delete("/{id}")
def delete_blog_post(
        session: SessionDep,
        current_user: CurrentUser,
        id: uuid.UUID,
) -> Message:
    """
    删除博客文章。
    """
    post = session.get(BlogPost, id)
    if not post:
        raise HTTPException(status_code=404, detail="博客文章未找到")

    # 检查权限
    if not current_user.is_superuser and post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此文章")

    # 删除相关评论和点赞
    session.exec(select(Comment).where(Comment.post_id == id)).delete()
    session.exec(select(PostLike).where(PostLike.post_id == id)).delete()

    # 删除文章记录
    session.delete(post)
    session.commit()

    return Message(message="博客文章已成功删除")


@router.post("/{id}/like", response_model=Message)
def like_blog_post(
        session: SessionDep,
        current_user: CurrentUser,
        id: uuid.UUID,
) -> Any:
    """
    点赞博客文章。
    """
    post = session.get(BlogPost, id)
    if not post:
        raise HTTPException(status_code=404, detail="博客文章未找到")

    # 检查是否已点赞
    existing_like = session.exec(
        select(PostLike).where(
            (PostLike.post_id == id) &
            (PostLike.user_id == current_user.id)
        )
    ).first()

    if existing_like:
        return Message(message="您已经点赞过此文章")

    # 创建点赞记录
    like = PostLike(post_id=id, user_id=current_user.id)
    session.add(like)

    # 更新文章点赞数
    post.likes_count += 1
    session.add(post)

    session.commit()

    return Message(message="点赞成功")


@router.delete("/{id}/like", response_model=Message)
def unlike_blog_post(
        session: SessionDep,
        current_user: CurrentUser,
        id: uuid.UUID,
) -> Any:
    """
    取消点赞博客文章。
    """
    post = session.get(BlogPost, id)
    if not post:
        raise HTTPException(status_code=404, detail="博客文章未找到")

    # 查找并删除点赞记录
    like = session.exec(
        select(PostLike).where(
            (PostLike.post_id == id) &
            (PostLike.user_id == current_user.id)
        )
    ).first()

    if not like:
        return Message(message="您尚未点赞此文章")

    session.delete(like)

    # 更新文章点赞数
    if post.likes_count > 0:
        post.likes_count -= 1
    session.add(post)

    session.commit()

    return Message(message="取消点赞成功")


@router.get("/{id}/comments", response_model=CommentsPublic)
def get_post_comments(
        session: SessionDep,
        current_user: CurrentUser,
        id: uuid.UUID,
        skip: int = 0,
        limit: int = 20,
) -> Any:
    """
    获取博客文章的评论。
    """
    post = session.get(BlogPost, id)
    if not post:
        raise HTTPException(status_code=404, detail="博客文章未找到")

    # 获取顶级评论（没有父评论的评论）
    query = select(Comment).where(
        (Comment.post_id == id) &
        (Comment.parent_id == None)
    )
    count_query = select(func.count()).select_from(Comment).where(
        (Comment.post_id == id) &
        (Comment.parent_id == None)
    )

    # 执行查询
    total_count = session.exec(count_query).one()
    comments = session.exec(
        query.order_by(Comment.created_at.desc())
        .offset(skip).limit(limit)
    ).all()

    # 计算总页数
    total_pages = (total_count + limit - 1) // limit if total_count > 0 else 1

    # 构建响应数据
    result_comments = []
    for comment in comments:
        # 获取用户信息
        user_query = select(User).where(User.id == comment.user_id)
        user = session.exec(user_query).first()

        # 检查当前用户是否点赞
        liked = False
        if current_user:
            like_query = select(CommentLike).where(
                (CommentLike.comment_id == comment.id) &
                (CommentLike.user_id == current_user.id)
            )
            liked = session.exec(like_query).first() is not None

        # 获取回复
        replies_query = select(Comment).where(Comment.parent_id == comment.id)
        replies = session.exec(replies_query).all()

        # 处理回复
        reply_list = []
        for reply in replies:
            reply_user_query = select(User).where(User.id == reply.user_id)
            reply_user = session.exec(reply_user_query).first()

            reply_liked = False
            if current_user:
                reply_like_query = select(CommentLike).where(
                    (CommentLike.comment_id == reply.id) &
                    (CommentLike.user_id == current_user.id)
                )
                reply_liked = session.exec(reply_like_query).first() is not None

            reply_dict = reply.model_dump()
            reply_dict["user_name"] = reply_user.username if reply_user else "Unknown"
            reply_dict["user_avatar"] = reply_user.avatar if reply_user else None
            reply_dict["liked"] = reply_liked
            reply_list.append(parse_obj_as(CommentPublic, reply_dict))

        # 转换为公开模型
        comment_dict = comment.model_dump()
        comment_dict["user_name"] = user.username if user else "Unknown"
        comment_dict["user_avatar"] = user.avatar if user else None
        comment_dict["liked"] = liked
        comment_dict["replies"] = reply_list
        result_comments.append(parse_obj_as(CommentPublic, comment_dict))

    return CommentsPublic(data=result_comments, count=total_count, total_pages=total_pages)


@router.post("/{id}/comments", response_model=CommentPublic)
def create_comment(
        session: SessionDep,
        current_user: CurrentUser,
        id: uuid.UUID,
        content: str = Form(...),
        parent_id: Optional[uuid.UUID] = Form(None),
) -> Any:
    """
    为博客文章添加评论或回复。
    """
    post = session.get(BlogPost, id)
    if not post:
        raise HTTPException(status_code=404, detail="博客文章未找到")

    # 检查文章是否允许评论
    if not post.allow_comments:
        raise HTTPException(status_code=403, detail="此文章不允许评论")

    # 如果是回复，检查父评论是否存在
    if parent_id:
        parent_comment = session.get(Comment, parent_id)
        if not parent_comment or parent_comment.post_id != id:
            raise HTTPException(status_code=404, detail="父评论不存在或不属于此文章")

    # 创建评论
    comment = Comment(
        post_id=id,
        user_id=current_user.id,
        parent_id=parent_id,
        content=content
    )
    session.add(comment)

    # 更新文章评论数
    post.comments_count += 1
    session.add(post)

    session.commit()
    session.refresh(comment)

    # 获取用户信息
    user_query = select(User).where(User.id == current_user.id)
    user = session.exec(user_query).first()

    # 构造响应数据
    response_data = comment.model_dump()
    response_data["user_name"] = user.username if user else "Unknown"
    response_data["user_avatar"] = user.avatar if user else None
    response_data["liked"] = False
    response_data["replies"] = []
    # if parent_id:
    #     parent_comment = session.get(Comment, parent_id)  # 已在前面校验过存在
    #     reply_user = session.get(User, parent_comment.user_id)
    #     response_data["reply_username"] = reply_user.username if reply_user else "Unknown"
    # else:
    #     response_data["reply_username"] = None

    return parse_obj_as(CommentPublic, response_data)


@router.post("/comments/{id}/like", response_model=Message)
def like_comment(
        session: SessionDep,
        current_user: CurrentUser,
        id: uuid.UUID,
) -> Any:
    """
    点赞评论。
    """
    comment = session.get(Comment, id)
    if not comment:
        raise HTTPException(status_code=404, detail="评论未找到")

    # 检查是否已点赞
    existing_like = session.exec(
        select(CommentLike).where(
            (CommentLike.comment_id == id) &
            (CommentLike.user_id == current_user.id)
        )
    ).first()

    if existing_like:
        return Message(message="您已经点赞过此评论")

    # 创建点赞记录
    like = CommentLike(comment_id=id, user_id=current_user.id)
    session.add(like)

    # 更新评论点赞数
    comment.likes_count += 1
    session.add(comment)

    session.commit()

    return Message(message="点赞成功")


@router.delete("/comments/{id}/like", response_model=Message)
def unlike_comment(
        session: SessionDep,
        current_user: CurrentUser,
        id: uuid.UUID,
) -> Any:
    """
    取消点赞评论。
    """
    comment = session.get(Comment, id)
    if not comment:
        raise HTTPException(status_code=404, detail="评论未找到")

    # 查找并删除点赞记录
    like = session.exec(
        select(CommentLike).where(
            (CommentLike.comment_id == id) &
            (CommentLike.user_id == current_user.id)
        )
    ).first()

    if not like:
        return Message(message="您尚未点赞此评论")

    session.delete(like)

    # 更新评论点赞数
    if comment.likes_count > 0:
        comment.likes_count -= 1
    session.add(comment)
    session.commit()

    return Message(message="取消点赞成功")