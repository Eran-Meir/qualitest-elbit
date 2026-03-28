# Qualitest/Elbit Home Assignment

## Section 1: Message Queue Implementation (RabbitMQ)

This section implements a simple Publisher/Consumer architecture using Python and RabbitMQ. 

### Prerequisites
* Docker and Docker Compose installed.
* Python 3.8+ installed.

### Setup Instructions

1. **Start the RabbitMQ Broker:**
   Navigate to the repository root and start the RabbitMQ container in detached mode:
   ```bash
   docker-compose up -d