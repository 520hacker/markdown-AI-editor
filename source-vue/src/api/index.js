export const BASE_URL = "/api/ai";

export function post(url, params) {
  return fetch(`${BASE_URL}${url}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(params),
    mode: "cors",
  });
}

export function get(url) { 
  return fetch(`${BASE_URL}${url}`, {
    method: "GET",
    mode: "cors",
  });
}

export function fetchUserInfo() { 
  return fetch(`${BASE_URL}/user/currentUser`, {
    method: "GET",
    mode: "cors",
  });
}

export function loginUser(params) {
  return fetch(`${BASE_URL}/user/loginByPwd`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(params),
    mode: "cors",
  });
}

export function updateApiKey(params) {
  return fetch(`${BASE_URL}/user/updateOpenaiApiKey`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(params),
    mode: "cors",
  });
}

