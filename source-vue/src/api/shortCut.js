
import { post } from './index'

export function fetchAddShortCut(params) {
  return new Promise((resolve, reject) => {
    post("/echo/shortcut/add", params).then(async (event) => {
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

export function fetchShortCutList() {
  return new Promise((resolve, reject) => {
    post("/echo/shortcut/list", {}).then(async (event) => {
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

export function fetchShortCutDetail(params) {
  return new Promise((resolve, reject) => {
    post("/echo/shortcut/detail", params).then(async (event) => {
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

export function fetchUpdateShortCut(params) {
  return new Promise((resolve, reject) => {
    post("/echo/shortcut/update", params).then(async (event) => {
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
