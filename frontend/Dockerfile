# Build Stage
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
# If package-lock doesn't exist, npm ci might fail, so we use npm install
# We also want to respect the user's request for package-lock to be present in subsequent runs?
# But for now, just install.
RUN npm install
COPY . .
RUN npm run build

# Production Stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
