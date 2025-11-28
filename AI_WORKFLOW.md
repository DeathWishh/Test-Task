# Документация процесса

## Описание

Для выполнения тестового задания использовалась ОС Ubuntu 24.04.3 desktop, которая была развернута в виртуальной машине с помощью VirtualBox.

### Выбор программы для задач 1-2

Для первой и второй задачи хотелось использовать такую программу, которое имеет отношение к работе, соответсвтенно 
сразу были выбраны языки Си и Python. У меня не было на примете такой программы, поэтому при помощью AI такой код был 
сгенерирован. AI предложил несколько вариантов, среди которых был очень простой прокси-сервер с socks5, я его и выбрал. 
Данная программа по сути состоит из двух вещей - код на Си компилируется в отдельную библиотеку и представляет собой 
функционал парсинга данных, пришедших от клиента, Python же управляет подключениями и всем остальным. Да, может быть 
пример кода и разделения на функции не самый удачный, но показывает простую интеграцию кода Си в Python, а так же это
позволило покрыть тестами все случаи. 

### Выбор языка для задачи 3

Для последней задачи был выбран язык Rust, так как в последнее время он набирает всё большую популярность и
я хотел к нему уже давно приобщиться.

## Файловая структура тестового задания

```bash
test-task/
├── task1-testing/                 	   # Задача 1: Тестирование
│	├── src/                           # Исходный код основного приложения
│   │	├── c/                         # C компонент (библиотека)
│   │	│   ├── socks5_parser.h        # Заголовочный файл
│   │	│   ├── socks5_parser.c        # Реализация парсера
│	│	│	├──	libsocks5_parser.so	   # Скомпилированная Си библиотека
│	│	│	├──	socks5_parser.o		   # Объектный файл, созданный компилятором
│   │	│   └── Makefile               # Для сборки C библиотеки
│   │	│
│   │	└── python/                    # Python компонент
│   │	    ├──	__init__.py			   # Заглушка
│   │	    ├── socks5_proxy.py        # Основной прокси-сервер
│   │	    ├── socks5_native.py       # Python обертка для C библиотеки
│   │	    └── main.py                # Точка входа    
│	│
│	└──	tests/
│		├── unit/
│		│   ├── test_socks5_parser.py    	# Unit-тесты C библиотеки, включаяя edge cases
│		│   └── test_proxy_logic.py      	# Unit-тесты Python логики, включаяя error handling
│		├── integration/
│		│   └── test_proxy_integration.py 	# Интеграционные тесты
│		├── performance/
│		│   └── test_performance.py      	# Performance тесты
│		├── conftest.py                  	# Общие фикстуры
│  		└── test_client.py         			# Простой код клиента, чтобы самому посмотреть сервер в работе
│
├── task2-documentation/           # Задача 2: Документация
│   ├── readme.md                  # Основная документация
│   ├── api_reference.md           # API документация
│   ├── usage_examples.md          # Примеры использования
│   └── troubleshooting.md         # Решение проблем
│
├── task3-unknown-language/        # Задача 3: Незнакомый язык
│   ├── Cargo.toml                 # Список Rust зависимостей
│   ├── Cargo.lock                 # Информация о версиях Rust зависимостей
│   ├── src/					   
│   │   └── main.rs                # Код HTTP-сервера на Rust
|	├──	target/					   # Папка с собранным приложением на Rust
│   └── README.md                  # Документация Rust приложения, включая установку Rust и сборку приложения
│
├── AI_WORKFLOW.md                 # Документация процесса
├── Makefile                       # Основной Makefile
└── .gitignore					   # Файл gitignore для Git
```

## Выбор AI и анализ сильных/слабых сторон

