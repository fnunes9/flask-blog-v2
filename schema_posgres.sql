/* cria a tabela */
DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title CHAR(50) NOT NULL,
    content CHAR(100) NOT NULL
);

/* insere dados iniciais */
INSERT INTO posts(title, content) VALUES 
('First Post', 'Content for the first post');

INSERT INTO posts (title, content) VALUES 
('Second Post', 'Content for the second post');