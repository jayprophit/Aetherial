# Deployment Guide: Production Environment Setup

## Introduction

This guide provides detailed instructions for deploying the Unified Platform in a production environment. It covers infrastructure requirements, installation steps, configuration, monitoring, and maintenance procedures.

## Prerequisites

### Hardware Requirements

- **Web Servers**:
  - Minimum: 4 vCPUs, 8GB RAM, 50GB SSD
  - Recommended: 8 vCPUs, 16GB RAM, 100GB SSD
  - Load balanced across multiple instances

- **Database Server**:
  - Minimum: 4 vCPUs, 16GB RAM, 100GB SSD
  - Recommended: 8 vCPUs, 32GB RAM, 500GB SSD
  - High availability configuration

- **AI Service Servers**:
  - Minimum: 8 vCPUs, 16GB RAM, 100GB SSD
  - Recommended: 16 vCPUs, 32GB RAM, 200GB SSD
  - GPU acceleration recommended

- **Storage**:
  - Scalable object storage for user uploads
  - Minimum 1TB initial capacity
  - Backup storage equal to primary storage

### Software Requirements

- **Operating System**: Ubuntu 20.04 LTS or later
- **Container Runtime**: Docker 20.10 or later
- **Orchestration**: Docker Compose or Kubernetes
- **Database**: PostgreSQL 14 or later
- **Web Server**: Nginx 1.20 or later
- **Node.js**: Version 16 or later
- **SSL Certificate**: Valid SSL certificate for production domains

### Network Requirements

- **Domains**: Primary domain and subdomains configured
- **DNS**: Proper DNS configuration for all domains
- **Firewall**: Configured to allow necessary traffic
- **Load Balancer**: Configured for web server instances
- **CDN**: Content delivery network for static assets (recommended)

## Installation Process

### 1. Prepare the Environment

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required dependencies
sudo apt install -y curl git build-essential

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create application directory
sudo mkdir -p /opt/unified-platform
sudo chown $(whoami):$(whoami) /opt/unified-platform
```

### 2. Deploy the Application

```bash
# Extract the deployment package
tar -xzf unified-platform-production.tar.gz -C /opt/unified-platform
cd /opt/unified-platform

# Configure environment variables
cp .env.template .env
nano .env  # Edit with your production values

# Run database migrations
node migrations/run-migrations.js

# Start the application
docker-compose up -d
```

### 3. Configure Web Server

```bash
# Install Nginx
sudo apt install -y nginx

# Configure Nginx as reverse proxy
sudo nano /etc/nginx/sites-available/unified-platform

# Example configuration:
# server {
#     listen 80;
#     server_name unifiedplatform.com www.unifiedplatform.com;
#     
#     location / {
#         return 301 https://$host$request_uri;
#     }
# }
# 
# server {
#     listen 443 ssl;
#     server_name unifiedplatform.com www.unifiedplatform.com;
#     
#     ssl_certificate /etc/letsencrypt/live/unifiedplatform.com/fullchain.pem;
#     ssl_certificate_key /etc/letsencrypt/live/unifiedplatform.com/privkey.pem;
#     
#     location / {
#         proxy_pass http://localhost:3000;
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#     }
# }

# Enable the site
sudo ln -s /etc/nginx/sites-available/unified-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Set Up SSL Certificate

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d unifiedplatform.com -d www.unifiedplatform.com

# Verify automatic renewal
sudo certbot renew --dry-run
```

### 5. Configure Backups

```bash
# Set up daily backups
sudo crontab -e

