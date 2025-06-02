// models/blog.ts

// 博客分类枚举
export type BlogCategory = 'tech' | 'life' | 'study' | 'travel' | 'other';

// 博客状态枚举
export type BlogStatus = 'draft' | 'published';

// 博客文章接口
export interface BlogPost {
  id: string;
  title: string;
  category: BlogCategory;
  summary: string;
  content: string;
  cover_image?: string;
  tags: string[];
  allow_comments: boolean;
  featured: boolean;
  status: BlogStatus;
  author_id: string;
  author_name: string;
  author_avatar?: string;
  created_at: string;
  updated_at: string;
  published_at?: string;
  views_count: number;
  likes_count: number;
  comments_count: number;
  liked: boolean;
}

// 评论接口
export interface Comment {
  id: string;
  post_id: string;
  user_id: string;
  user_name: string;
  user_avatar?: string;
  parent_id?: string;
  content: string;
  created_at: string;
  updated_at: string;
  likes_count: number;
  liked: boolean;
  replies: Comment[];
}

// 博客列表响应
export interface BlogPostsResponse {
  code: number;
  message: string;
  data: {
    data: BlogPost[];
    count: number;
    total_pages: number;
  };
}

// 单个博客响应
export interface BlogPostResponse {
  code: number;
  message: string;
  data: BlogPost;
}

// 评论列表响应
export interface CommentsResponse {
  code: number;
  message: string;
  data: {
    data: Comment[];
    count: number;
    total_pages: number;
  };
}

// 评论响应
export interface CommentResponse {
  code: number;
  message: string;
  data: Comment;
}

// 消息响应
export interface MessageResponse {
  code: number;
  message: string;
}