Для всех задач использовался DeepSeek. На мой взгляд и по моему мнению, он именно что заточен под программирование и генерирует только необходимый код, редко
ошибается и отлично разбирается в Linux, а так же у него большое контекстное окно, что позволяет запоминать много информации в одном чате.
Но DeepSeek порой через чур оптимистичен, в том смысле, что многие очень сложные задачи может посчитать выполнимыми для простых пользователей за малое время и
часто даёт на это добро, но это не проблема, если иметь критическое мышление и оценивать свои силы. Тогда как ChatGPT более критично оценивает силы пользователя и
чаще предупреждает. Ну и несоменный плюс DeepSeek в том, что он полностью бесплатен и без проблем работет на территории РФ. Но для кодинга в последнее время ChatGPT 
я редко использую, в бесплатной версии он порой пишет плохой код, который часто нужно править и в платной версии тоже бывают проблемы. 
ChatGPT идеален для креативных задач, например что-то сочинить, придумать, для задач общего назначения, например задать вопрос не по программированию, и для мультимедийных, 
например для разбора изображений. В ChatGPT вероятно больше знаний из разных сфер, поэтому если надо решить что-то экзотическое или креативное, с небольшим погружением в 
технические детали, то возможно это лучший выбор. Claude так же хорошо справляется с кодом, как и DeepSeek, но часто пишет код объёмно и многословно, что может быть 
сложно читать, особенно в сложных задачах, когда надо быстро вникнуть, тогда как DeepSeek скорее всего напишет код проще и понятнее для человека, который не знаком с 
темой. Но там, где DeepSeek может не справиться, я бы сначала попробовал Claude, и потом ChatGPT.

## История промтов

### Задача 1: Тестирование приложения

```
Придумай несколько простых вариантов проекта какой-нибудь backend программы, возможно сервера, который будет 
создавать тунель или перенаправлять трафик и предоставляет высоконагруженный API, используя сетевое и системное 
программирование, с подключением множества клиентов. Сам код пока писать не надо. 
```

```
Хорошие варианты, я выбрал вариант 3, сгенерируй минимально работающий код программы используя C и Pyhton. 
Какие части писать на Pyhton, а какие на C, выбор остаётся за тобой.
```

```
Слушай, а ты можешь объяснить в чём смысл компонента для C части?
```

```
Понял, то-есть C часть выступает в качестве библиотеки, которую мы используем в python.
```

```
Как теперь будет выглядеть структура проекта с C и python частью? Так же перепроверь код и посмотри, что нет ли ошибок.
```

```
Я внёс твои правки, которые ты предложил. Теперь мне нужно для этого приложения написать тесты:

1) Unit тесты основных функций
2) Интеграционные тесты API
3) Edge cases и error handling
4) Performance тесты (если применимо)
```

```
Я попробовал запустить тесты, но часть Unit тестов падает, вот вывод терминала:

vboxuser@Ubuntu:~/Downloads/socks5-proxy-test/task1-testing/tests$ python3 run_tests.py
🔬 Running SOCKS5 Proxy Tests...

📋 Running Unit Tests...
================================================= test session starts ==================================================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/vboxuser/Downloads/socks5-proxy-test/task1-testing
collected 19 items                                                                                                     

tests/unit/test_proxy_logic.py::TestProxyLogic::test_proxy_initialization PASSED                                 [  5%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_ipv4 PASSED                                  [ 10%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_domain PASSED                                [ 15%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_unsupported_atyp PASSED                      [ 21%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_connection_error PASSED                      [ 26%]
tests/unit/test_proxy_logic.py::TestErrorHandling::test_handle_client_invalid_handshake PASSED                   [ 31%]
tests/unit/test_proxy_logic.py::TestErrorHandling::test_handle_client_connection_reset PASSED                    [ 36%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_handshake_valid PASSED                                  [ 42%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_handshake_invalid_version PASSED                        [ 47%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_handshake_insufficient_data PASSED                      [ 52%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_ipv4 FAILED                                     [ 57%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_domain FAILED                                   [ 63%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_invalid_data PASSED                             [ 68%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_unsupported_atyp PASSED                         [ 73%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_handshake_multiple_methods PASSED                          [ 78%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_request_max_domain_length FAILED                           [ 84%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_request_domain_too_long PASSED                             [ 89%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_zero_length_domain PASSED                                  [ 94%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_valid_domain_min_length FAILED                             [100%]

__________________________________________ TestSocks5Parser.test_request_ipv4 __________________________________________
tests/unit/test_socks5_parser.py:45: in test_request_ipv4
    assert request.dst_port == 1080  # 0x0438 = 1080
E   assert 0 == 1080
E    +  where 0 = <socks5_native.Socks5Request object at 0x7cdf72216cd0>.dst_port
_________________________________________ TestSocks5Parser.test_request_domain _________________________________________
tests/unit/test_socks5_parser.py:58: in test_request_domain
    assert domain_str == 'example.com'
E   AssertionError: assert '' == 'example.com'
E     - example.com
_____________________________________ TestEdgeCases.test_request_max_domain_length _____________________________________
tests/unit/test_socks5_parser.py:95: in test_request_max_domain_length
    assert request.dst_addr.domain.len == 254
E   assert 97 == 254
E    +  where 97 = <socks5_native.Socks5Request.AddrUnion.Domain object at 0x7cdf723ddad0>.len
E    +    where <socks5_native.Socks5Request.AddrUnion.Domain object at 0x7cdf723ddad0> = <socks5_native.Socks5Request.AddrUnion object at 0x7cdf723de1d0>.domain
E    +      where <socks5_native.Socks5Request.AddrUnion object at 0x7cdf723de1d0> = <socks5_native.Socks5Request object at 0x7cdf723dcbd0>.dst_addr
______________________________________ TestEdgeCases.test_valid_domain_min_length ______________________________________
tests/unit/test_socks5_parser.py:125: in test_valid_domain_min_length
    assert success == True
E   assert False == True
=============================================== short test summary info ================================================
FAILED tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_ipv4 - assert 0 == 1080
FAILED tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_domain - AssertionError: assert '' == 'example.com'
FAILED tests/unit/test_socks5_parser.py::TestEdgeCases::test_request_max_domain_length - assert 97 == 254
FAILED tests/unit/test_socks5_parser.py::TestEdgeCases::test_valid_domain_min_length - assert False == True
============================================= 4 failed, 15 passed in 0.45s =============================================
❌ Unit tests failed!
```

