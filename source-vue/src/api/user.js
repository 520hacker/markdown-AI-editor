import { post, get } from './index'

export function fetchUserInfo() {
  return new Promise((resolve, reject) => {
    get("/user/currentUser", {}).then(async (event) => {
      event.json().then(response => {
        if (!response.status) {
          resolve(response.data);
        } else {
          reject(response);
        }
      });
    });
  });
}

export function fetchLogin(params) {
  return new Promise((resolve, reject) => {
    post("/user/loginByPwd", params).then(async (event) => {
      event.json().then(response => {
        if (!response.status) {
          resolve(response.data);
        } else {
          reject(response);
        }
      });
    });
  });
}

export function fetchRegister(params) {
  return new Promise((resolve, reject) => {
    post("/user/register", params).then(async (event) => {
      event.json().then(response => {
        if (!response.status) {
          resolve(response.data);
        } else {
          reject(response);
        }
      });
    });
  });
}

export function fetchUpdateUser(params) {
  return new Promise((resolve, reject) => {
    post("/user/update", params).then(async (event) => {
      event.json().then(response => {
        if (!response.status) {
          resolve(response.data);
        } else {
          reject(response);
        }
      });
    });
  });
}

export function fetchSendSms(params) {
  return new Promise((resolve, reject) => {
    post("/user/sendSms", params).then(async (event) => {
      event.json().then(response => {
        if (!response.status) {
          resolve(response.data);
        } else {
          reject(response);
        }
      });
    });
  });
}

export function queryAppVersion(params) {
  return new Promise((resolve, reject) => {
    post("/echo/checkVersion", params).then(async (event) => {
      event.json().then(response => {
        if (!response.status) {
          resolve(response.data);
        } else {
          reject(response);
        }
      });
    });
  });
} 

export function userLogout() {
  return new Promise((resolve, reject) => {
    post("/user/logout", {}).then(async (event) => {
      event.json().then(response => {
        if (!response.status) {
          resolve(response.data);
        } else {
          reject(response);
        }
      });
    });
  });
} 


export function updateOpenaiApiKey(params) {
  return new Promise((resolve, reject) => {
    post("/user/updateOpenaiApiKey", params).then(async (event) => {
      event.json().then(response => {
        if (!response.status) {
          resolve(response.data);
        } else {
          reject(response);
        }
      });
    });
  });
} 