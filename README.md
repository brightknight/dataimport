0 environment
    linux
    mysql
    python2.7 above
    testing for ubuntu 12.04

1 database structure
    data table: workdb.workitems_import
    colums:
      `id` int(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (`id`)
      `name` text COLLATE utf8_unicode_ci NOT NULL,
      `begindate` date NOT NULL,
      `enddate` date NOT NULL,
      `worktype` tinyint(4) NOT NULL,             // 1-个人工作, 2-项目进展
      `project` text COLLATE utf8_unicode_ci NOT NULL,
      `tasktype` text COLLATE utf8_unicode_ci NOT NULL,
      `plantype` tinyint(4) NOT NULL,             // 1-计划内, 0-else
      `taskname` text COLLATE utf8_unicode_ci NOT NULL,
      `content` text COLLATE utf8_unicode_ci NOT NULL,
      `status` int(11) NOT NULL,                  // 1 '1按时', 2 '2延期', 3 '3提前'
      `hours` int(11) NOT NULL,
      `diary` text COLLATE utf8_unicode_ci NOT NULL,
      `comment` text COLLATE utf8_unicode_ci NOT NULL,
    
2 configuration
    start.sh:
    path = xxx
    di.init(host='localhost',user='root',passwd='root')

