使用说明：
1. 本python脚本使用2.7.x版本，不支持3.x. python -V
2. 由于使用了linux的shell指令（unzip），仅支持linux系统，在ubuntu上验证通过。
3. 确保jdk环境已经建立，在jdk1.7环境下测试通过
4. GUI使用的python的TKinter插件，确保python-tk模块已经安装。unbuntu： sudo apt-get install python-tk
5. 如果要修改原始包和目标包的初始选择路径，请修改第24行'initialdir'对应的值
6. 最终的差分包缺省会生成在该python的当前目录，命名规则是： <model>_<yyyymmddhhmmss>.zip
7. 确保python所在目录，对于当前用户来说有写权限。