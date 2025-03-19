-- database/schema.sql
-- 启用外键约束
PRAGMA
foreign_keys = ON;

DROP TABLE IF EXISTS analysis_results;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS posts;

-- 帖子表
CREATE TABLE posts
(
    post_id     TEXT PRIMARY KEY,
    subreddit   TEXT    NOT NULL,
    title       TEXT    NOT NULL,
    content     TEXT,
    key_words   TEXT,
    author      TEXT    NOT NULL,
    created_utc INTEGER NOT NULL,
    fetched_at  INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    url         TEXT,
    score       INTEGER          DEFAULT 0,
    UNIQUE (post_id)
);

-- 评论表
CREATE TABLE comments
(
    comment_id  TEXT PRIMARY KEY,
    post_id     TEXT    NOT NULL,
    parent_id   TEXT,
    author      TEXT    NOT NULL,
    content     TEXT    NOT NULL,
    created_utc INTEGER NOT NULL,
    score       INTEGER DEFAULT 0,
    depth       INTEGER DEFAULT 0,
    FOREIGN KEY (post_id) REFERENCES posts (post_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES comments (comment_id),
    UNIQUE (comment_id)
);

-- 分析结果表
CREATE TABLE analysis_results
(
    result_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id       TEXT    NOT NULL,
    analysis_type TEXT    NOT NULL,
    result_text   TEXT    NOT NULL,
    model_version TEXT    NOT NULL,
    timestamp     INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    parameters    TEXT,
    FOREIGN KEY (post_id) REFERENCES posts (post_id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_posts_created_utc ON posts(created_utc);
CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id);
CREATE INDEX IF NOT EXISTS idx_analysis_post_id ON analysis_results(post_id);


