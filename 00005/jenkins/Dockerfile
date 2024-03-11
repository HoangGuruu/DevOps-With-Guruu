# Use a Node.js image available from Docker Hub
FROM node:alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) into the working directory
COPY package*.json ./

# Install the application dependencies
RUN npm install

# Copy the entire source code of the application into the working directory inside the container
COPY . .

# Expose port 3000, if needed
EXPOSE 3000

# Run the 'npm run dev' command when the container is started
CMD ["npm", "run", "dev"]
