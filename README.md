---

# 🚀 Real-Time Data Pipeline: Postgres to ClickHouse

This project implements a high-performance, production-ready Change Data Capture (CDC) pipeline. It mirrors the architecture of Yandex Cloud DataLens concepts, allowing you to sync transactional data from PostgreSQL to ClickHouse for real-time analytics.

## 🏗 System Architecture

1. **Simulator (Python)**: Generates random events (purchases, views) and inserts them into Postgres.
2. **PostgreSQL**: The source transactional database (configured with logical replication).
3. **Debezium (Kafka Connect)**: Monitors Postgres Write-Ahead Logs (WAL) and streams changes as JSON.
4. **Redpanda**: A high-performance, Kafka-compatible message broker that stores the change stream.
5. **ClickHouse**: The OLAP engine that "pulls" data from Redpanda using a Kafka Engine and Materialized View.
6. **DataLens**: The BI tool used to visualize the final results.

---

## 🛠 Getting Started

### Prerequisites

* Docker and Docker Compose installed.
* At least 4GB of RAM allocated to Docker.

### Execution

1. **Start the stack**:
```bash
docker-compose up -d --build

```


2. **Wait for initialization**: The `pipeline-setup` container will wait for the services to be healthy before injecting the Debezium configuration. This usually takes about 30–45 seconds.

---

## 🖥 User Interfaces & Access

| Service | URL | What to check |
| --- | --- | --- |
| **Redpanda Console** | [http://localhost:8081](https://www.google.com/search?q=http://localhost:8081) | View the `cdc.public.events` topic to see live JSON messages. |
| **DataLens** | [http://localhost:8080](https://www.google.com/search?q=http://localhost:8080) | Create connections and build your BI dashboards. |
| **ClickHouse UI** | [http://localhost:8082](https://www.google.com/search?q=http://localhost:8082) | Run SQL queries on the analytical tables. |
| **pgAdmin** | [http://localhost:5050](https://www.google.com/search?q=http://localhost:5050) | Manage the source Postgres instance. |

---

## 🔐 Database Credentials

### PostgreSQL

* **Host**: `localhost` (Internal: `postgres`)
* **Port**: `5432`
* **User**: `admin`
* **Password**: `production_password`
* **Database**: `main_db`

### ClickHouse

* **Host**: `localhost` (Internal: `clickhouse`)
* **HTTP Port**: `8123`
* **Native Port**: `9000`
* **User**: `default`
* **Password**: *(None by default)*

### pgAdmin

* **URL**: `http://localhost:5050`
* **Username**: `admin@admin.com`
* **Password**: `admin`

---

## 🔍 How to Verify the Pipeline

### 1. Check Kafka Stream

Open **Redpanda Console** (Port 8081). Navigate to **Topics** -> **cdc.public.events**. If the simulator is running, you will see a stream of JSON objects containing `before` and `after` states of the Postgres rows.

### 2. Check ClickHouse Ingestion

Open **ClickHouse UI** (Port 8082) and run the following query:

```sql
SELECT * FROM events ORDER BY created_at DESC LIMIT 10;

```

If data is appearing here, your Materialized View is correctly consuming from the Kafka engine.

### 3. Setup DataLens

1. Open **DataLens** (Port 8080).
2. **Create Connection**: Select **ClickHouse**.
* **Host**: `clickhouse` (This is the internal Docker name)
* **Port**: `8123`
* **User**: `default`


3. **Create Dataset**: Select the `events` table.
4. **Create Chart**: Use `created_at` for the X-axis and `count(id)` for the Y-axis to see real-time event throughput.

---

## ⚠️ Troubleshooting

* **Connect Container Exited**: Check logs using `docker logs connect`. It usually means it couldn't reach Redpanda during the initial handshake. The healthchecks in the `docker-compose.yml` are designed to prevent this.
* **No data in ClickHouse**: Ensure the `pipeline-setup` container finished successfully (`docker ps -a` should show it as `Exited (0)`).

