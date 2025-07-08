#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整工作流自动化脚本 - 一键执行从章节文件到游戏运行的完整流程
修复版本：解决所有工作流环节的bug
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

class CompleteWorkflowAutomation:
    def __init__(self):
        self.project_root = Path.cwd()
        self.steps_completed = []
        self.errors = []
        
    def log_step(self, step_name: str, success: bool, message: str = ""):
        """记录步骤执行结果"""
        status = "✅" if success else "❌"
        print(f"{status} {step_name}: {message}")
        
        if success:
            self.steps_completed.append(step_name)
        else:
            self.errors.append(f"{step_name}: {message}")
    
    def run_script(self, script_name: str, description: str) -> bool:
        """运行Python脚本"""
        print(f"\n🚀 执行: {description}")
        
        try:
            result = subprocess.run([sys.executable, script_name], 
                                  capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                self.log_step(description, True, "执行成功")
                return True
            else:
                self.log_step(description, False, f"执行失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_step(description, False, "执行超时")
            return False
        except Exception as e:
            self.log_step(description, False, f"执行异常: {str(e)}")
            return False
    
    def check_prerequisites(self) -> bool:
        """检查前置条件"""
        print("🔍 检查前置条件...")
        
        # 检查章节文件目录
        chapters_dir = self.project_root / "novel_texts" / "chapters"
        if not chapters_dir.exists():
            self.log_step("章节目录检查", False, f"找不到目录: {chapters_dir}")
            return False
        
        chapter_files = list(chapters_dir.glob("chapter_*_data.txt"))
        if len(chapter_files) < 10:
            self.log_step("章节文件检查", False, f"章节文件太少: {len(chapter_files)}")
            return False
        
        self.log_step("章节文件检查", True, f"发现 {len(chapter_files)} 个章节文件")
        
        # 检查必要的脚本文件
        required_scripts = [
            "fixed_novel_to_game_converter.py",
            "fixed_story_flow_optimizer.py", 
            "fixed_sql_generator.py",
            "fixed_database_importer.py"
        ]
        
        for script in required_scripts:
            if not (self.project_root / script).exists():
                self.log_step("脚本文件检查", False, f"找不到脚本: {script}")
                return False
        
        self.log_step("脚本文件检查", True, "所有必要脚本都存在")
        return True
    
    def step1_convert_chapters(self) -> bool:
        """步骤1: 转换章节文件为游戏场景"""
        return self.run_script("fixed_novel_to_game_converter.py", "章节转换为游戏场景")
    
    def step2_optimize_story_flow(self) -> bool:
        """步骤2: 优化故事流"""
        return self.run_script("fixed_story_flow_optimizer.py", "故事流优化")
    
    def step3_generate_sql(self) -> bool:
        """步骤3: 生成SQL文件"""
        return self.run_script("fixed_sql_generator.py", "生成SQL导入文件")
    
    def step4_import_database(self) -> bool:
        """步骤4: 导入数据库"""
        return self.run_script("fixed_database_importer.py", "导入数据到数据库")
    
    def step5_start_backend(self) -> bool:
        """步骤5: 启动后端服务器"""
        print("\n🚀 执行: 启动后端服务器")
        
        backend_dir = self.project_root / "backend"
        if not backend_dir.exists():
            self.log_step("启动后端服务器", False, "找不到backend目录")
            return False
        
        try:
            # 检查后端是否已经在运行
            import requests
            try:
                response = requests.get("http://localhost:8080/api/stories", timeout=2)
                if response.status_code == 200:
                    self.log_step("启动后端服务器", True, "后端服务器已在运行")
                    return True
            except:
                pass
            
            # 启动后端服务器
            print("正在启动后端服务器...")
            process = subprocess.Popen(
                ["mvn", "spring-boot:run"],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 等待服务器启动
            for i in range(30):  # 等待最多30秒
                try:
                    response = requests.get("http://localhost:8080/api/stories", timeout=1)
                    if response.status_code == 200:
                        self.log_step("启动后端服务器", True, "后端服务器启动成功")
                        return True
                except:
                    pass
                time.sleep(1)
                print(f"等待后端启动... ({i+1}/30)")
            
            self.log_step("启动后端服务器", False, "后端服务器启动超时")
            return False
            
        except Exception as e:
            self.log_step("启动后端服务器", False, f"启动失败: {str(e)}")
            return False
    
    def step6_start_frontend(self) -> bool:
        """步骤6: 启动前端服务器"""
        print("\n🚀 执行: 启动前端服务器")
        
        frontend_dir = self.project_root / "frontend"
        if not frontend_dir.exists():
            self.log_step("启动前端服务器", False, "找不到frontend目录")
            return False
        
        try:
            # 检查前端是否已经在运行
            import requests
            try:
                response = requests.get("http://localhost:3000", timeout=2)
                if response.status_code == 200:
                    self.log_step("启动前端服务器", True, "前端服务器已在运行")
                    return True
            except:
                pass
            
            # 启动前端服务器
            print("正在启动前端服务器...")
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 等待服务器启动
            for i in range(20):  # 等待最多20秒
                try:
                    response = requests.get("http://localhost:3000", timeout=1)
                    if response.status_code == 200:
                        self.log_step("启动前端服务器", True, "前端服务器启动成功")
                        return True
                except:
                    pass
                time.sleep(1)
                print(f"等待前端启动... ({i+1}/20)")
            
            self.log_step("启动前端服务器", False, "前端服务器启动超时")
            return False
            
        except Exception as e:
            self.log_step("启动前端服务器", False, f"启动失败: {str(e)}")
            return False
    
    def step7_verify_integration(self) -> bool:
        """步骤7: 验证前后端集成"""
        print("\n🚀 执行: 验证前后端集成")
        
        try:
            import requests
            
            # 测试后端API
            response = requests.get("http://localhost:8080/api/stories/story_1_1", timeout=5)
            if response.status_code != 200:
                self.log_step("验证前后端集成", False, f"后端API测试失败: {response.status_code}")
                return False
            
            story_data = response.json()
            if not story_data.get('storyId'):
                self.log_step("验证前后端集成", False, "后端返回数据格式错误")
                return False
            
            # 测试选择API
            response = requests.get("http://localhost:8080/api/choices/story_1_1", timeout=5)
            if response.status_code != 200:
                self.log_step("验证前后端集成", False, f"选择API测试失败: {response.status_code}")
                return False
            
            choices_data = response.json()
            if not isinstance(choices_data, list) or len(choices_data) == 0:
                self.log_step("验证前后端集成", False, "选择数据为空")
                return False
            
            self.log_step("验证前后端集成", True, f"API测试成功，获得 {len(choices_data)} 个选择")
            return True
            
        except Exception as e:
            self.log_step("验证前后端集成", False, f"集成测试失败: {str(e)}")
            return False
    
    def generate_report(self):
        """生成执行报告"""
        report_file = self.project_root / "workflow_execution_report.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 工作流执行报告\n\n")
            f.write(f"执行时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 执行步骤\n")
            for i, step in enumerate(self.steps_completed, 1):
                f.write(f"{i}. ✅ {step}\n")
            
            if self.errors:
                f.write("\n## 错误信息\n")
                for error in self.errors:
                    f.write(f"- ❌ {error}\n")
            
            f.write(f"\n## 总结\n")
            f.write(f"- 成功步骤: {len(self.steps_completed)}\n")
            f.write(f"- 失败步骤: {len(self.errors)}\n")
            
            if len(self.errors) == 0:
                f.write("- 状态: ✅ 工作流执行成功\n")
                f.write("- 游戏访问地址: http://localhost:3000\n")
                f.write("- 后端API地址: http://localhost:8080/api\n")
            else:
                f.write("- 状态: ❌ 工作流执行失败\n")
        
        print(f"\n📊 执行报告已生成: {report_file}")
    
    def run_complete_workflow(self):
        """运行完整工作流"""
        print("🎮 完整工作流自动化")
        print("=" * 60)
        
        # 检查前置条件
        if not self.check_prerequisites():
            print("\n❌ 前置条件检查失败，无法继续执行")
            return False
        
        # 执行各个步骤
        steps = [
            self.step1_convert_chapters,
            self.step2_optimize_story_flow,
            self.step3_generate_sql,
            self.step4_import_database,
            self.step5_start_backend,
            self.step6_start_frontend,
            self.step7_verify_integration
        ]
        
        for step in steps:
            if not step():
                print(f"\n❌ 工作流在步骤 '{step.__name__}' 失败")
                break
        
        # 生成报告
        self.generate_report()
        
        # 显示结果
        if len(self.errors) == 0:
            print("\n🎉 工作流执行成功！")
            print("🌐 游戏访问地址: http://localhost:3000")
            print("🔧 后端API地址: http://localhost:8080/api")
        else:
            print(f"\n❌ 工作流执行失败，共 {len(self.errors)} 个错误")
            for error in self.errors:
                print(f"   - {error}")
        
        return len(self.errors) == 0

def main():
    """主函数"""
    automation = CompleteWorkflowAutomation()
    success = automation.run_complete_workflow()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
