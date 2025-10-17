from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.database import read_data, save_data

router = APIRouter()


@router.get("/users")
def users_page():
    users = read_data("users.json")

    users_html = ""
    for user in users:
        users_html += f"""
        <div class="user-card">
            <div class="user-info">
                <h3>{user['username']}</h3>
                <p class="user-email">{user['email']}</p>
                <p class="user-id">ID: {user['id']}</p>
            </div>
        </div>
        """

    return HTMLResponse(
        f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Пользователи - Мой Блог</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: 'Arial', sans-serif;
                background-color: #687d31;
                min-height: 100vh;
                background-image: url(
                    'https://i.pinimg.com/1200x/61/94/58/61945810e068dbcc17ac4818134327de.jpg'
                );
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}

            .overlay {{
                background-color: rgba(104, 125, 49, 0.85);
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 1;
            }}

            .container {{
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                position: relative;
                z-index: 2;
            }}

            .back-link {{
                display: inline-block;
                background-color: #19350c;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 10px;
                margin-bottom: 20px;
                transition: all 0.3s ease;
            }}

            .back-link:hover {{
                background-color: #2a5215;
                transform: translateY(-2px);
            }}

            .content-box {{
                background-color: #d5d3cc;
                color: #19350c;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
                margin-bottom: 30px;
            }}

            .content-box h1 {{
                margin-top: 0;
                color: #19350c;
                text-align: center;
            }}

            .create-form {{
                background-color: rgba(25, 53, 12, 0.1);
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 30px;
            }}

            .form-group {{
                margin-bottom: 15px;
            }}

            .form-input {{
                width: 100%;
                padding: 12px;
                border: 2px solid #19350c;
                border-radius: 10px;
                background-color: white;
                color: #19350c;
                font-size: 16px;
                box-sizing: border-box;
            }}

            .form-input:focus {{
                outline: none;
                border-color: #687d31;
            }}

            .submit-btn {{
                background-color: #19350c;
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                width: 100%;
            }}

            .submit-btn:hover {{
                background-color: #2a5215;
                transform: translateY(-2px);
            }}

            .users-list {{
                display: grid;
                gap: 15px;
            }}

            .user-card {{
                background-color: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                border-left: 5px solid #19350c;
            }}

            .user-info h3 {{
                margin: 0 0 10px 0;
                color: #19350c;
                font-size: 1.3em;
            }}

            .user-email {{
                color: #687d31;
                margin: 5px 0;
                font-weight: bold;
            }}

            .user-id {{
                color: #666;
                margin: 5px 0;
                font-size: 0.9em;
            }}

            .empty-state {{
                text-align: center;
                color: #666;
                padding: 40px;
                background-color: rgba(255, 255, 255, 0.5);
                border-radius: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="overlay"></div>
        <div class="container">
            <a href="/" class="back-link">← Назад на главную</a>

            <div class="content-box">
                <h1>👥 Управление пользователями</h1>

                <div class="create-form">
                    <h3>Создать нового пользователя</h3>
                    <div class="form-group">
                        <input type="text" id="username" class="form-input"
                               placeholder="Введите имя пользователя">
                    </div>
                    <div class="form-group">
                        <input type="email" id="email" class="form-input"
                               placeholder="Введите email">
                    </div>
                    <button class="submit-btn" onclick="createUser()">
                        Создать пользователя
                    </button>
                </div>

                <h3>Список пользователей:</h3>
                <div class="users-list">
                    {
                        users_html
                        if users_html
                        else '<div class="empty-state">😔 Пользователей пока нет</div>'
                    }
                </div>
            </div>
        </div>

        <script>
            async function createUser() {{
                const username = document.getElementById('username').value;
                const email = document.getElementById('email').value;

                if (!username || !email) {{
                    alert('Пожалуйста, заполните все поля');
                    return;
                }}

                const response = await fetch(
                    '/api/users?username=' + encodeURIComponent(username) +
                    '&email=' + encodeURIComponent(email),
                    {{
                        method: 'POST'
                    }}
                );

                if (response.ok) {{
                    alert('Пользователь успешно создан!');
                    location.reload();
                }} else {{
                    alert('Ошибка при создании пользователя');
                }}
            }}

            // Добавляем обработчик нажатия Enter
            document.addEventListener('DOMContentLoaded', function() {{
                document.getElementById('username').addEventListener(
                    'keypress', function(e) {{
                    if (e.key === 'Enter') createUser();
                }});
                document.getElementById('email').addEventListener(
                    'keypress', function(e) {{
                    if (e.key === 'Enter') createUser();
                }});
            }});
        </script>
    </body>
    </html>
    """
    )


@router.post("/api/users")
def create_user_api(username: str, email: str):
    users = read_data("users.json")

    new_user = {
        "id": len(users) + 1,
        "username": username,
        "email": email,
        "created_at": datetime.now().isoformat(),
    }

    users.append(new_user)
    save_data("users.json", users)

    return {"message": "Пользователь создан"}
