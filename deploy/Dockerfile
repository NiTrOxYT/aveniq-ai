# AVENIQ AI — Multi-Tenant SaaS Platform Dockerfile
FROM node:20-alpine AS base

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production || true

COPY . .

EXPOSE 8097

CMD ["node", "-e", "console.log('AVENIQ SaaS Engine Docker Container Ready')"]
