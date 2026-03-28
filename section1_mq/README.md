# Qualitest/Elbit Home Assignment

## Section 1: Message Queue Implementation (RabbitMQ)

This section implements a Publisher/Consumer architecture using Python and RabbitMQ. The entire stack is containerized using Docker Compose for a seamless, zero-configuration startup.

### Prerequisites
* Docker and Docker Compose installed.

### Running the System

1. **Launch the Environment:**
   Navigate to the root of the repository and run the following command to build the images and start the broker and Python scripts:
   ```bash
   sudo docker-compose up --build
   ```

