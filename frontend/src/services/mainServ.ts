import { generalRequest } from "./genServ.ts";
import {
  type DataResponse,
  type ValidateCode,
} from "../models/general";

// 获取图片验证码后台数据请求方法
export async function getValidateCode(): Promise<ValidateCode> {
  const res = await generalRequest("/api/users/validateCode", {
    method: 'GET'
  });
  return res as ValidateCode;
}
//后台检验图片验证码数据请求方法
export function testValidateInfo(data: Object): Promise<DataResponse> {
  const res = generalRequest("/api/users/validateCode", {
    method: 'POST', data
  });
  return res as Promise<DataResponse>;
}

//后台检验邮箱验证码数据请求方法
export function testEmailValidateInfo(data: Object): Promise<DataResponse> {
  const res = generalRequest("/api/users/emailCodeVerification", {
    method: 'POST', data
  });
  return res as Promise<DataResponse>;
}
//获取邮箱验证码后台数据请求方法
export async function getEmailCode(data: Object): Promise<DataResponse> {
  const res = await generalRequest("/api/users/emailCode", {
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
  const res = await generalRequest("/api/resetPassWord", {
    method: 'POST', data
  });
  return res as Promise<DataResponse>;
}
//用户注册后台数据请求方法
export async function registerUser(data: Object) {
  const res = await generalRequest("/api/auth/register", {
    method: 'POST', data
  });
  return res as Promise<DataResponse>;
}

