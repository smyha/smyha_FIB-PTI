FROM tomcat:10
COPY my_webapp /my_webapp
WORKDIR /
RUN cp -r my_webapp /usr/local/tomcat/webapps


# cd ${USER_HOME}/apache-tomcat-10.0.10/webapps
# docker build -f Dockerfile -t carrenting .
# docker run --name carrenting -d -p 8080:8080 -p 8443:8443 carrenting