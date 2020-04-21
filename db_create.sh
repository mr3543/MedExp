#!/bin/sh
sqlite3 med_db.db <<EOF
.read schema.sql
EOF

mongo <<EOF
use med_articles 
db.createCollection("articles_text")
db.articles_text.createIndex( { title:"text",text:"text" } )
EOF
