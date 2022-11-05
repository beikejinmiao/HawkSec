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

