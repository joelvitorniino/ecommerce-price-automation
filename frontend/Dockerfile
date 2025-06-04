
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

FROM node:20-alpine AS production

WORKDIR /app

COPY --from=build /app ./

EXPOSE 3000

CMD ["npm", "run", "preview", "--", "--host", "--port", "3000"]
