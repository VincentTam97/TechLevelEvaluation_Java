# TechLevelEvaluation_Java

### 注意事项

- 本程序已经可以独立正常运行

    - Python：需要安装anaconda3，并安装pymongo库

    - Java：需要mongo-java-driver，应该已安装好
    
    - 需要在运行的机器上配置python环境变量，见https://blog.csdn.net/u012513525/article/details/54927333

- Python文件放在Java项目的工作目录下，不要移动

- Java项目的工作目录下必须要提前创建 _tempfiles 目录

- 迁移时，将Main类下的Main函数嵌入原项目，并作合适修改即可