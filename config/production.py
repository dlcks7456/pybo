from config.default import *
# 보통 서버 환경을 production 환경이라고 하므로 파일 이름을 server가 아니라 production으로 지었다.

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
# python -c "import os; print(os.urandom(16))"
SECRET_KEY = b'e\x9dX\xf9\x81\xf2\xe81\x95\xc3\xa3\x88\xc3u\x90\xc1'


