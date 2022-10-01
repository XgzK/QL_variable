-- 如果这个表存在则删除
DROP TABLE IF EXISTS repeat;
CREATE TABLE `repeat` (
    `jd_value1` varchar(255) NOT NULL UNIQUE,
    `jd_data` varchar(25) NOT NULL
);