# Stage 1: Build the frontend
FROM node:lts-alpine 

WORKDIR /app

COPY frontend/App/react-app /app
COPY frontend/App/react-app/package*.json ./

# Install dependencies including jwt-decode
RUN npm install axios bootstrap jwt-decode react react-dom react-router-dom \
    @types/react @types/react-dom @typescript-eslint/eslint-plugin \
    @typescript-eslint/parser @vitejs/plugin-react \
    eslint eslint-plugin-react-hooks eslint-plugin-react-refresh \
    typescript vite

RUN npm install --global serve

# Build the frontend
RUN npm run build
#RUN npm install -g servese

# Stage 2: Serve the application


#COPY --from=frontend-build /app/dist /usr/share/nginx/html

#FROM nginx:stable-alpine as production-stage
#RUN npm install
#RUN npm install --global serve
#COPY --from=build-stages /app/dist .
EXPOSE 3000
CMD ["serve", "-s", "dist/"]