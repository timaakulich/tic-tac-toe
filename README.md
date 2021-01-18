# System requirements
0. python 3.8
1. fastapi@0.63.0
2. postgresql@12


# How to run
0. Add 127.0.0.1 tic-tac-toe.app to /etc/hosts
1. ```docker-compose up```
2. Open browser at http://tic-tac-toe.app/docs or http://127.0.0.1:5555/docs


# API
0. Ping Service (Healthcheck) - http://127.0.0.1:5555/docs#/ping/ping_v1_ping__get
1. Signup - http://127.0.0.1:5555/docs#/auth/create_user_v1_auth_users_post
2. Signin - http://127.0.0.1:5555/docs#/auth/get_token_v1_auth_token_post

For the authorization use:
```-H  "Authorization: Bearer <token from (2)>"```
3. Get all players games - http://127.0.0.1:5555/docs#/game/get_games_v1_games__get
4. Start new game - http://127.0.0.1:5555/docs#/game/create_game_v1_games__post
5. Get game information - http://127.0.0.1:5555/docs#/game/get_game_v1_games__game_id__get
6. Get all moves http://127.0.0.1:5555/docs#/game/get_moves_v1_games__game_id__moves__get
7. Do move http://127.0.0.1:5555/docs#/game/create_move_v1_games__game_id__moves__post

# PS:
Run tests, flake8, isort - ```tox```
