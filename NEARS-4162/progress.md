NEARS-4162 QA progress. sha 0778d0e88df40bdef5ba52306c3f7e63a9bc7963 tree clean (git status --short empty) Mon Oct 12 10:39:16 +04 2026
employee fixture: qa4162.employee@nears-qa.test / Qa#4162-Emp!x9Zk (clone multi_food_db_qa4162, role 'QA4162 Role' id 4 store 4; made via Store Panel custom-role/create + employee/add-new)
servers: 8162 artisan pid 67148 php-S 67171 DB qa4162; 8163 artisan pid 93620 php-S 93627 DB qa4162a
AC2 PASS both modes (see ac2_firebase.txt ac2_manual.txt)
AC3 9 STUCK triggers PASS live (T1..T8; ac3_*.txt)
AC4 PASS live + AC6 schedule/message controls (ac4_ac6_schedule_message.txt)
