FROM node:12.18.4 AS builder

COPY package.json ./app/package.json
COPY package-lock.json ./app/package-lock.json

WORKDIR /app

RUN npm install
COPY . .
RUN npm run build -- --prod

RUN npm i -g serve

EXPOSE 3000

CMD [ "serve", "-s", "dist" ]

# FROM nginx:latest

# COPY --from=builder /app/dist /var/www/frontend

# COPY nginx.conf /etc/nginx/nginx.conf
# COPY default.conf /etc/nginx/conf.d/default.conf