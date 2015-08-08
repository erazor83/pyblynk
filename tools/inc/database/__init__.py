def createFromConf(conf):
	if conf['type']=='sqlite':
		import db_sqlite
		return db_sqlite.Database(conf['conf'])
