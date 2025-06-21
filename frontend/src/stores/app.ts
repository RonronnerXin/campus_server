// Utilities
import { PiniaPluginContext, defineStore } from "pinia";
import { userLoginReq } from '../services/userServ.ts';
import {  type UserInfo } from "../models/general";

export const useAppStore = defineStore("app", {
  state: () => ({
    usernameSave: "",
    passwordSave: "",
    remember: false,
    userInfo: {
      loggedIn: false,
      username: "",
      perName: "",
      jwtToken: "",
      id: "",
      roles: "",
      password: "",
      avatar: ""
    } as UserInfo
  }),
  actions: {
    async login(username: string, password: string): Promise<UserInfo> {
      const res = await userLoginReq(username, password);
      console.log("登录结果：", res);
      this.userInfo = {
        loggedIn: true,
        username: res.username,
        perName: res.perName,
        jwtToken: res.access_token,
        id: res.user_id,
        roles: res.roles,
        password: res.password,
        avatar:res.avatar
      };
      return this.userInfo;;
    },
    logout() {
      this.userInfo = {
        loggedIn: false,
        username: "",
        perName: "",
        jwtToken: "",
        roles: "",
        id: "",
        password: "",
        icon:""
      };
    },
    setIcon(icon:string){
      this.userInfo.icon=icon;
    },
    saveAccount(username: string, password: string) {
      this.usernameSave = username;
      this.passwordSave = password;
      this.remember = true;
    },
    removeAccount() {
      this.usernameSave = "";
      this.passwordSave = "";
      this.remember = false;
    },
  },
  persist: {
    storage: localStorage,
  },
});
