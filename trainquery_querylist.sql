CREATE TABLE `querylist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from` varchar(8) NOT NULL,
  `to` varchar(8) NOT NULL,
  `date` date NOT NULL,
  `number` varchar(64) DEFAULT NULL,
  `seat` varchar(80) DEFAULT NULL,
  `status` varchar(8) NOT NULL DEFAULT 'init',
  PRIMARY KEY (`id`),
  UNIQUE KEY `querylist_id_uindex` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8