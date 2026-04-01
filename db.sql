CREATE DATABASE IF NOT EXISTS inventory_db DEFAULT CHARSET utf8mb4;
USE inventory_db;

-- 1. 用户表
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL UNIQUE,
  `password` varchar(100) NOT NULL,
  `role` varchar(20) DEFAULT 'user',
  `status` tinyint(1) DEFAULT 1 COMMENT '1正常 0禁用',
  PRIMARY KEY (`id`)
);

-- 2. 商品表
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`)
);

-- 3. 库存表
CREATE TABLE `inventory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL DEFAULT 0,
  `min_alert` int DEFAULT 10 COMMENT '最低阈值',
  `max_alert` int DEFAULT 1000 COMMENT '最高阈值',
  PRIMARY KEY (`id`),
  FOREIGN KEY (`product_id`) REFERENCES `products`(`id`)
);

-- 4. 采购订单表
CREATE TABLE `purchases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `status` varchar(20) DEFAULT '待审核' COMMENT '待审核/已审核/已入库',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`product_id`) REFERENCES `products`(`id`)
);

-- 5. 销售订单表
CREATE TABLE `sales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `status` varchar(20) DEFAULT '待发货' COMMENT '待发货/已发货',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`product_id`) REFERENCES `products`(`id`)
);

-- 6. 日志表
CREATE TABLE `logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(50) NOT NULL,
  `action` varchar(255) NOT NULL,
  `type` varchar(20) DEFAULT '操作' COMMENT '登录/操作',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

INSERT INTO `users` (`username`, `password`, `role`) VALUES ('admin', '123456', 'admin');