```
Так, ну я добавил предложенные тобой исправления в socks5_parser.c, изменил Domain в socks5_native.py и обновил функцию чтения домена в тестах и вот вывод в терминале:

vboxuser@Ubuntu:~/Downloads/socks5-proxy-test/task1-testing/tests$ python3 run_tests.py
🔬 Running SOCKS5 Proxy Tests...

📋 Running Unit Tests...
========================================= test session starts =========================================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/vboxuser/Downloads/socks5-proxy-test/task1-testing
collected 19 items                                                                                    

tests/unit/test_proxy_logic.py::TestProxyLogic::test_proxy_initialization PASSED                [  5%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_ipv4 PASSED                 [ 10%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_domain PASSED               [ 15%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_unsupported_atyp PASSED     [ 21%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_connection_error PASSED     [ 26%]
tests/unit/test_proxy_logic.py::TestErrorHandling::test_handle_client_invalid_handshake PASSED  [ 31%]
tests/unit/test_proxy_logic.py::TestErrorHandling::test_handle_client_connection_reset PASSED   [ 36%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_handshake_valid PASSED                 [ 42%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_handshake_invalid_version PASSED       [ 47%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_handshake_insufficient_data PASSED     [ 52%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_ipv4 FAILED                    [ 57%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_domain FAILED                  [ 63%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_invalid_data PASSED            [ 68%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_unsupported_atyp PASSED        [ 73%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_handshake_multiple_methods PASSED         [ 78%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_request_max_domain_length FAILED          [ 84%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_request_domain_too_long FAILED            [ 89%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_zero_length_domain PASSED                 [ 94%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_valid_domain_min_length FAILED            [100%]

============================================== FAILURES ===============================================
_________________________________ TestSocks5Parser.test_request_ipv4 __________________________________
tests/unit/test_socks5_parser.py:45: in test_request_ipv4
    assert request.dst_port == 1080  # 0x0438 = 1080
E   assert 0 == 1080
E    +  where 0 = <socks5_native.Socks5Request object at 0x76233e422cd0>.dst_port
________________________________ TestSocks5Parser.test_request_domain _________________________________
tests/unit/test_socks5_parser.py:61: in test_request_domain
    assert domain_str == 'example.com'
E   AssertionError: assert '' == 'example.com'
E     - example.com
____________________________ TestEdgeCases.test_request_max_domain_length _____________________________
tests/unit/test_socks5_parser.py:98: in test_request_max_domain_length
    assert request.dst_addr.domain.len == 254
E   assert 97 == 254
E    +  where 97 = <socks5_native.Socks5Request.AddrUnion.Domain object at 0x76233e5ec250>.len
E    +    where <socks5_native.Socks5Request.AddrUnion.Domain object at 0x76233e5ec250> = <socks5_native.Socks5Request.AddrUnion object at 0x76233e5edad0>.domain
E    +      where <socks5_native.Socks5Request.AddrUnion object at 0x76233e5edad0> = <socks5_native.Socks5Request object at 0x76233e5ed150>.dst_addr
_____________________________ TestEdgeCases.test_request_domain_too_long ______________________________
tests/unit/test_socks5_parser.py:115: in test_request_domain_too_long
    assert success == False
E   assert True == False
_____________________________ TestEdgeCases.test_valid_domain_min_length ______________________________
tests/unit/test_socks5_parser.py:130: in test_valid_domain_min_length
    assert success == True
E   assert False == True
======================================= short test summary info =======================================
FAILED tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_ipv4 - assert 0 == 1080
FAILED tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_domain - AssertionError: assert '' == 'example.com'
FAILED tests/unit/test_socks5_parser.py::TestEdgeCases::test_request_max_domain_length - assert 97 == 254
FAILED tests/unit/test_socks5_parser.py::TestEdgeCases::test_request_domain_too_long - assert True == False
FAILED tests/unit/test_socks5_parser.py::TestEdgeCases::test_valid_domain_min_length - assert False == True
==================================== 5 failed, 14 passed in 0.48s =====================================
❌ Unit tests failed!
```

