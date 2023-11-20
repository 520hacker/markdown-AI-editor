import { post, BASE_URL } from './index'

export function queryChatList(params) {
  return new Promise((resolve, reject) => {
    post("/echo/openai/chatList", params).then(async (event) => {
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

export function queryChatContentList(params) {
  return new Promise((resolve, reject) => {
    post("/echo/openai/chatContentList", params).then(async (event) => {
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

export function queryTextChatCompletion(params) {
  return new Promise((resolve, reject) => {
    post("/echo/openai/chatTextCompletion", params).then(async (event) => {
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


export async function* makeTextFileLineIterator(url, params) {
  const utf8Decoder = new TextDecoder("utf-8");
  let response = await fetch(`${BASE_URL}${url}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(params),
    mode: "cors",
  });
  let reader = response.body.getReader();
  let { value: chunk, done: readerDone } = await reader.read();
  chunk = chunk ? utf8Decoder.decode(chunk, { stream: true }) : "";

  let re = /\r\n|\n|\r/gm;
  let startIndex = 0;

  for (; ;) {
    let result = re.exec(chunk);
    if (!result) {
      if (readerDone) {
        break;
      }
      let remainder = chunk.substr(startIndex);
      ({ value: chunk, done: readerDone } = await reader.read());
      chunk =
        remainder + (chunk ? utf8Decoder.decode(chunk, { stream: true }) : "");
      startIndex = re.lastIndex = 0;
      continue;
    }
    yield chunk.substring(startIndex, result.index);
    startIndex = re.lastIndex;
  }
  if (startIndex < chunk.length) {
    // last line didn't end in a newline char
    yield chunk.substr(startIndex);
  }
}