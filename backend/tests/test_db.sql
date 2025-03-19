-- 测试数据
INSERT INTO posts (post_id, subreddit, title, content, author, created_utc, url, score)
VALUES ('t3_test1', 'python', 'Test Post 1', 'Test Content 1', 'user1', 1647686400, 'http://reddit.com/t3_test1', 100),
       ('t3_test2', 'python', 'Test Post 2', 'Test Content 2', 'user2', 1647690000, 'http://reddit.com/t3_test2', 50);

INSERT INTO comments (comment_id, post_id, parent_id, author, content, created_utc, score, depth)
VALUES ('t1_comment1', 't3_test1', NULL, 'user3', 'Test Comment 1', 1647687400, 10, 0),
       ('t1_comment2', 't3_test1', 't1_comment1', 'user4', 'Test Comment 2', 1647688400, 5, 1);

INSERT INTO analysis_results (post_id, analysis_type, result_text, model_version, timestamp, parameters)
VALUES ('t3_test1', 'sentiment', 'Positive sentiment', 'deepseek-chat', 1647689400, '{"temperature": 0.7}');