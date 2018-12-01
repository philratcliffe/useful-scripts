gpg --status-fd=2 --enable-progress-filter --batch --verbose --with-colons --pinentry-mode=loopback \
--agent-program=/usr/bin/gpg-agent --dirmngr-program=/usr/bin/dirmngr \
--homedir=/home/phil/.local/share/Mailpile/default \
--personal-digest-preferences=SHA512 --digest-algo=SHA512 --cert-digest-algo=SHA512 --utf8-strings \
--keyserver http://eu.pool.sks-keyservers.net \
--keyserver-options ca-cert-file=/home/phil/projects/Mailpile/mailpile/crypto/gpgi.py \
--fingerprint --search-key mailpiletest@protonmail.com
