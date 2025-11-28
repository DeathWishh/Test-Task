# Пример приложения с HTTP сервером и базой данных

## Описание

Для проекта был выбран язык Rust

## 1. Установка Rust и зависимостей

```bash
# Обновление пакетов в Ubuntu
sudo apt update
sudo apt upgrade -y

# Установка системных зависимостей для SQLite
sudo apt install -y libsqlite3-dev pkg-config build-essential

# Установка компилятора Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Проверка установки
rustc --version
cargo --version
```

#### Если следующая команда завершается неудачей:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

#### В таком случае можно попробовать установить вручную конкретную версию:

```bash
# Скачаем нужную версию (1.83.0)
wget https://static.rust-lang.org/dist/rust-1.83.0-x86_64-unknown-linux-gnu.tar.gz

# Распакуем
tar -xzf rust-1.83.0-x86_64-unknown-linux-gnu.tar.gz
cd rust-1.83.0-x86_64-unknown-linux-gnu

# Установим
sudo ./install.sh

# Проверим версию
rustc --version
cargo --version
```

#### Если после этого нет cargo, то:

```bash
# Установим
sudo apt install cargo

# Проверим версию
cargo --version
```

## 2. Создание проекта (это можно пропустить, используется только если создавать с нуля)

```bash
# Создаем новый проект
cargo new task3-unknown-language
cd task3-unknown-language

# Редактируем Cargo.toml
cat > Cargo.toml << 'EOF'
[package]
name = "webserver"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1.0", features = ["full"] }
warp = "0.3"
serde = { version = "1.0", features = ["derive"] }
rusqlite = "0.29"
EOF
```

## 3. Добавляем код (это можно пропустить, используется только если создавать с нуля)

```bash
# Копируем код в src/main.rs
# Можно использовать любой текстовый редактор:
nano src/main.rs
# или
vim src/main.rs
# или
code src/main.rs (если установлен VS Code)
```

## 4. Сборка и запуск

```bash
# Сборка в режиме отладки (быстрее для разработки)
cargo build

# Или сборка в режиме релиза (оптимизированная)
cargo build --release

# Запуск в режиме отладки
cargo run

# Или запуск собранного бинарника
./target/debug/webserver
# или для релизной версии
./target/release/webserver
```

## 5. Альтернативный способ - готовый скрипт для создания проекта

Создайте файл setup_and_run.sh:

```bash
#!/bin/bash

echo "Setting up Rust webserver on Ubuntu..."

# Проверка Rust
if ! command -v cargo &> /dev/null; then
    echo "Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source ~/.cargo/env
fi

# Установка зависимостей
sudo apt update
sudo apt install -y libsqlite3-dev pkg-config build-essential

# Создание проекта
cargo new task3-unknown-language
cd task3-unknown-language

# Создание Cargo.toml
cat > Cargo.toml << 'EOF'
[package]
name = "webserver"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1.0", features = ["full"] }
warp = "0.3"
serde = { version = "1.0", features = ["derive"] }
rusqlite = "0.29"
EOF

echo "Cargo.toml created successfully!"
echo "Now add the Rust code to src/main.rs and run: cargo run"
```

Сделайте его исполняемым и запустите:

```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

## 6. Тестирование сервера

Запуск:

```bash
# Запуск в режиме отладки
cargo run

# Или запуск собранного бинарника
./target/debug/webserver
# или для релизной версии
./target/release/webserver
```

После запуска сервера, откройте новое окно терминала и протестируйте:

```bash
# Проверка здоровья
curl http://localhost:8080/health

# Создание пользователя
curl -X POST -H "Content-Type: application/json" -d '{"name":"Alice","email":"alice@example.com"}' http://localhost:8080/users

# Получение всех пользователей
curl http://localhost:8080/users

# Получение пользователя по ID
curl http://localhost:8080/users/1

# Удаление пользователя
curl -X DELETE http://localhost:8080/users/1
```

## 7. Запуск в фоновом режиме (для продакшена)

```bash
# Сборка релизной версии
cargo build --release

# Запуск в фоне
nohup ./target/release/webserver > server.log 2>&1 &

# Проверка что сервер работает
curl http://localhost:8080/health

# Просмотр логов
tail -f server.log

# Остановка сервера (найти PID и убить)
ps aux | grep webserver
kill <PID>
```

## 8. Упрощенная версия для быстрого старта

Если нужно максимально простой запуск:

```bash
# Устанавливаем Rust как показано выше, затем:

cat > Cargo.toml << 'EOF'
[package]
name = "simple-server"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1", features = ["full"] }
warp = "0.3"
serde = { version = "1.0", features = ["derive"] }
rusqlite = "0.29"
EOF

cat > src/main.rs << 'EOF'
use warp::Filter;

#[tokio::main]
async fn main() {
    let hello = warp::path!("hello" / String)
        .map(|name| format!("Hello, {}!", name));

    let health = warp::path!("health")
        .map(|| "OK");

    let routes = hello.or(health);

    println!("Server starting at http://localhost:8080");
    warp::serve(routes).run(([127, 0, 0, 1], 8080)).await;
}
EOF

cargo run
```

Этот упрощенный сервер можно сразу протестировать:

```bash
curl http://localhost:8080/health
curl http://localhost:8080/hello/world
```

## 9. Возможные проблемы и решения

#### 1. Ошибка линковки с SQLite:

Переустановите:

```bash
sudo apt install -y libsqlite3-dev
```
#### 2. Порт занят:

Измените порт в коде с 8080 на другой (например, 8081)

#### 3. Проблемы с правами:

Измените права

```bash
chmod +x target/release/webserver
```

## 10. Возможности, особенности программы:

#### 1. Есть 5 разных endpoints на которые можно отправлять запросы:

- GET /health - проверка работоспособности
- GET /users - получить всех пользователей
- POST /users - создать пользователя
- GET /users/{id} - получить пользователя по ID
- DELETE /users/{id} - удалить пользователя

#### 2. Валидация:

- Проверка формата email
- Проверка уникальности email
- Проверка пустого имени

#### 3. База данных:

- In-memory SQLite
- Автоматическая инициализация таблицы
- Потокобезопасный доступ через Arc<Mutex>

#### 4. Обработка ошибок:

- Кастомные ошибки валидации
- Правильные HTTP-статусы
- JSON-ответы единого формата

#### 5. Асинхронность:

- Использование Tokio runtime
- Блокирующие операции БД выполняются в spawn_blocking