```
Так, я вынес Socks5Domain отдельно, как ты говорил, а так же убедился, что библиотека перекомпилирована и похоже, что это небольшой прогресс, теперь проваливаются только 3 теста, а 16 проходят, вот текущий вывод в терминале:

vboxuser@Ubuntu:~/Downloads/socks5-proxy-test/task1-testing/tests$ python3 run_tests.py
🔬 Running SOCKS5 Proxy Tests...

📋 Running Unit Tests...
========================================= test session starts =========================================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/vboxuser/Downloads/socks5-proxy-test/task1-testing
collected 19 items                                                                                    

tests/unit/test_proxy_logic.py::TestProxyLogic::test_proxy_initialization PASSED                [  5%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_ipv4 PASSED                 [ 10%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_domain PASSED               [ 15%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_unsupported_atyp PASSED     [ 21%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_connection_error PASSED     [ 26%]
tests/unit/test_proxy_logic.py::TestErrorHandling::test_handle_client_invalid_handshake PASSED  [ 31%]
tests/unit/test_proxy_logic.py::TestErrorHandling::test_handle_client_connection_reset PASSED   [ 36%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_handshake_valid PASSED                 [ 42%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_handshake_invalid_version PASSED       [ 47%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_handshake_insufficient_data PASSED     [ 52%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_ipv4 FAILED                    [ 57%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_domain PASSED                  [ 63%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_invalid_data PASSED            [ 68%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_unsupported_atyp PASSED        [ 73%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_handshake_multiple_methods PASSED         [ 78%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_request_max_domain_length PASSED          [ 84%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_request_domain_too_long FAILED            [ 89%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_zero_length_domain PASSED                 [ 94%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_valid_domain_min_length FAILED            [100%]
============================================== FAILURES ===============================================
_________________________________ TestSocks5Parser.test_request_ipv4 __________________________________
tests/unit/test_socks5_parser.py:44: in test_request_ipv4
    assert list(request.dst_addr.ipv4.addr) == [127, 0, 0, 1]
E   AttributeError: 'c_ubyte_Array_4' object has no attribute 'addr'
_____________________________ TestEdgeCases.test_request_domain_too_long ______________________________
tests/unit/test_socks5_parser.py:115: in test_request_domain_too_long
    assert success == False
E   assert True == False
_____________________________ TestEdgeCases.test_valid_domain_min_length ______________________________
tests/unit/test_socks5_parser.py:130: in test_valid_domain_min_length
    assert success == True
E   assert False == True
======================================= short test summary info =======================================
FAILED tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_ipv4 - AttributeError: 'c_ubyte_Array_4' object has no attribute 'addr'
FAILED tests/unit/test_socks5_parser.py::TestEdgeCases::test_request_domain_too_long - assert True == False
FAILED tests/unit/test_socks5_parser.py::TestEdgeCases::test_valid_domain_min_length - assert False == True
==================================== 3 failed, 16 passed in 0.40s =====================================
❌ Unit tests failed!
```

