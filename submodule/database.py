import sqlite3

# connect = sqlite3.connect("./database/main.db", check_same_thread=False)
# cursor = connect.cursor()

authDB = sqlite3.connect("./database/auth.sql", check_same_thread=False)
authCursor = authDB.cursor()
"""
authDB에는 토큰 인증과 관련된 데이터들이 저장됩니다

[ auth ]
| token | forever | expire | permission |

token -> 토큰이 저장됩니다
forever -> 거짓(0)일 경우 초회 토큰 이용시 expire가 파라미터로 필요합니다
expire -> 만료되는 날짜를 datetime오브젝트를 텍스트로 기록합니다
~permission -> 참(1)일 경우에는 토큰의 추가가 가능합니다
"""

configDB = sqlite3.connect("./database/config.sql", check_same_thread=False)
configCursor = configDB.cursor()


"""
Tasks 등등 저장되는 곳입니다

[ tasks ]
| hash | data |
~hash -> 작업 고유의 번호를 부여받습니다
         추후에 절대 변하지 않습니다 ( 예외 있음 )
         hash값을 이용하여 다른 테이블 밑 데이터베이스와 교류합니다
~data -> 작업 정보입니다 다른 곳에 서술합니다

[ download & torrent ]
| hash | data |

[ thumbnail ]
| hash | data |
실질 썸네일은 다른 DB에 저장되기에 필요성 고민중
"""

userDB = sqlite3.connect("./database/user.sql", check_same_thread=False)
"""
유저의 환경설정이나 커스텀 데이터들이 저장될 예정입니다

[ preferences ]
| setting | boolean |

[ tags ]
기본 태그를 수정 / 추가 / 삭제 가능합니다
"""

byteDB = sqlite3.connect("./database/byte.sql", check_same_thread=False)
"""
해시와 바이트로 이루어진 데이터가 연결되어있습니다
미디어 파일을 저장하기에 용량이 매우 크므로 사후 관리가 필요할 것으로 보입니다

[ thumbnail ]
| hash | byte |
해시와 바이트가 묶여있는 꼴
"""

logDB = sqlite3.connect("./database/log.sql", check_same_thread=False)
"""
API가 프로그램에 입력한 모든 SQL 관련 명령어가 저장됩니다
추후 롤백에 이용됩니다

[ logs ]
| ip | token | sql |
"""