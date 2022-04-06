## 前置条件
- 有flomo PRO权限，详情可见 https://flomoapp.com/mine/?source=membership
- 熟悉Logseq https://github.com/logseq/logseq
- 具备Python基础、网页抓包基础技能

## 概述
- 在flomo 网页端通过F12获取到自己的cookie\token信息
- 修改源代码中的lspath参数为你本地的logseq path路径

## flomo中的使用指引
- 卡片笔记需要按特定的格式：三段（主题+内容+标签）以回车分隔，示例
![image](https://user-images.githubusercontent.com/38389059/161942734-fb2299e9-a48a-4a5c-8307-0a3bd06e1f50.png)
- 卡片添加特定的标签 #zk（参照上图）当然也支持多个标签的使用

## 本程序的使用效果

本程序的主要设计思路（后续还得再优化）
![](https://lewis-images.oss-cn-shenzhen.aliyuncs.com/img/20220406070759.png)
本程序的实现效果1：zk标签的卡片可同步到logseq
![](https://lewis-images.oss-cn-shenzhen.aliyuncs.com/img/20220406064856.png)
本程序的实现效果2：可从logseq跳转回flomo方便在源头修改卡片
![](https://lewis-images.oss-cn-shenzhen.aliyuncs.com/img/f2log.gif)