```
Да, юнит тесты проходят теперь все, теперь давай разберёмся с интеграционными тестами:

🔗 Running Integration Tests...
========================================= test session starts =========================================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/vboxuser/Downloads/socks5-proxy-test/task1-testing
collected 3 items                                                                                     

tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_socks5_handshake_integration FAILED [ 33%]
tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_socks5_connect_request_integration FAILED [ 66%]
tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_multiple_concurrent_connections FAILED [100%]

============================================== FAILURES ===============================================
____________________ TestSocks5ProxyIntegration.test_socks5_handshake_integration _____________________
tests/integration/test_proxy_integration.py:38: in test_socks5_handshake_integration
    sock.connect((host, port))
E   ConnectionRefusedError: [Errno 111] Connection refused
---------------------------------------- Captured stdout setup ----------------------------------------
SOCKS5 proxy listening on 127.0.0.1:0
_________________ TestSocks5ProxyIntegration.test_socks5_connect_request_integration __________________
tests/integration/test_proxy_integration.py:57: in test_socks5_connect_request_integration
    sock.connect((host, port))
E   ConnectionRefusedError: [Errno 111] Connection refused
---------------------------------------- Captured stdout setup ----------------------------------------
SOCKS5 proxy listening on 127.0.0.1:0
___________________ TestSocks5ProxyIntegration.test_multiple_concurrent_connections ___________________
tests/integration/test_proxy_integration.py:112: in test_multiple_concurrent_connections
    assert all(results), "Not all connections were successful"
E   AssertionError: Not all connections were successful
E   assert False
E    +  where False = all([False, False, False, False, False])
---------------------------------------- Captured stdout setup ----------------------------------------
SOCKS5 proxy listening on 127.0.0.1:0
---------------------------------------- Captured stdout call -----------------------------------------
Connection 0 failed: [Errno 111] Connection refused
Connection 1 failed: [Errno 111] Connection refused
Connection 2 failed: [Errno 111] Connection refused
Connection 3 failed: [Errno 111] Connection refused
Connection 4 failed: [Errno 111] Connection refused
======================================= short test summary info =======================================
FAILED tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_socks5_handshake_integration - ConnectionRefusedError: [Errno 111] Connection refused
FAILED tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_socks5_connect_request_integration - ConnectionRefusedError: [Errno 111] Connection refused
FAILED tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_multiple_concurrent_connections - AssertionError: Not all connections were successful
========================================== 3 failed in 0.66s ==========================================
❌ Integration tests failed!
```

```
Так, теперь вроде как осталось два интеграционных теста, которые не проходят:

🔗 Running Integration Tests...
========================================= test session starts =========================================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/vboxuser/Downloads/socks5-proxy-test/task1-testing
collected 4 items                                                                                     

tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_socks5_handshake_integration PASSED [ 25%]
tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_socks5_connect_request_integration FAILED [ 50%]
tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_multiple_concurrent_connections PASSED [ 75%]
tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_proxy_actual_connection FAILED [100%]

============================================== FAILURES ===============================================
_________________ TestSocks5ProxyIntegration.test_socks5_connect_request_integration __________________
tests/integration/test_proxy_integration.py:76: in test_socks5_connect_request_integration
    assert len(response) == 10
E   AssertionError: assert 0 == 10
E    +  where 0 = len(b'')
---------------------------------------- Captured stdout setup ----------------------------------------
SOCKS5 proxy listening on 127.0.0.1:50329
---------------------------------------- Captured stdout call -----------------------------------------
New connection from ('127.0.0.1', 57782)
Error handling client: cannot access local variable 'host' where it is not associated with a value
_______________________ TestSocks5ProxyIntegration.test_proxy_actual_connection _______________________
tests/integration/test_proxy_integration.py:137: in test_proxy_actual_connection
    assert response[0] == 5  # SOCKS5 version
E   IndexError: index out of range
---------------------------------------- Captured stdout setup ----------------------------------------
SOCKS5 proxy listening on 127.0.0.1:55455
---------------------------------------- Captured stdout call -----------------------------------------
New connection from ('127.0.0.1', 38356)
Error handling client: cannot access local variable 'host' where it is not associated with a value
======================================= short test summary info =======================================
FAILED tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_socks5_connect_request_integration - AssertionError: assert 0 == 10
FAILED tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_proxy_actual_connection - IndexError: index out of range
===================================== 2 failed, 2 passed in 2.44s =====================================
❌ Integration tests failed!
```

