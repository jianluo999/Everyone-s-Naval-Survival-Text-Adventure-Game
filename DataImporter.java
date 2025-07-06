import java.sql.*;
import java.io.*;
import java.nio.charset.StandardCharsets;

public class DataImporter {
    private static final String DB_URL = "jdbc:mysql://localhost:3306/sailing_game?useUnicode=true&characterEncoding=utf8mb4&serverTimezone=UTC";
    private static final String USER = "root";
    private static final String PASS = "mgsincos30";

    public static void main(String[] args) {
        try {
            Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);
            System.out.println("数据库连接成功！");
            
            // 导入第1章剩余场景
            importChapter1Remaining(conn);
            
            // 导入第2章场景
            importChapter2(conn);
            
            // 导入第5章场景
            importChapter5(conn);
            
            conn.close();
            System.out.println("数据导入完成！");
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    private static void importChapter1Remaining(Connection conn) throws SQLException {
        System.out.println("导入第1章剩余场景...");
        
        String sql = "INSERT INTO stories (story_id, title, content, chapter, scene, story_type, is_ending) VALUES (?, ?, ?, ?, ?, ?, ?)";
        PreparedStatement pstmt = conn.prepareStatement(sql);
        
        // 场景24
        pstmt.setString(1, "story_1_24");
        pstmt.setString(2, "船只差异");
        pstmt.setString(3, "\"你有蔬菜？我怎么只有香肠？\"\n\n在海上，蔬菜可比肉类珍稀多了。\n\n\"船呢，你们的船大吗，我的船有一百多米，太大了...\"\n\n\"什么！我的船只有十米！\"");
        pstmt.setInt(4, 1);
        pstmt.setInt(5, 24);
        pstmt.setString(6, "NORMAL");
        pstmt.setBoolean(7, false);
        pstmt.executeUpdate();
        
        // 场景25
        pstmt.setString(1, "story_1_25");
        pstmt.setString(2, "公平性质疑");
        pstmt.setString(3, "\"靠！这游戏根本不公平，你的船一级就有大炮！\"\n\n\"特殊船有技能的，我的船完全是白板。\"\n\n\"我要刷初始，有没有氪金商城？我有的是钱！\"");
        pstmt.setInt(4, 1);
        pstmt.setInt(5, 25);
        pstmt.setString(6, "DIALOGUE");
        pstmt.setBoolean(7, false);
        pstmt.executeUpdate();
        
        // 场景26
        pstmt.setString(1, "story_1_26");
        pstmt.setString(2, "探索船舱");
        pstmt.setString(3, "你合上日志，也开始在房间翻找起来。\n\n你发现骸骨手里的燧发枪是一件装备。");
        pstmt.setInt(4, 1);
        pstmt.setInt(5, 26);
        pstmt.setString(6, "NORMAL");
        pstmt.setBoolean(7, false);
        pstmt.executeUpdate();
        
        // 场景27
        pstmt.setString(1, "story_1_27");
        pstmt.setString(2, "武器获得");
        pstmt.setString(3, "你将燧发枪拿起，感觉沉甸甸的，很有分量。\n\n虽然锈蚀严重，但你能感觉到它曾经的威力。");
        pstmt.setInt(4, 1);
        pstmt.setInt(5, 27);
        pstmt.setString(6, "NORMAL");
        pstmt.setBoolean(7, false);
        pstmt.executeUpdate();
        
        // 场景28
        pstmt.setString(1, "story_1_28");
        pstmt.setString(2, "警告纸条");
        pstmt.setString(3, "纸条的背面还有一些字迹：\n\n\"船舱里还有一些补给，在床底下的箱子里。\"");
        pstmt.setInt(4, 1);
        pstmt.setInt(5, 28);
        pstmt.setString(6, "NORMAL");
        pstmt.setBoolean(7, false);
        pstmt.executeUpdate();
        
        // 场景29
        pstmt.setString(1, "story_1_29");
        pstmt.setString(2, "补给发现");
        pstmt.setString(3, "你蹲下身，在床底下摸索着。\n\n果然，有一个木制的箱子。");
        pstmt.setInt(4, 1);
        pstmt.setInt(5, 29);
        pstmt.setString(6, "NORMAL");
        pstmt.setBoolean(7, false);
        pstmt.executeUpdate();
        
        // 场景30
        pstmt.setString(1, "story_1_30");
        pstmt.setString(2, "准备出海");
        pstmt.setString(3, "收拾好物品后，你走出船舱，来到甲板上。\n\n海风吹拂着你的脸庞，远处是一望无际的大海。");
        pstmt.setInt(4, 1);
        pstmt.setInt(5, 30);
        pstmt.setString(6, "NORMAL");
        pstmt.setBoolean(7, false);
        pstmt.executeUpdate();
        
        pstmt.close();
        System.out.println("第1章剩余场景导入完成！");
    }
    
    private static void importChapter2(Connection conn) throws SQLException {
        System.out.println("导入第2章场景...");
        
        String sql = "INSERT INTO stories (story_id, title, content, chapter, scene, story_type, is_ending) VALUES (?, ?, ?, ?, ?, ?, ?)";
        PreparedStatement pstmt = conn.prepareStatement(sql);
        
        // 场景1
        pstmt.setString(1, "story_2_1");
        pstmt.setString(2, "深海探索开始");
        pstmt.setString(3, "你决定向深海进发，寻找更多的资源和秘密。");
        pstmt.setInt(4, 2);
        pstmt.setInt(5, 1);
        pstmt.setString(6, "ADVENTURE");
        pstmt.setBoolean(7, false);
        pstmt.executeUpdate();
        
        pstmt.close();
        System.out.println("第2章场景导入完成！");
    }
    
    private static void importChapter5(Connection conn) throws SQLException {
        System.out.println("导入第5章场景...");
        
        String sql = "INSERT INTO stories (story_id, title, content, chapter, scene, story_type, is_ending) VALUES (?, ?, ?, ?, ?, ?, ?)";
        PreparedStatement pstmt = conn.prepareStatement(sql);
        
        // 从文件中读取的场景41-49
        String[][] chapter5Data = {
            {"story_5_41", "浸水的宝箱 - 场景41", "这次钓了一个多小时，天色渐暗。", "NORMAL"},
            {"story_5_42", "浸水的宝箱 - 场景42", "这鱼很恶心，你理智下降2点。", "NORMAL"},
            {"story_5_43", "浸水的宝箱 - 场景43", "可就在你收起钓竿，准备回舱休息时。", "NORMAL"},
            {"story_5_44", "浸水的宝箱 - 场景44", "你留了个心眼，一手持发枪。", "NORMAL"},
            {"story_5_45", "浸水的宝箱 - 场景45", "那是一条章鱼，只是脑袋换成了人的心脏。", "NORMAL"},
            {"story_5_46", "浸水的宝箱 - 场景46", "吞来理智下降，会手抖人的心脏。", "NORMAL"},
            {"story_5_47", "浸水的宝箱 - 场景47", "提示：不可突破凡物的极限！", "NORMAL"},
            {"story_5_48", "浸水的宝箱 - 场景48", "因为系统提醒过，晚上会有危险。", "NORMAL"},
            {"story_5_49", "浸水的宝箱 - 场景49", "你很木没有睡意，手是打开世界聊天。", "NORMAL"}
        };
        
        for (int i = 0; i < chapter5Data.length; i++) {
            pstmt.setString(1, chapter5Data[i][0]);
            pstmt.setString(2, chapter5Data[i][1]);
            pstmt.setString(3, chapter5Data[i][2]);
            pstmt.setInt(4, 5);
            pstmt.setInt(5, 41 + i);
            pstmt.setString(6, chapter5Data[i][3]);
            pstmt.setBoolean(7, false);
            pstmt.executeUpdate();
        }
        
        pstmt.close();
        System.out.println("第5章场景导入完成！");
    }
}
