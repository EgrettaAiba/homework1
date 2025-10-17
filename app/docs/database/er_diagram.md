erDiagram
    users ||--o{ posts : author
    users ||--o{ comments : author
    users ||--o{ user_favorites : user
    users ||--o{ subscriptions : subscriber
    users ||--o{ subscriptions : target_user

    posts ||--o{ comments : post
    posts ||--o{ user_favorites : post
    posts }o--o{ categories : "many-to-many"
    comments ||--o{ comments : "self-reference"

    users {
        integer id PK
        varchar username UK
        varchar email UK
        varchar password_hash
        varchar first_name
        varchar last_name
        text bio
        varchar avatar_url
        timestamp created_at
        timestamp updated_at
        boolean is_active
    }

    posts {
        integer id PK
        varchar title
        varchar slug UK
        text content
        text excerpt
        integer author_id FK
        varchar status
        varchar featured_image
        timestamp created_at
        timestamp updated_at
        timestamp published_at
    }

    categories {
        integer id PK
        varchar name UK
        varchar slug UK
        text description
        timestamp created_at
    }

    post_categories {
        integer post_id PK,FK
        integer category_id PK,FK
        timestamp created_at
    }

    user_favorites {
        integer id PK
        integer user_id FK
        integer post_id FK
        timestamp created_at
    }

    comments {
        integer id PK
        text content
        integer author_id FK
        integer post_id FK
        integer parent_id FK
        timestamp created_at
        timestamp updated_at
        boolean is_edited
    }

    subscriptions {
        integer id PK
        integer subscriber_id FK
        integer target_user_id FK
        timestamp created_at
    }
