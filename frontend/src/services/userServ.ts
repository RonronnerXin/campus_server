import axios from 'axios'
import qs from 'qs';
import { generalRequest } from "./genServ";
import {
  type DataResponse,UserInfo
} from "../models/general";

export async function userLoginReq(username: string, password: string): Promise<any> {
  try {
    const res = await axios.post('/auth/users/login', qs.stringify({ // 转换为 username=xxx&password=yyy
      username: username,
      password: password
    }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
    //等待从服务器返还
    if (
      res.status == 200 &&
      res.data.access_token != null &&
      res.data.access_token != '' &&
      res.data.access_token != undefined
    ) {
      return res.data
    } else {
      throw new Error('未知错误');
    }
  } catch (error: any) {
    // 关键修改：提取后端返回的 detail 信息
    const errorMessage = error.response?.data?.detail || '登录失败，请检查网络连接';
    console.error('登录失败:', errorMessage);

    // 抛出携带具体错误信息的新异常
    throw new Error(`登录失败: ${errorMessage}`);
  }
}


export function getUser(): Promise<DataResponse> {
  return generalRequest("/auth/users", {
      method: 'GET'
  }) as Promise<DataResponse>;
}

// //通过用户ID获取用户信息
// export async function getUserInfo(id: number): Promise<DataResponse> {
//   const res = await generalRequest(`/auth/user/${id}`, {
//     method: "GET"
//   });
//   return res as DataResponse;
// }

export async function changeUserInfo(
  id: number,
  username: string,
  phone: string,
  email: string,
): Promise<DataResponse> {
  const res = await generalRequest("/api/user/changeUserInfo", 
    {
      method:"POST",
      data:{
        id: id,
        username:username,
        phone:phone,
        email:email
      }
    }
    );
  return res as DataResponse;
}

export async function changeUserAvatar(
  id: number,
  avatar:string
): Promise<DataResponse> {
  const res = await generalRequest("/api/user/changeUserAvatar", 
    {
      method:"POST",
      data:{
        id: id,
        avatar:avatar
      }
    }
    );
  return res as DataResponse;
}

export async function resetPassword(
  current_password: string,
  new_password: string
): Promise<DataResponse> {
  const res = await generalRequest("/auth/users/password", 
    {
      method: "POST",
      data: {
        current_password: current_password,
        new_password: new_password
      }
    }
  );
  return res as DataResponse;
}