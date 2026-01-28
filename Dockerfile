FROM nginx:alpine
# 删除默认页面并复制我们的精美页面
RUN rm /usr/share/nginx/html/*
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]