FROM tomcat:10.0.10-jdk11-openjdk

# Setup directory structure and permissions
RUN rm -rf /usr/local/tomcat/webapps/* && \
    mkdir -p /usr/local/tomcat/webapps/ROOT/WEB-INF/classes/mypackage && \
    mkdir -p /usr/local/tomcat/webapps/ROOT/WEB-INF/lib

# Copy application files
COPY WEB-INF/web.xml /usr/local/tomcat/webapps/ROOT/WEB-INF/
COPY chat.html /usr/local/tomcat/webapps/ROOT/
COPY CarRentalChatbot.class /usr/local/tomcat/webapps/ROOT/WEB-INF/classes/mypackage/

# Add required libraries
ADD https://repo1.maven.org/maven2/com/googlecode/json-simple/json-simple/1.1.1/json-simple-1.1.1.jar /usr/local/tomcat/webapps/ROOT/WEB-INF/lib/
ADD https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.0.33/mysql-connector-j-8.0.33.jar /usr/local/tomcat/lib/

# Set final permissions
RUN chmod -R 755 /usr/local/tomcat/webapps && \
    chmod 644 /usr/local/tomcat/lib/mysql-connector-j-8.0.33.jar