import axios, { type RawAxiosRequestHeaders } from "axios";
import { useAppStore } from "../stores/app";
//一般数据请求函数，参数为url后台接口映射全路径，和data 为传递后台的数据，返回值为服务器返回的data
export async function generalRequest(
  url: string,
  config: {
    method: 'GET' | 'POST' | 'PUT' | 'DELETE' |'PATCH'// 明确支持的方法类型
    data?: any // 请求体数据（POST/PUT使用）
    params?: any // URL参数（GET使用）
    headers?: RawAxiosRequestHeaders // 请求头
  }
): Promise<any> {
  const response = await axios({
    url,
    method: config.method,
    headers: getAuthHeader(),
    params: config.method === 'GET' ? config.params : undefined, // GET用params
    data: config.method !== 'GET' ? config.data : undefined // 非GET用data
  });

  if (response.status !== 200) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.data;
}
//文件数据上传服务器函数，参数为url后台接口映射全路径，和data 为传递后台的数据（包括文件数据），返回值为服务器返回的data
export async function uploadRequest(
  url: string,
  data: any | null
): Promise<any> {
  const res = await axios.post(url, data, {
    headers: getAuthHeaderFile(),
  });
  if (res.status != 200) {
    console.log("Error: " + res.status);
    return;
  }
  return res.data;
}
//获取数据请求Head信息，这个主要包括了用户的jwtToken信息
export function getAuthHeader(): any {
  return {
    Authorization: "Bearer " + useAppStore().userInfo.jwtToken,
  };
}
//获取文件上传请求Head信息，这个主要包括了用户的jwtToken信息和文件上传的Content-Type信息
export function getAuthHeaderFile(): RawAxiosRequestHeaders {
  return {
    Authorization: "Bearer " + useAppStore().userInfo.jwtToken,
    "Content-Type": "multipart/form-data",
  };
}
//文件下载函数，参数为url后台接口映射全路径，和label 为下载文件的名称，和data 为传递后台的数据，返回值为服务器返回的data
export async function downloadPost(url: string, label: string, data: any) {
  const requestOptions = {
    method: "POST",
    headers: {
      "content-type": "application/json",
      Authorization: "Bearer " + useAppStore().userInfo.jwtToken,
    },
    body: JSON.stringify({
      data: data,
    }),
  };
  const res = await fetch(url, requestOptions)
    .then(async (response) => {
      const blob = await response.blob();

      // check for error response
      if (!response.ok) {
        // get error message from body or default to response status
        const error = response.status;
        return Promise.reject(error);
      }
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = label;
      link.click();
      URL.revokeObjectURL(link.href);
      return Promise.resolve(response.status);
    })
    .catch((error) => {
      console.error("There was an error!", error);
    });
  return res;
}

// 获取 token
const getTokenFromCookie = () => {
  const match = document.cookie.match(/authToken=([^;]*)/);
  return match ? match[1] : null;
};

// 在请求拦截器中添加 token
axios.interceptors.request.use(config => {
  const token = getTokenFromCookie();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
