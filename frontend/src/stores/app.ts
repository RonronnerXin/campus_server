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
      id: 0,
      roles: "",
      password: "",
      icon: ""
    } as UserInfo
  }),
  actions: {
    async login(username: string, password: string): Promise<UserInfo> {
      const res = await userLoginReq(username, password);
      this.userInfo = {
        loggedIn: true,
        username: res.username,
        perName: res.perName,
        jwtToken: res.access_token,
        id: res.id,
        roles: res.roles,
        password: res.password,
        icon:"src/resource/"+res.icon
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
        id: 0,
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
