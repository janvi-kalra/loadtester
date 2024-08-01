# Dockerfile for Frontend (React)

FROM node:14
WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build
FROM nginx:1.19

# Copy the build output to the Nginx html directory
COPY --from=0 /app/build /usr/share/nginx/html

# Expose the port that Nginx will run on
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
