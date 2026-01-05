server {
    listen 80;
    listen [::]:80; 
    server_name skiptheboringbits.com;

    # Bloque de Proxy Inverso para n8n
    location /n8n/ {
        # CRÍTICO: Remueve el /n8n/ del URI antes de enviarlo a Docker [cite: 2]
        rewrite ^/n8n/(.*) /$1 break;
        
        # El proxy pasa la solicitud al puerto 5678 del contenedor Docker [cite: 3]
        proxy_pass http://localhost:5678; 

        # Encabezados esenciales [cite: 4, 5]
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https; 
        
        # Encabezados para WebSockets [cite: 6]
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_buffering off;
    }

    # NUEVO: Bloque de Proxy Inverso para SEO Audit
    location /seo-audit/ {
        # Redirige el tráfico al puerto 5000 de tu nuevo contenedor
        # El "/" final es vital para que la app reciba la ruta limpia
        proxy_pass http://127.0.0.1:5000/; 

        # Encabezados de red necesarios para identificar al usuario
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https; 

        # Soporte para aplicaciones modernas y carga de datos en tiempo real
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Aumentamos los tiempos de espera porque las auditorías SEO son lentas
        proxy_read_timeout 600s;
        proxy_send_timeout 600s;
    }
    
    # Bloque para la raíz del dominio
    location / {
        # Si tienes una web en el root, déjala aquí. [cite: 7]
        try_files $uri $uri/ =404; 
    }
}