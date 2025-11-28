#ifndef SOCKS5_PARSER_H
#define SOCKS5_PARSER_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

// Структуры для разобранных данных
typedef struct {
    uint8_t version;
    uint8_t nmethods;
    uint8_t methods[255];
} socks5_handshake_t;

typedef struct {
    uint8_t len;
    uint8_t name[255];
} socks5_domain_t;

typedef struct {
    uint8_t version;
    uint8_t cmd;
    uint8_t rsv;
    uint8_t atyp;
    union {
        struct { uint8_t addr[4]; } ipv4;
        struct { uint8_t addr[16]; } ipv6;
        socks5_domain_t domain;
    } dst_addr;
    uint16_t dst_port;
} socks5_request_t;

// Функции парсинга
int parse_socks5_handshake(const uint8_t* data, size_t len, socks5_handshake_t* handshake);
int parse_socks5_request(const uint8_t* data, size_t len, socks5_request_t* request);

#endif
