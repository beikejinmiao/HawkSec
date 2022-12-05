$HAWKSEC_HOME="D:/PycharmProjects/HawkSec"
# 使用工程venv
D:/PycharmProjects/HawkSec/venv/Scripts/pyinstaller --noconfirm --onefile --windowed --icon "$HAWKSEC_HOME/resources/image/app_logo_blue.png" --add-data "$HAWKSEC_HOME/conf/hawksec.yaml;conf/" --add-data "$HAWKSEC_HOME/resources;resources/" --add-data "$HAWKSEC_HOME/tools/unrar;tools/unrar/"  "$HAWKSEC_HOME/hawksec.py"

# 使用系统Python3.5
# https://www.cnblogs.com/onone/articles/8989259.html    【--icon必须为ico文件】
C:/OptSoft/Python/Python35/Scripts/pyinstaller --noconfirm --onefile --windowed --icon "$HAWKSEC_HOME/resources/image/app_logo_blue.ico" --add-data "$HAWKSEC_HOME/conf/hawksec.yaml;conf/" --add-data "$HAWKSEC_HOME/resources;resources/" --add-data "$HAWKSEC_HOME/tools/unrar;tools/unrar/"  "$HAWKSEC_HOME/hawksec.py"

# 移除--windowed参数，cmd窗口显示日志内容
# https://stackoverflow.com/questions/44641941/pyinstaller-fatal-error-failed-to-execute-script-when-using-multiprocessin
# pyinstaller打包后运行程序无法查看错误详情时,移除-windowed参数,可在控制台排查程序执行错误原因
C:/OptSoft/Python/Python35/Scripts/pyinstaller --noconfirm --onefile --icon "$HAWKSEC_HOME/resources/image/app_logo_blue.ico" --add-data "$HAWKSEC_HOME/conf/hawksec.yaml;conf/" --add-data "$HAWKSEC_HOME/resources;resources/" --add-data "$HAWKSEC_HOME/tools/unrar;tools/unrar/"  "$HAWKSEC_HOME/hawksec.py"

# 解决在Win7中的api-ms-win-crt-process-|1-1-0.dll缺失问题
# Win7 SP1未出现该问题，只在最初版Win7中出现
# 解决方案：添加 --paths "C:\Windows\System32\downlevel"
# https://stackoverflow.com/questions/48712154/pyinstaller-warning-lib-not-found
C:/OptSoft/Python/Python35/Scripts/pyinstaller --noconfirm --onefile --windowed --icon "$HAWKSEC_HOME/resources/image/app_logo_blue.ico" --add-data "$HAWKSEC_HOME/conf/hawksec.yaml;conf/" --add-data "$HAWKSEC_HOME/resources;resources/" --add-data "$HAWKSEC_HOME/tools/unrar;tools/unrar/"  --paths "C:\Windows\System32\downlevel"  "$HAWKSEC_HOME/hawksec.py"

# 如果使用NIS制作windows安装程序，必须使用`--onedir`参数而非`--onefile`
