from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from datetime import datetime
from app.database import read_data, save_data

router = APIRouter()

@router.get("/posts")
def posts_page():
    posts = read_data("posts.json")
    users = read_data("users.json")
    
    posts_html = ""
    for post in posts:
        author_name = "Неизвестный автор"
        for user in users:
            if user["id"] == post["author_id"]:
                author_name = user["username"]
                break
        
        posts_html += f"""
        <div class="post-card">
            <div class="post-header">
                <h3>{post['title']}</h3>
                <span class="post-author">👤 {author_name}</span>
            </div>
            <div class="post-content">
                <p>{post['content']}</p>
            </div>
            <div class="post-footer">
                <small>ID автора: {post['author_id']}</small>
            </div>
        </div>
        """
    
    users_options = ""
    for user in users:
        users_options += f'<option value="{user["id"]}">{user["username"]} (ID: {user["id"]})</option>'
    
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Посты - Мой Блог</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: 'Arial', sans-serif;
                background-color: #687d31;
                min-height: 100vh;
                background-image: url('https://i.pinimg.com/1200x/61/94/58/61945810e068dbcc17ac4818134327de.jpg');
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
                max-width: 900px;
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
                padding: 25px;
                border-radius: 15px;
                margin-bottom: 30px;
            }}

            .form-group {{
                margin-bottom: 20px;
            }}

            .form-label {{
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
                color: #19350c;
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

            .form-textarea {{
                width: 100%;
                padding: 12px;
                border: 2px solid #19350c;
                border-radius: 10px;
                background-color: white;
                color: #19350c;
                font-size: 16px;
                min-height: 120px;
                resize: vertical;
                box-sizing: border-box;
                font-family: Arial, sans-serif;
            }}

            .form-select {{
                width: 100%;
                padding: 12px;
                border: 2px solid #19350c;
                border-radius: 10px;
                background-color: white;
                color: #19350c;
                font-size: 16px;
                box-sizing: border-box;
            }}

            .form-input:focus,
            .form-textarea:focus,
            .form-select:focus {{
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

            .posts-list {{
                display: grid;
                gap: 20px;
            }}

            .post-card {{
                background-color: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                border-left: 5px solid #19350c;
                transition: transform 0.3s ease;
            }}

            .post-card:hover {{
                transform: translateY(-3px);
            }}

            .post-header {{
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 15px;
                border-bottom: 2px solid #e8f5e8;
                padding-bottom: 10px;
            }}

            .post-header h3 {{
                margin: 0;
                color: #19350c;
                font-size: 1.4em;
                flex: 1;
            }}

            .post-author {{
                background-color: #687d31;
                color: white;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.9em;
                font-weight: bold;
                margin-left: 15px;
            }}

            .post-content {{
                color: #333;
                line-height: 1.6;
                margin-bottom: 15px;
            }}

            .post-content p {{
                margin: 0;
            }}

            .post-footer {{
                color: #666;
                font-size: 0.9em;
                border-top: 1px solid #e8f5e8;
                padding-top: 10px;
            }}

            .empty-state {{
                text-align: center;
                color: #666;
                padding: 40px;
                background-color: rgba(255, 255, 255, 0.5);
                border-radius: 15px;
            }}

            @media (max-width: 768px) {{
                .post-header {{
                    flex-direction: column;
                }}
                
                .post-author {{
                    margin-left: 0;
                    margin-top: 10px;
                    align-self: flex-start;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="overlay"></div>
        <div class="container">
            <a href="/" class="back-link">← Назад на главную</a>
            
            <div class="content-box">
                <h1>📄 Управление постами</h1>
                
                <div class="create-form">
                    <h3>Создать новый пост</h3>
                    <div class="form-group">
                        <label class="form-label" for="title">Заголовок поста:</label>
                        <input type="text" id="title" class="form-input" placeholder="Введите заголовок поста">
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="content">Текст поста:</label>
                        <textarea id="content" class="form-textarea" placeholder="Введите текст поста"></textarea>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="author_id">Выберите автора:</label>
                        <select id="author_id" class="form-select">
                            <option value="">-- Выберите автора --</option>
                            {users_options}
                        </select>
                    </div>
                    <button class="submit-btn" onclick="createPost()">📝 Создать пост</button>
                </div>

                <h3>Список постов:</h3>
                <div class="posts-list">
                    {posts_html if posts_html else '<div class="empty-state">📭 Постов пока нет</div>'}
                </div>
            </div>
        </div>

        <script>
            async function createPost() {{
                const title = document.getElementById('title').value;
                const content = document.getElementById('content').value;
                const author_id = document.getElementById('author_id').value;
                
                if (!title || !content) {{
                    alert('Пожалуйста, заполните заголовок и текст поста');
                    return;
                }}

                if (!author_id) {{
                    alert('Пожалуйста, выберите автора');
                    return;
                }}

                const response = await fetch('/api/posts?title=' + encodeURIComponent(title) + '&content=' + encodeURIComponent(content) + '&author_id=' + encodeURIComponent(author_id), {{
                    method: 'POST'
                }});
                
                if (response.ok) {{
                    alert('Пост успешно создан!');
                    location.reload();
                }} else {{
                    alert('Ошибка при создании поста');
                }}
            }}

            // Добавляем обработчики нажатия Enter
            document.addEventListener('DOMContentLoaded', function() {{
                document.getElementById('title').addEventListener('keypress', function(e) {{
                    if (e.key === 'Enter') createPost();
                }});
            }});
        </script>
    </body>
    </html>
    """)

@router.post("/api/posts")
def create_post_api(title: str, content: str, author_id: int):
    posts = read_data("posts.json")
    users = read_data("users.json")
    
    author_exists = any(user["id"] == author_id for user in users)
    if not author_exists:
        return {"error": "Автор не найден"}, 400
    
    new_post = {
        "id": len(posts) + 1,
        "title": title,
        "content": content,
        "author_id": author_id,
        "created_at": datetime.now().isoformat()
    }
    
    posts.append(new_post)
    save_data("posts.json", posts)
    
    return {"message": "Пост создан"}
