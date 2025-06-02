// models/general.ts

// 通用响应接口
export interface DataResponse {
  code: number;
  message: string;
  data?: any;
}

// 验证码响应
export interface ValidateCode {
  code: number;
  message: string;
  data: {
    id: string;
    image: string;
  };
}

// 失物招领物品接口
export interface LostItem {
  id: string;
  type: 'lost' | 'found';
  title: string;
  category: string;
  description: string;
  location: string;
  time: string;
  contact_type: 'phone' | 'wechat' | 'qq';
  contact_value?: string;
  hide_contact: boolean;
  status: 'unclaimed' | 'claimed' | 'expired';
  owner_id: string;
  created_at: string;
  updated_at: string;
  views_count: number;
  images: string[];
}

// 失物招领列表响应
export interface LostItemsResponse {
  code: number;
  message: string;
  data: {
    data: LostItem[];
    count: number;
    total_pages: number;
  };
}

// 单个失物招领响应
export interface LostItemResponse {
  code: number;
  message: string;
  data: LostItem;
}

// 消息响应
export interface MessageResponse {
  code: number;
  message: string;
}