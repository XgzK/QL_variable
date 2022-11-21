-- 如果这个表存在则删除 --
DROP TABLE IF EXISTS repeat;
CREATE TABLE `repeat` (
    `jd_value1` varchar(255) NOT NULL UNIQUE,
    `jd_data` varchar(25) NOT NULL
);

-- 青龙数据库表 --
DROP TABLE IF EXISTS QL;
CREATE TABLE `QL` (
     `name` varchar(30) NOT NULL UNIQUE,
     `ip` varchar(30) NOT NULL,
     `Client_ID` varchar(25) NOT NULL,
     `Client_Secret` varchar(25) NOT NULL,
     `Authorization` varchar(25),
     `json` varchar(25) NOT NULL,
     `state` INT(1) not null
);
-- 别名
-- name: ""
-- # 设置自己青龙的IP:端口
-- ip: ""
-- # 下面和青龙有关 系统设置-->应用设置-->新建应用-->权限选择所有自己配置
-- Client ID: ""
-- Client Secret: ""
-- # 青龙类似于cookie，登录后自动获取，不用管,不能移动行
-- Authorization: ""
-- # 青龙任务保存路径
-- json: date/name.json
-- state 表示状态是否正常