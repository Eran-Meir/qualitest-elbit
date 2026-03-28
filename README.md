# Qualitest / Elbit Systems - Home Assignment

This repository contains the deliverables for the DevOps/SRE technical assignment.

---

## Section 1: Implementing a Publisher and Consumer (RabbitMQ)

This section implements a simple message queuing system using Python and RabbitMQ. The publisher sends 10 messages to the channel "ABC", and the consumer subscribes to the same channel to print them. The entire architecture is fully containerized for a zero-configuration startup.

### Setup & Execution

1. **Prerequisites:** Docker and Docker Compose installed on your machine.
2. **Launch the Stack:** Navigate to the `section1_mq` directory and run the following command to build the images and start the environment:
   ```bash
   cd section1_mq
   sudo docker-compose up --build
   ```

3. **Expected Output:**
   Once the RabbitMQ broker initializes, the publisher and consumer containers will connect automatically. You will see the messages being sent and received in real-time in your terminal:
   ```text
   mq_publisher | [*] Publisher connected to rabbitmq. Sending messages to 'ABC'...
   mq_publisher |  [x] Sent 'Hello! This is message number 1'
   mq_consumer  | [*] Waiting for messages on 'ABC' at rabbitmq. To exit press CTRL+C
   mq_consumer  |  [x] Received Hello! This is message number 1
   mq_publisher |  [x] Sent 'Hello! This is message number 2'
   mq_consumer  |  [x] Received Hello! This is message number 2
   ...
   mq_publisher |  [x] Sent 'Hello! This is message number 10'
   mq_consumer  |  [x] Received Hello! This is message number 10
   mq_publisher | [*] All messages sent. Connection closed.
   ```

4. **RabbitMQ Management Dashboard:**
   To observe the message queues, connections, and system metrics visually:
   * Open your web browser and navigate to: `http://localhost:15672`
   * **Username:** `guest`
   * **Password:** `guest`
   * Navigate to the **"Queues"** tab to see the `ABC` channel metrics.

5. **Tear Down:**
   To cleanly stop the environment and remove the containers, run:
   ```bash
   sudo docker-compose down
   ```

---

## Section 2: Creating a Service to Monitor CPU Usage and Send Alerts

### 1. Implementation Description
To create a reliable service that monitors CPU usage and triggers alerts, I have implemented a background daemon script using Python. A working version of this script is located in the `section2_cpu_monitor` directory.

### 2. Language and Libraries
* **Programming Language:** Python 3.x
* **Core Library:** `psutil` (Python System and Process Utilities). This is the industry standard for retrieving information on running processes and system utilization (CPU, memory, disks, network).
* **Standard Libraries:** * `time`: To handle the continuous monitoring intervals.
  * `logging`: To maintain a local historical record of CPU spikes and act as the immediate alerting output.

### 3. Continuous Monitoring Method
The service utilizes an infinite `while True` loop to act as a continuous daemon. Inside the loop, it calls `psutil.cpu_percent(interval=1)`. 
Setting the `interval` parameter to 1 second is crucial; it blocks the script for 1 second to compare system CPU times, providing an accurate, non-blocking average rather than an instantaneous spike. To ensure the monitoring script itself does not consume unnecessary CPU cycles, a `time.sleep(5)` interval pauses the execution between checks.

### 4. Alerting Method
When the CPU threshold (80%) is breached, the system triggers an alerting mechanism. In the provided solution, it uses the `logging` module to stream a `CRITICAL ALERT` to the console and immediately writes it to a persistent local file (`cpu_alerts.log`). In a full production environment, this block of code would be expanded to use `smtplib` to dispatch an email via an SMTP relay, or utilize the `requests` library to trigger a webhook notification to Slack or PagerDuty.

### 5. High-Level Pseudo-Code

```text
IMPORT psutil, time, logging

DEFINE THRESHOLD = 80.0
DEFINE CHECK_INTERVAL = 5 seconds

FUNCTION start_monitoring():
    LOG "Starting CPU Monitor..."
    
    WHILE True:
        // Get CPU average over a 1-second window
        current_cpu = psutil.cpu_percent(interval=1)
        
        IF current_cpu > THRESHOLD:
            TRIGGER_ALERT("CRITICAL: CPU usage is at {current_cpu}%")
            LOG_TO_FILE("Alert dispatched for high CPU.")
        ELSE:
            LOG "CPU usage normal: {current_cpu}%"
        
        // Wait before the next check
        SLEEP(CHECK_INTERVAL)

// Initialize the service
start_monitoring()
```

---

## Bonus Question: Understanding and Moving Multicast Messages

### 1. What is Multicast and its Typical Use Cases?
Multicast is a network communication protocol where a single stream of data is transmitted to multiple, specific recipients simultaneously. Unlike unicast (one-to-one) or broadcast (one-to-all), multicast is a "one-to-many" model utilizing specific IP address ranges (Class D: 224.0.0.0 to 239.255.255.255). Clients who wish to receive the data must actively "subscribe" to a specific multicast group address.

**Typical Use Cases:**
* **Streaming Media:** IPTV or live corporate video broadcasts where sending a separate unicast stream to every viewer would exhaust network bandwidth.
* **Financial Services:** High-frequency trading platforms distributing live stock ticker data to hundreds of endpoints simultaneously with minimal latency variance.
* **Routing and Discovery:** Network protocols like OSPF use multicast to discover peers and share routing tables on a local network.

### 2. Solutions for Moving Multicast Between Networks
Standard network routers are typically configured to drop multicast and broadcast traffic to prevent network storms. To route multicast messages across different subnets or WANs, specific protocols are required:

* **IGMP (Internet Group Management Protocol):** Used on the local area network (LAN). Client machines use IGMP to signal to their local router that they want to join a specific multicast group.
* **