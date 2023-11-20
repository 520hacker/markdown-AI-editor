// 跳转新页面
const { pathname } = new URL(location);
const key = pathname.split('/')[1];
if (!key || key == '') {
    window.location.href = "/new"
}

// 获取元素
const popupFrame = document.getElementById('popup-frame');
const qrCodeFrame = document.getElementById('qrcode-frame');
const qrCodeUrl = document.getElementById('qrcode-url');
qrCodeUrl.innerHTML = window.location.href;

// 初始化
document.addEventListener('DOMContentLoaded', function () {
    if (typeof vditorScript !== 'undefined') {
        vditorScript()
    }
})

updatePageTitle = (content) => { 
    // 将Markdown内容按行分割成数组
    var lines = content.split('\n'); 
    // 遍历数组，找到第一个以 '#' 开头的行
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].trim();
      if (line.replace(' ','') != '') {
        // 提取H1标题内容（去除 '#' 和空格）
        var title = line.replace(/^#+\s*/, ''); 
        title = title.replace('#','');
        // 更新当前页面的标题
        document.title = "记-" +  title.replace(' ','');  
        break;
      }
    }
  }


vditorScript = () => {
    new Vue({
        el: '#app',
        data: {
            history_id: 0,
            content: '',
            contentEditor: '',
        },
        mounted() {
            var newIcon = {
                hotkey: '⇧⌘n',
                name: 'new',
                tipPosition: 's',
                tip: '新开文档',
                className: 'right',
                icon: '<svg t="1691674362684" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2362" width="32" height="32"><path d="M323.968 0.704L127.552 195.008 128.448 1024h768V0L323.968 0.704z m509.76 960.64H192.448V256.96h190.976V64h450.304v897.856-0.512zM318.656 193.984H215.424L318.592 88.96l0.064 105.024z" p-id="2363"></path></svg>',
                click() {
                    window.open("/new")
                },
            };
            var saveIcon = {
                hotkey: '⇧⌘s',
                name: 'new',
                tipPosition: 's',
                tip: '保存',
                className: 'right',
                icon: '<svg t="1691719590018" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2352" width="32" height="32"><path d="M426.666667 128h-149.333334v234.453333c0 12.074667 9.450667 21.546667 21.205334 21.546667h298.922666c11.626667 0 21.205333-9.6 21.205334-21.546667V128h-64v149.504c0 23.466667-19.157333 42.496-42.624 42.496h-42.752A42.666667 42.666667 0 0 1 426.666667 277.504V128zM192 896V661.546667C192 602.474667 239.786667 554.666667 298.837333 554.666667h426.325334A106.709333 106.709333 0 0 1 832 661.546667V896h42.517333A21.312 21.312 0 0 0 896 874.752V273.664L750.336 128H704v234.453333c0 58.965333-47.701333 106.88-106.538667 106.88H298.538667A106.56 106.56 0 0 1 192 362.453333V128H149.248A21.269333 21.269333 0 0 0 128 149.482667v725.034666C128 886.421333 137.578667 896 149.482667 896H192zM42.666667 149.482667A106.602667 106.602667 0 0 1 149.248 42.666667H768a42.666667 42.666667 0 0 1 30.165333 12.501333l170.666667 170.666667A42.666667 42.666667 0 0 1 981.333333 256v618.752A106.645333 106.645333 0 0 1 874.517333 981.333333H149.482667A106.752 106.752 0 0 1 42.666667 874.517333V149.482667z m704 512.042666c0-12.010667-9.536-21.525333-21.504-21.525333H298.837333C286.933333 640 277.333333 649.6 277.333333 661.546667V896h469.333334V661.546667z" fill="#000000" p-id="2353"></path></svg>',
                click() {
                    popupFrame.style.display = 'block';
                    qrCodeFrame.style.display = 'block';
                },
            };

            var toolbar = [
                newIcon,
                saveIcon,
                "headings",
                "bold",
                "italic",
                "strike",
                "emoji",
                "|",
                "line",
                "quote",
                "list",
                "ordered-list",
                "check",
                "outdent",
                "indent",
                "code",
                "inline-code",
                "undo",
                "redo",
                "link",
                "upload",
                "table",
                "edit-mode",
                "both",
                "preview",
                "fullscreen",
                "outline",
                "code-theme",
                "content-theme", 
                "export"
            ];

            // 获取窗口信息
            const width = window.innerWidth; 
            const pageHeight = document.body.scrollHeight;

            // 判断宽度并输出
            if (width < 641) {
                toolbar = [
                    newIcon,
                    "headings",
                    "bold",
                    "list",
                    "ordered-list",
                    "check",
                ];
            }

            this.contentEditor = new Vditor('vditor', {
                height: pageHeight - 10,
                mode: 'ir',
                toolbar: toolbar,
                toolbarConfig: {
                    pin: true,
                },
                cache: {
                    enable: false,
                }, 
                upload: {
                    accept: 'image/*,.mp3, .wav, .rar',
                    token: 'test',
                    url: '/api/upload',
                    linkToImgUrl: '/api/fetch',
                    filename (name) {
                        return name.replace(/[^(a-zA-Z0-9\u4e00-\u9fa5\.)]/g, '').
                        replace(/[\?\\/:|<>\*\[\]\(\)\$%\{\}@~]/g, '').
                        replace('/\\s/g', '')
                    },
                },
                blur: () => {
                    var self = this;
                    var content = self.contentEditor.getValue();
                    if (self.content == content) {
                        console.log('nothing changed')
                        return;
                    }

                    self.content = content;
                    updatePageTitle(content);

                    var parameter = {
                        "content": content
                    }
                    axios.post(`/api/update/${key}`, parameter)
                        .then(response => {
                            try {
                                var data = response.data;
                                self.history_id = data.history_id;
                            }
                            catch
                            {

                            }
                        });
                },
                after: () => {
                    var self = this;
                    axios.get(`/api/get/${key}`)
                        .then(response => {
                            self.content = response.data;
                            self.contentEditor.setValue(response.data);
                            updatePageTitle(self.content)
                            var qrcode = new QRCode('qrcode');
                            qrcode.makeCode(window.location.href);
                        });

                    var fullscreenButton = document.querySelector('button[data-type="fullscreen"]');
                    if (fullscreenButton) {
                        fullscreenButton.click();
                    }

                    var refreshTask = setInterval(function () {
                        var url = `/api/refresh/${key}/${self.history_id}`
                        console.log(url)
                        axios.get(url)
                            .then(response => {
                                if (response.data != {} && response.data.content) {
                                    var data = response.data
                                    self.content = data.content;
                                    self.contentEditor.setValue(self.content)
                                    self.history_id = data.history_id;
                                }
                            });
                    }, 5000);
                },
            })
        },
    })
}


// 绑定点击事件  
popupFrame.addEventListener('click', () => {
    // 设置为隐藏
    popupFrame.style.display = 'none';
    qrCodeFrame.style.display = 'none';
});