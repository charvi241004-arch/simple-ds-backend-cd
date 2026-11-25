# Backend-only Data Science Deployment (Iris API)

A small end-to-end example: FastAPI prediction service + scikit-learn model,
containerized with Docker and deployed by GitHub Actions.

## 1. Run locally without Docker

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.train_model
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs`.

## 2. Run with Docker

```bash
docker build -t iris-api .
docker run --rm -p 8000:8000 iris-api
```

Or use Compose locally after creating `.env` with your Docker Hub username:
```bash
echo 'DOCKERHUB_USERNAME=your_dockerhub_username' > .env
docker compose -f compose.yml up -d
```
For a local build, change the `image:` in compose.yml to `iris-api:latest`
and add `build: .` under the service.

## 3. Test the API

Health:
```bash
curl http://localhost:8000/health
```

Prediction:
```bash
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

Swagger UI: `http://localhost:8000/docs`

## 4. Configure Continuous Deployment

This example deploys to an Ubuntu/Linux VM that has Docker Engine and the
Docker Compose plugin installed and is reachable by SSH.

1. Create a Docker Hub access token.
2. Push this project to a GitHub repository on branch `main`.
3. In GitHub repository **Settings → Secrets and variables → Actions**, add:
   - `DOCKERHUB_USERNAME`: Docker Hub username
   - `DOCKERHUB_TOKEN`: Docker Hub access token
   - `SERVER_HOST`: public IP or hostname of the deployment VM
   - `SERVER_USER`: SSH user on that VM
   - `SERVER_SSH_KEY`: private SSH key allowed to log in to that VM
4. Ensure the SSH user can run Docker commands on the VM.
5. Push a commit to `main`.

GitHub Actions runs tests, builds the Docker image, pushes `latest` and a
commit-SHA tag to Docker Hub, copies the Compose file to the VM, then pulls
and restarts the service. Check **GitHub → Actions** for the run log.

## 5. Architecture

Developer → GitHub push → GitHub Actions → tests → Docker build → Docker Hub
→ SSH deployment VM → Docker Compose → FastAPI + trained ML model.

## Notes

- This is backend-only; there is no frontend.
- The model is trained on the built-in Iris dataset during image build.
- For a real deployment, use HTTPS/reverse proxy, firewall rules, non-root
  containers, pinned image tags, monitoring, and proper secret rotation.
- The workflow assumes a Linux deployment VM with Docker already installed.
