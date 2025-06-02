import { generalRequest } from "./genServ.ts";
import {
  type DataResponse,
  type LostItemResponse,
  type LostItemsResponse,
  type MessageResponse
} from "../models/lostItem.ts";

// 定义物品类型接口
export interface LostItemData {
  type: 'lost' | 'found';
  title: string;
  category: string;
  description: string;
  location: string;
  time: string;
  contact_type: 'phone' | 'wechat' | 'qq';
  contact_value?: string;
  hide_contact: boolean;
  status?: 'unclaimed' | 'claimed' | 'expired';
}

// 获取失物招领列表
export async function getLostItems(params?: {
  skip?: number;
  limit?: number;
  type?: 'lost' | 'found';
  category?: string;
  status?: string;
  q?: string;
}): Promise<LostItemsResponse> {
  const res = await generalRequest("/api/lost-items/", {
    method: 'GET',
    params
  });
  return res as LostItemsResponse;
}

// 获取我发布的失物招领列表
export async function getMyLostItems(params?: {
  skip?: number;
  limit?: number;
  status?: string;
}): Promise<LostItemsResponse> {
  const res = await generalRequest("/api/lost-items/my", {
    method: 'GET',
    params
  });
  return res as LostItemsResponse;
}

// 获取失物招领详情
export async function getLostItemDetail(id: string): Promise<LostItemResponse> {
  const res = await generalRequest(`/api/lost-items/${id}`, {
    method: 'GET'
  });
  return res as LostItemResponse;
}

// 创建失物招领信息
export async function createLostItem(data: LostItemData, images?: File[]): Promise<LostItemResponse> {
  // 使用FormData处理包含文件的请求
  const formData = new FormData();
  
  // 添加基本信息
  Object.entries(data).forEach(([key, value]) => {
    if (value !== undefined) {
      formData.append(key, value.toString());
    }
  });
  
  // 添加图片文件
  if (images && images.length > 0) {
    images.forEach(image => {
      formData.append('images', image);
    });
  }
  
  const res = await generalRequest("/api/lost-items/", {
    method: 'POST',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  return res as LostItemResponse;
}

// 更新失物招领信息
export async function updateLostItem(
  id: string, 
  data: LostItemData, 
  images?: File[], 
  deleteImages?: string[]
): Promise<LostItemResponse> {
  // 使用FormData处理包含文件的请求
  const formData = new FormData();
  
  // 添加基本信息
  Object.entries(data).forEach(([key, value]) => {
    if (value !== undefined) {
      formData.append(key, value.toString());
    }
  });
  
  // 添加图片文件
  if (images && images.length > 0) {
    images.forEach(image => {
      formData.append('images', image);
    });
  }
  
  // 添加要删除的图片URL
  if (deleteImages && deleteImages.length > 0) {
    deleteImages.forEach(imageUrl => {
      formData.append('delete_images', imageUrl);
    });
  }
  
  const res = await generalRequest(`/api/lost-items/${id}`, {
    method: 'PUT',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  return res as LostItemResponse;
}

// 更新物品状态
export async function updateItemStatus(
  id: string, 
  status: 'unclaimed' | 'claimed' | 'expired'
): Promise<LostItemResponse> {
  const res = await generalRequest(`/api/lost-items/${id}/status`, {
    method: 'PATCH',
    data: { status }
  });
  
  return res as LostItemResponse;
}

// 删除失物招领信息
export async function deleteLostItem(id: string): Promise<MessageResponse> {
  const res = await generalRequest(`/api/lost-items/${id}`, {
    method: 'DELETE'
  });
  
  return res as MessageResponse;
}