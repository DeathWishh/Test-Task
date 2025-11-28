use serde::{Deserialize, Serialize};
use warp::Filter;
use rusqlite::{params, Connection, OptionalExtension};
use std::sync::Arc;
use tokio::sync::Mutex;
use std::convert::Infallible;

type Db = Arc<Mutex<Connection>>;

#[derive(Debug, Serialize, Deserialize)]
struct User {
    id: Option<i64>,
    name: String,
    email: String,
}

#[derive(Serialize)]
struct ApiResponse<T> {
    success: bool,
    data: T,
}

// Кастомные ошибки
#[derive(Debug)]
struct ValidationError(&'static str);

impl warp::reject::Reject for ValidationError {}

#[tokio::main]
async fn main() {
    // Инициализация in-memory SQLite базы данных
    let conn = Connection::open_in_memory().expect("Failed to create database");
    init_db(&conn).expect("Failed to initialize database");
    let db = Arc::new(Mutex::new(conn));

    // Маршруты
    let health_route = warp::path!("health")
        .map(|| warp::reply::json(&ApiResponse { success: true, data: "OK" }));

    let get_users_route = warp::path!("users")
        .and(warp::get())
        .and(with_db(db.clone()))
        .and_then(get_users);

    let create_user_route = warp::path!("users")
        .and(warp::post())
        .and(warp::body::json())
        .and(with_db(db.clone()))
        .and_then(create_user);

    let get_user_route = warp::path!("users" / i64)
        .and(warp::get())
        .and(with_db(db.clone()))
        .and_then(get_user_by_id);

    let delete_user_route = warp::path!("users" / i64)
        .and(warp::delete())
        .and(with_db(db.clone()))
        .and_then(delete_user);

    let routes = health_route
        .or(get_users_route)
        .or(create_user_route)
        .or(get_user_route)
        .or(delete_user_route)
        .with(warp::cors().allow_any_origin())
        .recover(handle_rejection);

    println!("Server started at http://localhost:8080");
    warp::serve(routes).run(([127, 0, 0, 1], 8080)).await;
}

fn with_db(db: Db) -> impl Filter<Extract = (Db,), Error = Infallible> + Clone {
    warp::any().map(move || db.clone())
}

// Инициализация БД
fn init_db(conn: &Connection) -> rusqlite::Result<()> {
    conn.execute(
        "CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )",
        [],
    )?;
    
    // Добавим тестовые данные
    conn.execute(
        "INSERT INTO users (name, email) VALUES (?1, ?2)",
        params!["Alice", "alice@example.com"],
    )?;
    
    conn.execute(
        "INSERT INTO users (name, email) VALUES (?1, ?2)",
        params!["Bob", "bob@example.com"],
    )?;
    
    Ok(())
}

// Валидация email
fn validate_email(email: &str) -> bool {
    email.contains('@') && email.contains('.')
}

// Обработчики
async fn get_users(db: Db) -> Result<impl warp::Reply, warp::Rejection> {
    let conn = db.lock().await;
    let mut stmt = conn.prepare("SELECT id, name, email FROM users").map_err(|e| {
        eprintln!("Database error: {}", e);
        warp::reject::custom(ValidationError("Database error"))
    })?;
    
    let users_iter = stmt.query_map([], |row| {
        Ok(User {
            id: Some(row.get(0)?),
            name: row.get(1)?,
            email: row.get(2)?,
        })
    }).map_err(|e| {
        eprintln!("Database error: {}", e);
        warp::reject::custom(ValidationError("Database error"))
    })?;

    let users: Result<Vec<_>, _> = users_iter.collect();
    let users = users.map_err(|e| {
        eprintln!("Database error: {}", e);
        warp::reject::custom(ValidationError("Database error"))
    })?;

    Ok(warp::reply::json(&ApiResponse {
        success: true,
        data: users,
    }))
}

async fn create_user(user: User, db: Db) -> Result<impl warp::Reply, warp::Rejection> {
    // Валидация
    if user.name.is_empty() {
        return Err(warp::reject::custom(ValidationError("Name cannot be empty")));
    }
    if !validate_email(&user.email) {
        return Err(warp::reject::custom(ValidationError("Invalid email format")));
    }

    let conn = db.lock().await;
    let result = conn.execute(
        "INSERT INTO users (name, email) VALUES (?1, ?2)",
        params![&user.name, &user.email],
    );

    match result {
        Ok(_) => Ok(warp::reply::json(&ApiResponse {
            success: true,
            data: "User created",
        })),
        Err(e) => {
            if e.to_string().contains("UNIQUE constraint failed") {
                Err(warp::reject::custom(ValidationError("Email already exists")))
            } else {
                eprintln!("Database error: {}", e);
                Err(warp::reject::custom(ValidationError("Database error")))
            }
        }
    }
}

async fn get_user_by_id(id: i64, db: Db) -> Result<impl warp::Reply, warp::Rejection> {
    let conn = db.lock().await;
    let user = conn
        .query_row(
            "SELECT id, name, email FROM users WHERE id = ?1",
            [id],
            |row| {
                Ok(User {
                    id: Some(row.get(0)?),
                    name: row.get(1)?,
                    email: row.get(2)?,
                })
            },
        )
        .optional()
        .map_err(|e| {
            eprintln!("Database error: {}", e);
            warp::reject::custom(ValidationError("Database error"))
        })?;

    match user {
        Some(user) => Ok(warp::reply::json(&ApiResponse {
            success: true,
            data: user,
        })),
        None => Err(warp::reject::not_found()),
    }
}

async fn delete_user(id: i64, db: Db) -> Result<impl warp::Reply, warp::Rejection> {
    let conn = db.lock().await;
    let changes = conn
        .execute("DELETE FROM users WHERE id = ?1", [id])
        .map_err(|e| {
            eprintln!("Database error: {}", e);
            warp::reject::custom(ValidationError("Database error"))
        })?;

    if changes > 0 {
        Ok(warp::reply::json(&ApiResponse {
            success: true,
            data: "User deleted",
        }))
    } else {
        Err(warp::reject::not_found())
    }
}

// Обработка ошибок
async fn handle_rejection(err: warp::Rejection) -> Result<impl warp::Reply, Infallible> {
    let (code, message) = if err.is_not_found() {
        (warp::http::StatusCode::NOT_FOUND, "Not Found")
    } else if let Some(e) = err.find::<ValidationError>() {
        (warp::http::StatusCode::BAD_REQUEST, e.0)
    } else if let Some(_) = err.find::<warp::reject::MethodNotAllowed>() {
        (warp::http::StatusCode::METHOD_NOT_ALLOWED, "Method Not Allowed")
    } else {
        eprintln!("Unhandled rejection: {:?}", err);
        (warp::http::StatusCode::INTERNAL_SERVER_ERROR, "Internal Server Error")
    };

    Ok(warp::reply::with_status(
        warp::reply::json(&ApiResponse::<&str> {
            success: false,
            data: message,
        }),
        code,
    ))
}