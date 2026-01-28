FROM nginx:alpine

# 删除默认页面
RUN rm /usr/share/nginx/html/*

# 复制所有 HTML 文件到容器
# 这样 index.html 和 status.html 都会被放进去
COPY *.html /usr/share/nginx/html/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]