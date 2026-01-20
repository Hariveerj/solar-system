FROM openjdk:11-jre-slim

WORKDIR /app

ADD target/*.jar app.jar

EXPOSE 8080

CMD ["java","-jar","app.jar"]