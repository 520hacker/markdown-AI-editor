# 支持AI和Markdown的匿名随手记

欢迎访问我们部署的支持Markdown格式的匿名随手记平台：[https://suishouji.qiangtu.com](https://suishouji.qiangtu.com/)

## 背景与目的

在探索了 [https://github.com/Lincest/web-note](https://github.com/Lincest/web-note) 这个项目之后，我们发现在日常使用中，传统的纯文本记事本已经无法满足需求。因此，我们决定为其添加Markdown支持，以更好地满足用户的编辑和记录需求。

## 主要功能特点

- **匿名编辑：** 用户可以匿名进行编辑，保护隐私。
- **选中文字AI对话**：选中文字之后可以在当前文档利用AI对选中的文字进行拓展、改写、回答、翻译等。
- **短网址：** 每篇随手记都会自动生成一个短网址，方便分享。
- **导出功能：** 支持将编辑的内容导出。
- **二维码生成：** 可以将编辑的内容生成二维码，方便在移动设备上继续查看或分享。
- **多人协作：** 多人同时编辑一篇随手记，会自动合并更新，但可能存在5秒内更改内容的冲突。
- **AI辅助：** 提供AI辅助功能，提供更便捷的写作体验。
- **一键保存到Memos（未来可能实现）：** 我们也考虑将一键保存到Memos作为未来的功能之一，以进一步丰富用户的记录体验。

## 如何使用

1. 使用以下命令获取我们的Docker镜像：`docker pull odinluo/suishouji:latest`。
2. 将端口映射到5000，并将数据和文件保留，可以通过映射目录 `/app/files`来实现。
3. 参考compose配置：

```yaml
version: '3'
services:
  twoapi:
    image: odinluo/suishouji:latest
    ports:
      - 7028:5000
    deploy:
      resources:
        limits:
          memory: 500m
    environment:
      - STATIC_DOMAIN=https://2504-static.qiangtu.com
    volumes:
      - /www/wwwroot/suishouji.qiangtu.com:/app/files
      - /www/wwwroot/2504-static.qiangtu.com:/app/assets

```

注： 本初采用本地化图床，未采用oss, 则需要配置图床域名 STATIC_DOMAIN 和本地图床文件夹 /www/wwwroot/2504-static.qiangtu.com。 

### 请注意，图床域名指向的站点请设置为纯静态模式！！！！！！



## 特色与亮点

- **开放编辑：** 每个人都可以对内容进行编辑。
- **便捷新建：** 点击左上角的“新建”按钮，系统将自动生成一个新的短网址。
- **多人协作：** 支持多人同时编辑，但请注意可能存在冲突情况。
- **移动端支持：** 提供二维码生成功能，便于在移动设备上查看和分享。
- **拓展性强：** 即使当前版本暂时屏蔽了OSS上传相关功能，但我们仍考虑作为未来的拓展方向。
- **AI写作助手**：AI写作助手功能，提升写作效率。
- **版本历史：** 当前版本已经支持版本历史功能，但尚未暴露相关接口。

我们诚邀您体验我们的随手记平台，记录生活的点滴，留下您宝贵的思考和回忆！

## 鸣谢项目
- vditor
- Echo
