FROM node:18-alpine as build

WORKDIR /app

# Копируем package файлы
COPY package*.json ./
RUN npm install

# Копируем env файл
COPY .env ./

# Копируем исходный код
COPY . .

# Собираем приложение
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]