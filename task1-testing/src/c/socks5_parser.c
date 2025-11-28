#include "socks5_parser.h"
#include <string.h>
#include <arpa/inet.h>

int parse_socks5_handshake(const uint8_t* data, size_t len, socks5_handshake_t* handshake) 
{
    if (!data || !handshake || len < 3) return -1;
    
    handshake->version = data[0];
    if (handshake->version != 0x05) return -2;
    
    handshake->nmethods = data[1];
    if (handshake->nmethods == 0 || handshake->nmethods > 255) return -3;
    if (len < (size_t)(2 + handshake->nmethods)) return -4;
    
    memcpy(handshake->methods, &data[2], handshake->nmethods);
    return 0;
}

int parse_socks5_request(const uint8_t* data, size_t len, socks5_request_t* request) 
{
    if (!data || !request) return -1;
    if (len < 4) return -1;
    
    request->version = data[0];
    request->cmd = data[1];
    request->rsv = data[2];
    request->atyp = data[3];
    
    size_t offset = 4;
    
    switch (request->atyp) {
        case 0x01: // IPv4
            if (len < offset + 4 + 2) return -2;
            memcpy(request->dst_addr.ipv4.addr, &data[offset], 4);
            offset += 4;
            break;
            
        case 0x03: // Domain name
            if (len < offset + 1) return -3;
            request->dst_addr.domain.len = data[offset];
            offset += 1;
            
            if (request->dst_addr.domain.len == 0 || request->dst_addr.domain.len > 254) 
                return -4;
            if (len < offset + request->dst_addr.domain.len + 2) return -5;
            
            memcpy(request->dst_addr.domain.name, &data[offset], request->dst_addr.domain.len);
            offset += request->dst_addr.domain.len;
            break;
            
        case 0x04: // IPv6
            if (len < offset + 16 + 2) return -6;
            memcpy(request->dst_addr.ipv6.addr, &data[offset], 16);
            offset += 16;
            break;
            
        default:
            return -7;
    }
    
    // Parse port safely
    if (len < offset + 2) return -8;
    uint16_t port;
    memcpy(&port, &data[offset], 2);
    request->dst_port = ntohs(port);
    
    return 0;
}
