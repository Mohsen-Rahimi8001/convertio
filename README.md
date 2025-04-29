# 🎬 Microservices Video Processing Platform

This project is a distributed microservices-based video management and processing platform. It allows authenticated users to upload, manage, and process videos with asynchronous operations like video reversal using RabbitMQ for messaging and ffmpeg for processing.

## 🧩 Services Overview

- **Gateway Service**: Acts as the API gateway. Handles authentication, forwards requests to appropriate services, and serves as the single entry point.
- **User Service**: Manages user registration, authentication (JWT-based), and account lifecycle events. Sends RabbitMQ messages when a user is deleted.
- **Media Service**: Handles video uploads, ownership checks, deletion, and stores metadata in a relational database. Publishes processing tasks to RabbitMQ.
- **Convert Service**: Listens to video processing tasks via RabbitMQ (e.g., reverse operation), performs the task using ffmpeg, and saves results to a shared volume.
- **RabbitMQ**: Facilitates asynchronous communication between services.
- **Docker & Docker Compose**: All services run in containers with isolated environments.

## 🔁 Workflow

1. Users upload videos through the gateway → media service.
2. Users request a video operation (e.g., reverse).
3. Media service sends a task message via RabbitMQ to the convert service.
4. Convert service processes the video using ffmpeg and saves it.
5. Users access the converted video via the same media endpoint.

## ⚙️ Tech Stack

- Python, Django, DRF
- Flask-RESTX (Gateway)
- RabbitMQ
- MongoDB
- PostgreSQL
- ffmpeg / ffmpeg-python
- Docker & docker-compose
