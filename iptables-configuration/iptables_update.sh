for i in `curl https://www.cloudflare.com/ips-v4`; do 
    iptables -I INPUT -p tcp -s $i --dport https -j ACCEPT; 
done
