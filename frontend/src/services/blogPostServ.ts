// services/blog.ts
import { generalRequest } from "./genServ";
import {
  type BlogCategory,
  type BlogStatus,
  type BlogPostsResponse,
  type BlogPostResponse,
  type CommentsResponse,
  type CommentResponse,
  type MessageResponse
} from "../models/blogpost";

// 博客创建/更新数据接口
export interface BlogPostData {
  title: string;
  category: BlogCategory;
  summary: string;
  content: string;
  tags: string[];
  allow_comments: boolean;
  featured: boolean;
  status: BlogStatus;
}

// 获取博客文章列表
export async function getBlogPosts(params?: {
  skip?: number;
  limit?: number;
  category?: BlogCategory;
  featured?: boolean;
  tag?: string;
  q?: string;
}): Promise<BlogPostsResponse> {
  const res = await generalRequest("/api/blog-posts/", {
    method: 'GET',
    params
  });
  return res as BlogPostsResponse;
}

// 获取我的博客文章列表
export async function getMyBlogPosts(params?: {
  skip?: number;
  limit?: number;
  status?: BlogStatus;
}): Promise<BlogPostsResponse> {
  const res = await generalRequest("/api/blog-posts/my", {
    method: 'GET',
    params
  });
  return res as BlogPostsResponse;
}

// 获取博客文章详情
export async function getBlogPostDetail(id: string): Promise<BlogPostResponse> {
  const res = await generalRequest(`/api/blog-posts/${id}`, {
    method: 'GET'
  });
  return res as BlogPostResponse;
}

// 创建博客文章
export async function createBlogPost(
  data: BlogPostData,
  images?: File[]
): Promise<BlogPostResponse> {
  const formData = new FormData();

  // 添加基本信息
  Object.entries(data).forEach(([key, value]) => {
    if (value !== undefined) {
      if (key === 'tags') {
        // 处理标签数组
        (value as string[]).forEach(tag => {
          formData.append('tags', tag);
        });
      } else {
        formData.append(key, value.toString());
      }
    }
  });

    // 添加图片文件
  if (images && images.length > 0) {
    images.forEach(image => {
      formData.append('images', image);
    });
  }
  
  const res = await generalRequest("/api/blog-posts/", {
    method: 'POST',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  return res as BlogPostResponse;
}

// 更新博客文章
export async function updateBlogPost(
  id: string,
  data: BlogPostData,
  coverImage?: File,
  removeCover?: boolean
): Promise<BlogPostResponse> {
  const formData = new FormData();
  
  // 添加基本信息
  Object.entries(data).forEach(([key, value]) => {
    if (value !== undefined) {
      if (key === 'tags') {
        // 处理标签数组
        (value as string[]).forEach(tag => {
          formData.append('tags', tag);
        });
      } else {
        formData.append(key, value.toString());
      }
    }
  });
  
  // 添加封面图片
  if (coverImage) {
    formData.append('cover_image', coverImage);
  }
  
  // 是否移除封面
  if (removeCover) {
    formData.append('remove_cover', 'true');
  }
  
  const res = await generalRequest(`/api/blog-posts/${id}`, {
    method: 'PUT',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  return res as BlogPostResponse;
}

// 删除博客文章
export async function deleteBlogPost(id: string): Promise<MessageResponse> {
  const res = await generalRequest(`/api/blog-posts/${id}`, {
    method: 'DELETE'
  });
  
  return res as MessageResponse;
}

// 点赞博客文章
export async function likeBlogPost(id: string): Promise<MessageResponse> {
  const res = await generalRequest(`/api/blog-posts/${id}/like`, {
    method: 'POST'
  });
  
  return res as MessageResponse;
}

// 取消点赞博客文章
export async function unlikeBlogPost(id: string): Promise<MessageResponse> {
  const res = await generalRequest(`/api/blog-posts/${id}/like`, {
    method: 'DELETE'
  });
  
  return res as MessageResponse;
}

// 获取文章评论列表
export async function getBlogComments(
  postId: string,
  params?: {
    skip?: number;
    limit?: number;
  }
): Promise<CommentsResponse> {
  const res = await generalRequest(`/api/blog-posts/${postId}/comments`, {
    method: 'GET',
    params
  });
  return res as CommentsResponse;
}

// 发表评论
export async function createComment(
  postId: string,
  content: string,
  parentId?: string
): Promise<CommentResponse> {
  const formData = new FormData();
  formData.append('content', content);
  if (parentId) {
    formData.append('parent_id', parentId);
  }
  
  const res = await generalRequest(`/api/blog-posts/${postId}/comments`, {
    method: 'POST',
    data: formData
  });
  
  return res as CommentResponse;
}

// 点赞评论
export async function likeComment(id: string): Promise<MessageResponse> {
  const res = await generalRequest(`/api/blog-posts/comments/${id}/like`, {
    method: 'POST'
  });
  
  return res as MessageResponse;
}

// 取消点赞评论
export async function unlikeComment(id: string): Promise<MessageResponse> {
  const res = await generalRequest(`/api/blog-posts/comments/${id}/like`, {
    method: 'DELETE'
  });
  
  return res as MessageResponse;
}