# Add the following line:
# 0 2 * * * /opt/unified-platform/backup.sh >> /var/log/unified-platform-backup.log 2>&1
```

## Configuration

### Environment Variables

The `.env` file contains all necessary configuration for the application. Key variables include:

- **Database Configuration**:
  - `DB_HOST`: Database hostname
  - `DB_PORT`: Database port
  - `DB_USERNAME`: Database username
  - `DB_PASSWORD`: Database password
  - `DB_NAME`: Database name

- **Authentication**:
  - `JWT_SECRET`: Secret key for JWT tokens
  - `JWT_EXPIRY`: Token expiration time

- **AI Services**:
  - `AI_API_KEY`: API key for AI services
  - `AI_SERVICE_URL`: URL for AI service

- **Storage**:
  - `STORAGE_TYPE`: Storage type (local, s3)
  - `S3_BUCKET`: S3 bucket name
  - `S3_ACCESS_KEY`: S3 access key
  - `S3_SECRET_KEY`: S3 secret key
  - `S3_REGION`: S3 region

- **Email**:
  - `SMTP_HOST`: SMTP server hostname
  - `SMTP_PORT`: SMTP server port
  - `SMTP_USER`: SMTP username
  - `SMTP_PASS`: SMTP password
  - `EMAIL_FROM`: Sender email address

- **Monitoring**:
  - `SENTRY_DSN`: Sentry DSN for error tracking

### Application Configuration

The `config/production.json` file contains application-specific configuration:

- **Server Settings**:
  - Port and host configuration
  - CORS settings
  - Rate limiting

- **Feature Flags**:
  - Enable/disable specific features
  - Feature-specific configuration

- **Logging**:
  - Log level and format
  - Log destination

- **Monitoring**:
  - Health check interval
  - Performance metrics

## Scaling and High Availability

### Horizontal Scaling

To scale the application horizontally:

1. **Web Servers**:
   - Add additional web server instances
   - Update load balancer configuration
   - Ensure session persistence if needed

2. **AI Services**:
   - Add additional AI service instances
   - Configure load balancing between instances
   - Consider specialized hardware for AI workloads

3. **Database**:
   - Implement read replicas for read-heavy workloads
   - Consider sharding for very large datasets
   - Ensure proper connection pooling

### High Availability Configuration

For high availability:

1. **Database**:
   - Set up primary-replica configuration
   - Configure automatic failover
   - Regular backup and recovery testing

2. **Web Servers**:
   - Deploy across multiple availability zones
   - Configure health checks and auto-recovery
   - Implement blue-green deployment strategy

3. **Load Balancing**:
   - Use redundant load balancers
   - Configure proper health checks
   - Implement failover mechanisms

## Monitoring and Maintenance

### Monitoring Setup

1. **System Monitoring**:
   - CPU, memory, disk usage
   - Network traffic and latency
   - Container health and resource usage

2. **Application Monitoring**:
   - Request rates and response times
   - Error rates and types
   - User activity and business metrics

3. **Database Monitoring**:
   - Query performance
   - Connection pool usage
   - Replication lag
   - Disk usage and growth

4. **AI Service Monitoring**:
   - Model performance metrics
   - Inference times
   - Error rates
   - Resource utilization

### Health Checks

Use the provided health check script to monitor system health:

```bash
# Run health check
/opt/unified-platform/health-check.sh

# Set up regular health checks
sudo crontab -e

# Add the following line:
# */5 * * * * /opt/unified-platform/health-check.sh >> /var/log/unified-platform-health.log 2>&1
```

### Backup and Recovery

1. **Database Backups**:
   - Daily full backups
   - Point-in-time recovery capability
   - Regular backup verification

2. **Application Data Backups**:
   - User uploads and content
   - Configuration files
   - Logs and audit trails

3. **Recovery Testing**:
   - Regular recovery drills
   - Documented recovery procedures
   - Recovery time objective (RTO) measurement

### Maintenance Procedures

1. **Updates and Patches**:
   - Regular security updates
   - Scheduled maintenance windows
   - Blue-green deployment for zero downtime

2. **Database Maintenance**:
   - Regular vacuum and analyze
   - Index optimization
   - Storage management

3. **Log Management**:
   - Log rotation and archiving
   - Log analysis for security and performance
   - Compliance-related log retention

## Security Considerations

### Network Security

- Implement Web Application Firewall (WAF)
- Configure proper firewall rules
- Use VPN for administrative access
- Implement DDoS protection

### Application Security

- Regular security updates
- Dependency vulnerability scanning
- Input validation and sanitization
- Output encoding
- CSRF and XSS protection

### Data Security

- Encryption at rest for sensitive data
- Encryption in transit (TLS/SSL)
- Data access controls and audit logging
- Regular security audits

### Compliance

- Implement age verification controls
- Configure KYC verification systems
- Set up content moderation
- Configure digital asset locking for minors

## Troubleshooting

### Common Issues

1. **Application Startup Failures**:
   - Check logs with `docker-compose logs`
   - Verify environment variables
   - Check disk space and permissions

2. **Database Connection Issues**:
   - Verify database credentials
   - Check network connectivity
   - Examine database logs

3. **Performance Problems**:
   - Check resource utilization
   - Examine slow query logs
   - Review application logs for bottlenecks

### Logging

Logs are available in the following locations:

- **Application Logs**: `docker-compose logs`
- **Nginx Logs**: `/var/log/nginx/`
- **System Logs**: `journalctl`
- **Backup Logs**: `/var/log/unified-platform-backup.log`
- **Health Check Logs**: `/var/log/unified-platform-health.log`

### Support Resources

- **Documentation**: `/opt/unified-platform/docs/`
- **Support Email**: support@unifiedplatform.com
- **Support Portal**: https://support.unifiedplatform.com

## Conclusion

This deployment guide provides the necessary information to deploy, configure, and maintain the Unified Platform in a production environment. Follow these instructions carefully to ensure a secure, reliable, and performant deployment.

For additional assistance, please contact the platform support team.
