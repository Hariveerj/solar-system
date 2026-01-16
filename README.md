# Solar System Java Application

A simple Java Spring Boot project to display Solar System and its planets.

---
## Requirements

For development, you will need Java 17 and Maven installed in your environment.

### Java
- #### Java installation on Windows

  Download and install the JDK from the [official Oracle website](https://www.oracle.com/java/technologies/javase-downloads.html) or [OpenJDK](https://openjdk.org/).

- #### Java installation on Ubuntu

  You can install OpenJDK easily with apt, just run the following commands:

      $ sudo apt update
      $ sudo apt install openjdk-17-jdk

- #### Verify Installation

  If the installation was successful, you should be able to run the following command:

      $ java -version
      java version "17.x.x"

### Maven
- #### Maven installation

  Download Maven from the [Apache Maven website](https://maven.apache.org/download.cgi) and follow the installation instructions.

- #### Verify Installation

  If the installation was successful, you should be able to run the following command:

      $ mvn -v
      Apache Maven 3.x.x

---
## Build and Run the Application

### Install Dependencies and Build
    $ mvn clean install

### Run the Application
    $ mvn spring-boot:run

### Access Application on Browser
    http://localhost:8080/

