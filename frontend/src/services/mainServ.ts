import { generalRequest } from "./genServ.ts";
import {
  type DataResponse,
  type ValidateCode,
} from "../models/general";

// 获取图片验证码后台数据请求方法
export async function getValidateCode(): Promise<ValidateCode> {
  const res = await generalRequest("/auth/users/getValidateCode", {
    method: 'GET'
  });
  return res as ValidateCode;
}
//后台检验图片验证码数据请求方法
export function testValidateInfo(data: Object): Promise<DataResponse> {
  const res = generalRequest("/auth/users/testValidateInfo", {
    method: 'POST', data
  });
  return res as Promise<DataResponse>;
}

//后台检验邮箱验证码数据请求方法
export function testEmailValidateInfo(data: Object): Promise<DataResponse> {
  const res = generalRequest("/auth/users/verifyEmailCode", {
    method: 'POST', data
  });
  return res as Promise<DataResponse>;
}
//获取邮箱验证码后台数据请求方法
export async function getEmailCode(data: Object): Promise<DataResponse> {
  const res = await generalRequest("/auth/users/getEmailCode", {
    method: 'POST', data
  });
  return res as Promise<DataResponse>;
}

export async function readItem(): Promise<DataResponse> {
  const res = await generalRequest("/api/debates/", {
    params: {
      skip: 0,
      limit: 20
    },
    method: 'GET'
  });
  return res as Promise<DataResponse>;
}

//重置密码后台数据请求方法
export async function resetPassWord(data: Object) {
  const res = await generalRequest("/auth/resetPassWord", {
    method: 'POST', data
  });
  return res as Promise<DataResponse>;
}
//用户注册后台数据请求方法
export async function registerUser(data: Object) {
  const res = await generalRequest("/auth/users/register", {
    method: 'POST', data
  });
  return res as Promise<DataResponse>;
}

