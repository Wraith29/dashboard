Write-Output "Stopping Docker.";
docker compose down;

Write-Output "Docker Stopped.";
Write-Output "Restarting Docker";

docker compose up -d --force-recreate --build

Write-Output "Docker Restarted";
