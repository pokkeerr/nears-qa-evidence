NEARS-4120 QA cycle 0 progress (checkpoint)
AC1 PASS api-matrix.txt (6 rows owner+employee x mk-none/mk-unsub/mk-unsub-app: 403 auth-002, no token, sentinel auth_token unchanged: api-token-after.txt)
AC2 PASS web-matrix.txt + ac2-web-mk-none-login-error.png + web-login-remember-token-after.txt
AC3 PASS api + web controls (api-matrix.txt, web-matrix.txt)
AC4 PASS api controls 403 auth-002 no vendor.login_suspended line
AC5 PASS ac5-vendorapp-observations.txt + ac5-vendorapp-*.png
AC6 PASS one [FAIL] vendor.login_suspended line per refused rid; 0 for admitted/401 rids
phpunit-backstop.txt: 8 classes green