```
Так, я изменил test_proxy_logic.py, как ты посоветовал, но тесты не менял и вроде как теперь все тесты проходят успешно:

vboxuser@Ubuntu:~/Downloads/socks5-proxy-test/task1-testing/tests$ python3 run_tests.py
🔬 Running SOCKS5 Proxy Tests...

📋 Running Unit Tests...
========================================== test session starts ===========================================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/vboxuser/Downloads/socks5-proxy-test/task1-testing
collected 19 items                                                                                       

tests/unit/test_proxy_logic.py::TestProxyLogic::test_proxy_initialization PASSED                   [  5%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_ipv4 PASSED                    [ 10%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_domain PASSED                  [ 15%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_unsupported_atyp PASSED        [ 21%]
tests/unit/test_proxy_logic.py::TestProxyLogic::test_handle_connect_connection_error PASSED        [ 26%]
tests/unit/test_proxy_logic.py::TestErrorHandling::test_handle_client_invalid_handshake PASSED     [ 31%]
tests/unit/test_proxy_logic.py::TestErrorHandling::test_handle_client_connection_reset PASSED      [ 36%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_handshake_valid PASSED                    [ 42%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_handshake_invalid_version PASSED          [ 47%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_handshake_insufficient_data PASSED        [ 52%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_ipv4 PASSED                       [ 57%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_domain PASSED                     [ 63%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_invalid_data PASSED               [ 68%]
tests/unit/test_socks5_parser.py::TestSocks5Parser::test_request_unsupported_atyp PASSED           [ 73%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_handshake_multiple_methods PASSED            [ 78%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_request_max_domain_length PASSED             [ 84%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_request_domain_too_long PASSED               [ 89%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_zero_length_domain PASSED                    [ 94%]
tests/unit/test_socks5_parser.py::TestEdgeCases::test_valid_domain_min_length PASSED               [100%]

=========================================== 19 passed in 0.21s ===========================================

🔗 Running Integration Tests...
========================================== test session starts ===========================================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/vboxuser/Downloads/socks5-proxy-test/task1-testing
collected 4 items                                                                                        

tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_socks5_handshake_integration PASSED [ 25%]
tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_socks5_connect_request_integration PASSED [ 50%]
tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_multiple_concurrent_connections PASSED [ 75%]
tests/integration/test_proxy_integration.py::TestSocks5ProxyIntegration::test_proxy_actual_connection PASSED [100%]

=========================================== 4 passed in 2.60s ============================================

⚡️ Running Performance Tests...
========================================== test session starts ===========================================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/vboxuser/Downloads/socks5-proxy-test/task1-testing
collected 3 items                                                                                        

tests/performance/test_performance.py::TestPerformance::test_handshake_parsing_performance PASSED  [ 33%]
tests/performance/test_performance.py::TestPerformance::test_request_parsing_performance PASSED    [ 66%]
tests/performance/test_performance.py::TestPerformance::test_concurrent_parsing_performance PASSED [100%]

=========================================== 3 passed in 0.52s ============================================

✅ All tests completed successfully!
```

```
Хм, а как можно его поднять и просто проверить, идёт ли через него трафик? Ну то-есть посмотреть вне тестов как он работает. 
И желательно простым способом.
```

### Задача 2: Документация

```
Для моего приложения сгенерируй мне следующее:

1) README.md с установкой и запуском приложения.
2) API документацию для разработчиков.
3) Примеры использования приложения, то-есть как этим пользоваться.
4) А так же troubleshooting секцию.

И желательно всё писать по факту, без лишнего пафоса и в формате Markdown, если можно. И ещё, учитывай, 
что я это делаю под Ubuntu 24.04 и использую системные gcc и python3.
```

