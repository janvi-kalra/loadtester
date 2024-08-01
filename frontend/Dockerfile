# Dockerfile for Frontend (React)

FROM node:14
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

RUN npm run build

# Use the official Nginx image to serve the React app
FROM nginx:1.19

# Copy the build output to the Nginx html directory
COPY --from=0 /app/build /usr/share/nginx/html

# Expose the port that Nginx will run on
EXPOSE 80

# Command to run Nginx
CMD ["nginx", "-g", "daemon off;"]
