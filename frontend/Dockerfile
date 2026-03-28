FROM nginx:alpine

COPY ./nginx-spa.conf /etc/nginx/conf.d/default.conf
COPY ./dist /usr/share/nginx/html

EXPOSE 80