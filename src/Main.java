import com.mongodb.*;
import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class Main {

    public static void main(String[] args) {

        // 调用Python代码部分，可以在Java的控制台显示Python的标准输出
        try {
            System.out.println("--- Start Running Python ---");
            String[] args1 = new String[]{"python", "SingleFileVersion.py"};
            Process pr = Runtime.getRuntime().exec(args1);
            System.out.println(args1[1]);
            BufferedReader in = new BufferedReader(new InputStreamReader(
                    pr.getInputStream(), "GBK"));
            String line;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
            in.close();
            pr.waitFor();
            System.out.println("--- End Python ---");
        } catch (IOException IOE) {
            System.out.println("Python文件出错。");
            IOE.printStackTrace();
        } catch (InterruptedException IE) {
            System.out.println("等待Python运行时出错。");
        }


        // 连接Mongo数据库，这部分项目里已经有了，可灵活调整
        Mongo mongo = new Mongo("localhost", 27017);
        DB database = mongo.getDB("config");
        DBCollection collection = database.getCollection("data_assembled");


        // 添加需要读取的文件，这部分文件事实上由Python代码负责生成
        List<String> fileNames = new ArrayList<>();
        fileNames.add("0人工智能_dbcontent.txt");
        fileNames.add("1智能制造_dbcontent.txt");
        fileNames.add("2大数据_dbcontent.txt");
        fileNames.add("3云计算_dbcontent.txt");
        fileNames.add("4工业互联网_dbcontent.txt");
        fileNames.add("5网络安全_dbcontent.txt");
        fileNames.add("6集成电路_dbcontent.txt");
        fileNames.add("7物联网_dbcontent.txt");


        // 读取文件并写入数据库
        for (String fileName : fileNames) {
            String field = fileName.substring(1, fileName.indexOf('_'));
            System.out.println(field);
            File file = new File("_tempfiles/" + fileName);
            try {
                InputStreamReader reader = new InputStreamReader(new FileInputStream(file), "GBK");
                BufferedReader br = new BufferedReader(reader);
                String content = "";
                content = br.readLine();
                System.out.println(content);
                br.close();
                DBObject object = new BasicDBObject("functionName", "GetExpectationByField")
                        .append("parameters", field).append("content", content);
                collection.insert(object);

            } catch (FileNotFoundException FNFE) {
                System.out.println("文件读取出错。请检查是否有xxx_dbcontent.txt");
            } catch (IOException IOE) {
                System.out.println("文件中无内容。");
            }

        }
    }
}
