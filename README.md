# Personal Dashboard

A dashboard app that contains / will contain several modules that I can use in my daily life.

## Setup

### Development

Setting up for development requires having a mongodb instance up and running on your machine, either running on port 27017 (Mongo Default) or customising the value in [.env.dev](./.env.dev)

```sh
# Create a virtual python environment
python -m venv .venv

# Activate the virtual env
./.venv/Scripts/activate

# Install the dependencies
pip install -r requirements.txt

# Run the app
flask run
```

### Production

^ Production simply means to be running in the background, and for actual usage.

All of the setup has been configured into the `Dockerfile` and `docker-compose.yml` files so that it simply takes running

```sh
docker compose up -d
```

To get the app fully up and running locally.

The app can then be easily accessed at [localhost/dashboard](http://localhost/dashboard)

All data is then stored within a docker volume, which will persist between sessions, so if you need to restart the app you won't lose your data.

## Modules

- [ ] [Recipe Manager](#recipe-manager)
- [ ] [Car Management](#car-management)

### Recipe Manager

The recipe manager is used to store recipes to be used as inspiration.
This module will also include a kitchen feature, which can be used to track current food items in stock, and maybe build recipes from those, or filter by items already in the kitchen.

**Features:**

- [x] Create Recipes
- [x] View Recipes
- [ ] Delete Recipes
- [ ] Tag Recipes
- [ ] Search for Recipes

### Car Management

This module is used to manage various things to do with looking after cars. The main usage will be for tracking things such as MOT / Service reminders.

**Features:**

- [ ] MOT Reminders
- [ ] Service Reminders