```
Ты не совсем точно сделал, для всех функций кода предоставь так же информацию о том, что подаётся на вход 
и что возвращается.
```

### Задача 3: Незнакомый язык

```
Привет, я новичок в Rust. Мне нужно создать пример HTTP-сервера, с 3-4 endpoints и добавь туда базовую 
валидацию входных данных. Так же интегрируй подключение к простой базе данных (SQLite/in-memory), чтобы 
она использовалась. Предоставь полный код на Rust, используя асинхронность (tokio). Код должен быть 
простым для понимания.
```

```
Хорошо, а надо ли это как-то собирать и как запустить скажем под Ubuntu?
```

```
Я попробовал поставить Rust через терминал, но команда:

"curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"

Возвращает следующее:

curl:56 Recv failure: Connection reset by peer
sh: 527: Syntax error: end of file unexpected (expecting ";;")
```

```
Смотри, во время команды cargo build произошла ошибка, у тебя есть идеи что это может быть?

Compiling webserver v0.1.0 (/home/vboxuser/Downloads/socks5-proxy-test/task3-unknown-language)
error[E0412]: cannot find type Infallible in crate warp
   --> src/main.rs:188:83
    |
188 | ...warp::Reply, warp::Infallible> {
    |                       ^^^^^^^^^^ not found in warp
    |
help: consider importing this enum
    |
1   + use std::convert::Infallible;
    |
help: if you import Infallible, refer to it directly
    |
188 - async fn handle_rejection(err: warp::Rejection) -> Result<impl warp::Reply, warp::Infallible> {
188 + async fn handle_rejection(err: warp::Rejection) -> Result<impl warp::Reply, Infallible> {
    |

error[E0412]: cannot find type NotFound in module warp::reject
   --> src/main.rs:197:40
    |
197 |     } else if err.find::<warp::reject::NotFound>().is_some() {
    |                                        ^^^^^^^^ not found in warp::reject
    |
help: there is an enum variant rusqlite::ErrorCode::NotFound and 3 others; try using the variant's enum
    |
197 |     } else if err.find::<rusqlite::ErrorCode>().is_some() {
    |                          ~~~~~~~~~~~~~~~
197 |     } else if err.find::<std::io::ErrorKind>().is_some() {
    |                          ~~~~~~~~~~~~~~
197 |     } else if err.find::<tokio::io::ErrorKind>().is_some() {
    |                          ~~~~~~~~~~~~~~~~

error[E0599]: the method run exists for struct Server<Recover<CorsFilter<Or<..., ...>>, ...>>, but its trait bounds were not satisfied
  --> src/main.rs:63:25
   |
63 |     warp::serve(routes).run(([127, 0, 0, 1], 8080)).await;
   |                         ^^^ method cannot be called on Server<Recover<CorsFilter<Or<..., ...>>, ...>> due to unsatisfied trait bounds
   |
  ::: /home/vboxuser/.cargo/registry/src/index.crates.io-6f17d22bba15001f/warp-0.3.7/src/filter/recover.rs:41:1
   |
41 | pub struct RecoverFuture<T: Filter, F>
   | -------------------------------------- doesn't satisfy <_ as Future>::Output = Result<(Either<(Either<(Preflight,), (Either<(Wrapped<(Either<(Either<(Either<(Either<(Json,), (impl Reply,)>,), (impl Reply,)>,), (impl Reply,)>,), (impl Reply,)>,)>,), (Either<(Either<(Either<(Either<(Json,), (impl Reply,)>,), (impl Reply,)>,), (impl Reply,)>,), (impl Reply,)>,)>,)>,), (impl Reply,)>,), {type error}>
   |
   = note: the full type name has been written to '/home/vboxuser/Downloads/socks5-proxy-test/task3-unknown-language/target/debug/deps/webserver-8d7dbba44b6ed97c.long-type-16948786121162695908.txt'
   = note: consider using --verbose to print the full type name to the console
   = note: the following trait bounds were not satisfied:
           {type error}: Sized
           {type error}: Sized
           which is required by impl Future<Output = Result<impl Reply, {type error}>>: futures_core::future::TryFuture
           {type error}: Sized
           which is required by
```